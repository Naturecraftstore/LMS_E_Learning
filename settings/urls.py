from django.urls import path
from . import views

urlpatterns = [

    # MAIN SETTINGS
    path(
        '',
        views.settings_page,
        name='settings_page'
    ),

    # TRAINER SETTINGS
    path(
        'trainer/',
        views.trainer_settings,
        name='trainer_settings'
    ),

    # STUDENT SETTINGS
    path(
        'student/',
        views.student_settings,
        name='student_settings'
    ),

]