from django.urls import path
from . import views

urlpatterns = [
    path('complaint/student/', views.complaint_form_student, name='complaint_form_student'),
    path('complaint/warden/', views.complaint_form_warden, name='complaint_form_warden'),
    path('submit-complaint/', views.complaint_form_student, name='submit_complaint'),
    path('complaints/', views.complaints_view, name='complaints_list'),
    path('complaint/success/', views.complaint_success, name='complaint_success'),
    path('warden/hmsteam/', views.team_info_warden, name='team_info_warden'),
    path('student/hmsteam/', views.team_info_student, name='team_info_student'),
    path('emsteam/', views.page3, name='ems_team'),
    path('complaints/page2/', views.page2, name='page2'),
    path('complaints/page6/', views.page6, name='page6'),
    path('api/student-complaints/', views.fetch_student_complaints, name='fetch_student_complaints'),
    path('api/warden-complaints/', views.fetch_warden_complaints, name='fetch_warden_complaints'),
    path('api/update-complaint-status/', views.update_status_for_all_dashboards, name='update_complaint_status'),
    path('previous-student-complaints/', views.previous_student_complaints, name='previous_student_complaints'),
    path('previous-warden-complaints/', views.previous_warden_complaints, name='previous_warden_complaints'),
    path('api/student-complaints-for-warden/', views.fetch_student_complaints_for_warden, name='fetch_student_complaints_for_warden'),
    path('api/update-ems-status-and-student-status/', views.update_ems_status_and_student_status, name='update_ems_status_and_student_status'),
    path('api/active-complaints/', views.fetch_active_complaints, name='fetch_active_complaints'),
]