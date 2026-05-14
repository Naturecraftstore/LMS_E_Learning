from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from assignments.models import Assignment, Submission
from coding_tasks.models import CodingSubmission,CodingTask
from django.db.models import Avg
from courses.models import Course
from accounts.models import User
from notifications.utils import send_notification
from .models import Progress


# =========================
# STUDENT PROGRESS
# =========================

@login_required
def student_progress(request):

    if request.user.role != 'student':
        return redirect('login')

    student = request.user

    # COURSES
    courses = Course.objects.filter(students=student)

    # ASSIGNMENTS
    assignments = Assignment.objects.filter(course__in=courses)

    total_assignments = assignments.count()

    completed_assignments = Submission.objects.filter(
        student=student,
        status__in=['submitted', 'graded']
    ).count()

    # CODING
    coding_tasks = CodingTask.objects.filter(course__in=courses)

    completed_coding = CodingSubmission.objects.filter(
        student=student,
        status='Passed'
    ).count()

    # OVERALL PROGRESS
    total_items = total_assignments + coding_tasks.count()

    completed_items = (
        completed_assignments +
        completed_coding
    )

    progress_percent = 0

    if total_items > 0:

        progress_percent = int(
            (completed_items / total_items) * 100
        )

    # =========================
    # NOTIFICATIONS
    # =========================

    # Student notification
    send_notification(
        recipient=student,
        sender=None,
        notif_type='progress',
        message=f"Your overall course progress is {progress_percent}%.",
        progress=progress_percent
    )

    # Trainer notification
    if student.trainer:

        send_notification(
            recipient=student.trainer,
            sender=student,
            notif_type='progress',
            message=f"{student.username} progress updated to {progress_percent}%.",
            progress=progress_percent
        )

    # Completion notification
    if progress_percent >= 70:

        send_notification(
            recipient=student,
            sender=None,
            notif_type='progress',
            message="Congratulations! You completed course progress successfully.",
            progress=progress_percent
        )

    # Certificate eligibility
    if progress_percent >= 90:

        send_notification(
            recipient=student,
            sender=None,
            notif_type='progress',
            message="You are now eligible for certificate approval.",
            progress=progress_percent
        )

    return render(request, 'progress/student_progress.html', {

        'courses': courses,

        'total_courses': courses.count(),

        'total_assignments': total_assignments,

        'completed_assignments': completed_assignments,

        'coding_tasks': coding_tasks.count(),

        'completed_coding': completed_coding,

        'progress_percent': progress_percent,
    })
# =========================
# TRAINER PROGRESS
# =========================

@login_required
def trainer_progress(request):

    if request.user.role != 'trainer':
        return redirect('login')

    students = User.objects.filter(
        trainer=request.user,
        role='student'
    )

    progress_data = []

    for student in students:

        student_courses = Course.objects.filter(
            students=student,
            trainer=request.user
        )

        for course in student_courses:

            assignments = Assignment.objects.filter(
                course=course
            )

            total_assignments = assignments.count()

            completed_assignments = Submission.objects.filter(
                student=student,
                assignment__in=assignments,
                status__in=['submitted', 'graded']
            ).count()

            coding = CodingSubmission.objects.filter(
                student=student,
                task__course=course
            )

            passed = coding.filter(
                status='Passed'
            ).count()

            total_coding = coding.count()

            total_items = total_assignments + total_coding

            completed_items = (
                completed_assignments + passed
            )

            progress_percent = 0
                # Trainer notification to student


            if total_items > 0:
                progress_percent = int(
                    (completed_items / total_items) * 100
                )

            score = 0

            for c in coding:
                score += c.score or 0

            # Trainer notification to student

                send_notification(
                    recipient=student,
                    sender=request.user,
                    notif_type='progress',
                    message=f"Trainer checked your progress for {course.title}. Current progress: {progress_percent}%",
                    course_name=course.title,
                    progress=progress_percent
                )

                # Course completed

                if progress_percent >= 70:

                    send_notification(
                        recipient=student,
                        sender=request.user,
                        notif_type='progress',
                        message=f"You completed {course.title} successfully.",
                        course_name=course.title,
                        progress=progress_percent
                    )
            progress_data.append({
                'student': student,
                'course': course,
                'attendance': progress_percent,
                'score': score,
                'completed': progress_percent >= 70,
            })

    return render(request, 'progress/trainer_progress.html', {
        'progress': progress_data
    })


# =========================
# ADMIN PROGRESS
# =========================

@login_required
def admin_progress(request):

    if request.user.role != 'admin':
        return redirect('login')

    students = User.objects.filter(role='student')

    progress_data = []

    for student in students:

        student_courses = Course.objects.filter(
            students=student
        )

        for course in student_courses:

            assignments = Assignment.objects.filter(
                course=course
            )

            total_assignments = assignments.count()

            completed_assignments = Submission.objects.filter(
                student=student,
                assignment__in=assignments,
                status__in=['submitted', 'graded']
            ).count()

            coding = CodingSubmission.objects.filter(
                student=student,
                task__course=course
            )

            passed = coding.filter(
                status='Passed'
            ).count()

            total_coding = coding.count()

            total_items = total_assignments + total_coding

            completed_items = (
                completed_assignments + passed
            )

            progress_percent = 0

            if total_items > 0:
                progress_percent = int(
                    (completed_items / total_items) * 100
                )

            score = 0

            for c in coding:
                score += c.score or 0
                # Admin monitoring notification

                if progress_percent < 40:

                    send_notification(
                        recipient=student,
                        sender=request.user,
                        notif_type='admin',
                        message=f"Warning! Your progress in {course.title} is very low.",
                        course_name=course.title,
                        progress=progress_percent
                    )

                # Certificate eligibility

                if progress_percent >= 90:

                    send_notification(
                        recipient=student,
                        sender=request.user,
                        notif_type='progress',
                        message=f"You became eligible for certificate in {course.title}.",
                        course_name=course.title,
                        progress=progress_percent
                    )

            progress_data.append({
                'student': student,
                'course': course,
                'attendance': progress_percent,
                'score': score,
                'completed': progress_percent >= 70,
                'certificate_issued': progress_percent >= 90,
            })

    return render(request, 'progress/admin_progress.html', {
        'progress': progress_data
    })