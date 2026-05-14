from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)

from reportlab.pdfgen import canvas

from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages
from django.http import HttpResponse
from django.core.mail import EmailMessage

from .models import Certificate
from .forms import CertificateForm

from courses.models import Course
from progress.models import Progress
from accounts.models import User

# =========================
# NOTIFICATIONS
# =========================
from notifications.utils import send_notification


# =====================================
# TRAINER SEND CERTIFICATE TO ADMIN
# =====================================

@login_required
def send_certificate_request(request, course_id, student_id):

    if request.user.role != "trainer":
        return redirect("login")

    course = get_object_or_404(
        Course,
        id=course_id
    )

    # =========================
    # VALIDATION
    # =========================

    progress = Progress.objects.filter(
        student_id=student_id,
        course=course,
        completed=True
    ).first()

    if not progress:

        messages.error(
            request,
            "Student has not completed the course."
        )

        return redirect("trainer_progress")

    # =========================
    # CREATE CERTIFICATE
    # =========================

    certificate, created = Certificate.objects.get_or_create(

        student_id=student_id,
        course=course,

        defaults={

            'trainer': request.user,
            'completed': True,
        }
    )

    if request.method == "POST":

        form = CertificateForm(

            request.POST,
            request.FILES,
            instance=certificate
        )

        if form.is_valid():

            cert = form.save(commit=False)

            cert.status = "pending"

            cert.completed = True

            cert.trainer = request.user

            cert.save()

            # =====================================
            # ADMIN NOTIFICATIONS
            # =====================================

            admins = User.objects.filter(
                role='admin'
            )

            for admin in admins:

                send_notification(
                    recipient=admin,
                    sender=request.user,
                    notif_type='admin',
                    message=(
                        f"Certificate request submitted "
                        f"for {cert.student.username}"
                    ),
                    course_name=cert.course.title
                )

            # =====================================
            # STUDENT NOTIFICATION
            # =====================================

            send_notification(
                recipient=cert.student,
                sender=request.user,
                notif_type='course',
                message=(
                    f"Your certificate request "
                    f"was submitted for approval."
                ),
                course_name=cert.course.title
            )

            messages.success(
                request,
                "Certificate sent to admin for approval."
            )

            return redirect("trainer_dashboard")

    else:

        form = CertificateForm(
            instance=certificate
        )

    return render(

        request,

        'certificates/send_certificate.html',

        {

            'form': form,
            'certificate': certificate
        }
    )


# =====================================
# ADMIN CERTIFICATE REQUESTS
# =====================================

@login_required
def admin_certificate_requests(request):

    if request.user.role != "admin":
        return redirect("login")

    certificates = Certificate.objects.filter(
        status='pending'
    ).order_by('-created_at')

    return render(

        request,

        'certificates/admin_certificate_requests.html',

        {

            'certificates': certificates
        }
    )


# =====================================
# ADMIN APPROVE CERTIFICATE
# =====================================

@login_required
def approve_certificate(request, certificate_id):

    if request.user.role != "admin":
        return redirect("login")

    certificate = get_object_or_404(

        Certificate,

        id=certificate_id
    )

    certificate.status = "approved"

    certificate.approved_by = request.user

    certificate.completed_at = timezone.now()

    certificate.save()

    # =====================================
    # STUDENT NOTIFICATION
    # =====================================

    send_notification(
        recipient=certificate.student,
        sender=request.user,
        notif_type='course',
        message=(
            f"Your certificate for "
            f"{certificate.course.title} "
            f"has been approved."
        ),
        course_name=certificate.course.title
    )

    # =====================================
    # TRAINER NOTIFICATION
    # =====================================

    send_notification(
        recipient=certificate.trainer,
        sender=request.user,
        notif_type='admin',
        message=(
            f"Certificate approved for "
            f"{certificate.student.username}."
        ),
        course_name=certificate.course.title
    )

    messages.success(
        request,
        "Certificate approved successfully."
    )

    return redirect(
        'admin_certificate_requests'
    )


# =====================================
# ADMIN REJECT CERTIFICATE
# =====================================

