# views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.translation import activate

from .models import UserSettings


# =========================================
# MAIN SETTINGS PAGE
# =========================================
@login_required
def settings_page(request):

    settings_obj, created = UserSettings.objects.get_or_create(
        user=request.user
    )

    if request.method == "POST":

        # SAVE LANGUAGE
        language = request.POST.get("language")

        if language:

            settings_obj.language = language

            request.session['django_language'] = language

            activate(language)

        # SAVE SETTINGS
        settings_obj.dark_mode = (
            request.POST.get("dark_mode") == "on"
        )

        settings_obj.email_notifications = (
            request.POST.get("email_notifications") == "on"
        )

        settings_obj.push_notifications = (
            request.POST.get("push_notifications") == "on"
        )

        settings_obj.fingerprint_login = (
            request.POST.get("fingerprint_login") == "on"
        )

        settings_obj.two_factor_auth = (
            request.POST.get("two_factor_auth") == "on"
        )

        settings_obj.autoplay_videos = (
            request.POST.get("autoplay_videos") == "on"
        )

        settings_obj.offline_downloads = (
            request.POST.get("offline_downloads") == "on"
        )

        settings_obj.allow_chat = (
            request.POST.get("allow_chat") == "on"
        )

        settings_obj.allow_discussions = (
            request.POST.get("allow_discussions") == "on"
        )

        settings_obj.live_class_reminders = (
            request.POST.get("live_class_reminders") == "on"
        )

        settings_obj.save()

        return redirect("settings_page")

    return render(
        request,
        "settings/settings.html",
        {
            "settings_obj": settings_obj
        }
    )


# =========================================
# TRAINER SETTINGS
# =========================================
@login_required
def trainer_settings(request):

    if request.user.role != "trainer":
        return redirect("login")

    user = request.user

    settings_obj, created = UserSettings.objects.get_or_create(
        user=user
    )

    if request.method == "POST":

        # =====================================
        # USER DETAILS
        # =====================================

        user.username = request.POST.get("username")
        user.email = request.POST.get("email")
        user.phone = request.POST.get("phone")

        user.specialization = request.POST.get(
            "specialization"
        )

        user.experience = request.POST.get(
            "experience"
        )

        user.qualification = request.POST.get(
            "qualification"
        )

        user.gender = request.POST.get(
            "gender"
        )

        user.bio = request.POST.get(
            "bio"
        )

        user.address = request.POST.get(
            "address"
        )

        # =====================================
        # PROFILE IMAGE
        # =====================================

        if request.FILES.get("profile_image"):

            user.profile_image = request.FILES.get(
                "profile_image"
            )

        user.save()

        # =====================================
        # LANGUAGE
        # =====================================

        language = request.POST.get("language")

        if language:

            settings_obj.language = language

            request.session["django_language"] = language

            activate(language)

        # =====================================
        # SETTINGS
        # =====================================

        settings_obj.dark_mode = (
            request.POST.get("dark_mode") == "on"
        )

        settings_obj.email_notifications = (
            request.POST.get("email_notifications") == "on"
        )

        settings_obj.push_notifications = (
            request.POST.get("push_notifications") == "on"
        )

        settings_obj.two_factor_auth = (
            request.POST.get("two_factor_auth") == "on"
        )

        settings_obj.live_class_reminders = (
            request.POST.get("live_class_reminders") == "on"
        )

        settings_obj.allow_chat = (
            request.POST.get("allow_chat") == "on"
        )

        settings_obj.save()

        return redirect("trainer_settings")

    return render(
        request,
        "settings/trainer_settings.html",
        {
            "user": user,
            "settings_obj": settings_obj,
            "languages": UserSettings.LANGUAGE_CHOICES
        }
    )


# =========================================
# STUDENT SETTINGS
# =========================================
@login_required
def student_settings(request):

    if request.user.role != "student":
        return redirect("login")

    user = request.user

    settings_obj, created = UserSettings.objects.get_or_create(
        user=user
    )

    if request.method == "POST":

        # =====================================
        # USER DETAILS
        # =====================================

        user.username = request.POST.get("username")
        user.email = request.POST.get("email")
        user.phone = request.POST.get("phone")

        user.gender = request.POST.get(
            "gender"
        )

        user.dob = request.POST.get(
            "dob"
        )

        user.address = request.POST.get(
            "address"
        )

        # =====================================
        # PROFILE IMAGE
        # =====================================

        if request.FILES.get("profile_image"):

            user.profile_image = request.FILES.get(
                "profile_image"
            )

        user.save()

        # =====================================
        # LANGUAGE
        # =====================================

        language = request.POST.get("language")

        if language:

            settings_obj.language = language

            request.session["django_language"] = language

            activate(language)

        # =====================================
        # SETTINGS
        # =====================================

        settings_obj.dark_mode = (
            request.POST.get("dark_mode") == "on"
        )

        settings_obj.email_notifications = (
            request.POST.get("email_notifications") == "on"
        )

        settings_obj.push_notifications = (
            request.POST.get("push_notifications") == "on"
        )

        settings_obj.two_factor_auth = (
            request.POST.get("two_factor_auth") == "on"
        )

        settings_obj.live_class_reminders = (
            request.POST.get("live_class_reminders") == "on"
        )

        settings_obj.allow_chat = (
            request.POST.get("allow_chat") == "on"
        )

        settings_obj.save()

        return redirect("student_settings")

    return render(
        request,
        "settings/student_settings.html",
        {
            "user": user,
            "settings_obj": settings_obj,
            "languages": UserSettings.LANGUAGE_CHOICES
        }
    )