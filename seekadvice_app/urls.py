from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from .forms import UserPasswordResetForm, UserSetPasswordForm

urlpatterns = [
    path('register1', views.registration_personal, name='registration_personal'),
    path('registerintercept', views.registration_service_intercept, name='registration_service_intercept'),
    path('register2', views.registration_service, name='registration_service'),
    path('register3', views.registration_questions, name='registration_questions'),
    path('htmx_test', views.htmx_test, name='htmx_test'),
    path('htmx_check_mail', views.htmx_check_mail, name='htmx_check_mail'),
    path('login', views.user_login),
    path('home', views.app_home),
    path('faq', views.faq),
    path('privacy', views.privacy),
    path('terms', views.terms),
    path('about', views.about),
    path('logout', views.user_logout),
    path('', views.seekadvice_list),
    path('seekadvice', views.seekadvice_list),
    path('seekadviceupdate', views.seekadvice_list_update_htmx, name='seekadvice_list_update_htmx'),
    path('seekadvicetechexperts', views.seekadvice_list_techexpert),
    path('seekadvicetechexpertsupdate', views.seekadvice_list_update_htmx_techexpert, name='seekadvice_list_update_htmx_techexpert'),
    path('changepersonal', views.change_personal),
    path('selfseekadvice', views.self_seekadvice),
    path('selfseekadvicetechexperts', views.self_seekadvice_techexpert),
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name = "seekadvice_app/registration/reset_password.html", form_class=UserPasswordResetForm), name ='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name = "seekadvice_app/registration/password_reset_sent.html"), name ='password_reset_done'),
    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name = "seekadvice_app/registration/password_reset_form.html", form_class=UserSetPasswordForm), name ='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name = "seekadvice_app/registration/password_reset_done.html"), name ='password_reset_complete'),
    path('deleteuser', views.delete_user),
    # path('sendrequest/<str:soid>/', views.send_request),
    path('sendrequestmessage', views.send_request_message),
    path('userprofile/<str:username_id>/', views.show_user_profile),
    path('serviceoffer/<str:serviceoffer_id>/', views.show_service_offer),
    path('social-auth/', include('social_django.urls', namespace="social")),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('activatemail', views.pre_activate),
]