@login_required
def reject_certificate(request, certificate_id):

    if request.user.role != "admin":
        return redirect("login")

    certificate = get_object_or_404(

        Certificate,

        id=certificate_id
    )

    certificate.status = "rejected"

    certificate.save()

    # =====================================
    # STUDENT NOTIFICATION
    # =====================================

    send_notification(
        recipient=certificate.student,
        sender=request.user,
        notif_type='admin',
        message=(
            f"Your certificate for "
            f"{certificate.course.title} "
            f"was rejected."
        ),
        course_name=certificate.course.title
    )

    # =====================================
    # TRAINER NOTIFICATION
    # =====================================

    send_notification(
        recipient=certificate.trainer,
        sender=request.user,
        notif_type='admin',
        message=(
            f"Certificate rejected for "
            f"{certificate.student.username}."
        ),
        course_name=certificate.course.title
    )

    messages.error(
        request,
        "Certificate rejected."
    )

    return redirect(
        'admin_certificate_requests'
    )


# =====================================
# VIEW CERTIFICATE
# =====================================

@login_required
def view_certificate(request, certificate_id):

    certificate = get_object_or_404(

        Certificate,

        id=certificate_id,

        student=request.user,

        status='approved'
    )

    return render(

        request,

        'certificates/certificate.html',

        {

            'certificate': certificate
        }
    )


# =====================================
# DOWNLOAD CERTIFICATE PDF
# =====================================

@login_required
def download_certificate(request, certificate_id):

    certificate = get_object_or_404(

        Certificate,

        id=certificate_id,

        student=request.user,

        status='approved'
    )

    response = HttpResponse(
        content_type='application/pdf'
    )

    response['Content-Disposition'] = (

        f'attachment; '
        f'filename="certificate_{certificate.id}.pdf"'
    )

    p = canvas.Canvas(response)

    # TITLE
    p.setFont("Helvetica-Bold", 26)

    p.drawString(
        150,
        800,
        "Certificate of Completion"
    )

    # STUDENT
    p.setFont("Helvetica", 16)

    p.drawString(
        100,
        720,
        f"Student Name: "
        f"{certificate.student.username}"
    )

    # COURSE
    p.drawString(
        100,
        680,
        f"Course: "
        f"{certificate.course.title}"
    )

    # DATE
    p.drawString(
        100,
        640,
        f"Issued Date: "
        f"{certificate.issued_date}"
    )

    # DESCRIPTION
    p.drawString(
        100,
        580,
        "Successfully completed the course."
    )

    # DIRECTOR
    p.drawString(
        100,
        520,
        f"Director: "
        f"{certificate.director_name}"
    )

    p.showPage()

    p.save()

    return response


# =====================================
# EMAIL CERTIFICATE
# =====================================

@login_required
def email_certificate(request, certificate_id):

    certificate = get_object_or_404(

        Certificate,

        id=certificate_id,

        student=request.user,

        status='approved'
    )

    subject = "Your Course Certificate"

    message = f"""

    Hello {certificate.student.username},

    Congratulations!

    Your certificate for the course
    "{certificate.course.title}"
    has been approved.

    Regards,
    LMS Team
    """

    email = EmailMessage(

        subject,

        message,

        to=[certificate.student.email]
    )

    email.send()

    # =====================================
    # EMAIL SENT NOTIFICATION
    # =====================================

    send_notification(
        recipient=certificate.student,
        sender=None,
        notif_type='message',
        message=(
            f"Certificate email sent for "
            f"{certificate.course.title}"
        ),
        course_name=certificate.course.title
    )

    messages.success(
        request,
        "Certificate emailed successfully."
    )

    return redirect(
        'my_certificates'
    )


# =====================================
# STUDENT CERTIFICATE LIST
# =====================================

@login_required
def my_certificates(request):

    certificates = Certificate.objects.filter(

        student=request.user,

        status='approved'
    ).order_by('-created_at')

    return render(

        request,

        'certificates/my_certificates.html',

        {

            'certificates': certificates
        }
    )