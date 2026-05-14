# from django.urls import path
# from . import views

# app_name = 'teams'   # 🔥 VERY IMPORTANT

# urlpatterns = [
#     path('course/<int:course_id>/', views.course_teams, name='course_teams'),
#     path('create/<int:course_id>/', views.create_team, name='create_team'),

#     # ✅ ADD THIS (YOUR ERROR FIX)
#     path('search/', views.search, name='search'),

#     # ✅ notifications
#     path('notifications/', views.notifications, name='notifications'),

#     # ajax
#     path('get-students/', views.get_students, name='get_students'),

#     # file upload
#     path('upload/<int:team_id>/', views.upload_file, name='upload_file'),
# ]



# from django.urls import path
# from . import views

# app_name = 'teams'

# urlpatterns = [
#     # ✅ COURSE LIST PAGE (FIX FOR YOUR ERROR)
#     path('courses/', views.course_slides, name='course_slides'),

#     # Teams + chat
#     path('course/<int:course_id>/', views.course_teams, name='course_teams'),

#     # Create team
#     path('create/<int:course_id>/', views.create_team, name='create_team'),

#     # Search
#     path('search/', views.search, name='search'),

#     # Notifications
#     path('notifications/', views.notifications, name='notifications'),

#     # AJAX
#     path('get-students/', views.get_students, name='get_students'),

#     # File upload
#     path('upload/<int:team_id>/', views.upload_file, name='upload_file'),
# ]
    

from django.urls import path
from . import views

app_name = 'teams'

urlpatterns = [
    path('courses/', views.course_slides, name='course_slides'),
    path('course/<int:course_id>/', views.course_teams, name='course_teams'),
    path('create/<int:course_id>/', views.create_team, name='create_team'),
    path('search/', views.search, name='search'),
    path('get-students/', views.get_students, name='get_students'),
    path('notifications/', views.notifications, name='notifications'),
    path('delete-message/<int:msg_id>/', views.delete_message, name='delete_message'),
    path('react-message/<int:msg_id>/', views.react_message, name='react_message'),
    path(
    'trainer-courses/',
    views.trainer_course_slides,
    name='trainer_course_slides'
),

path(
    'student-courses/',
    views.student_course_slides,
    name='student_course_slides'
),


]