from django.urls import path


from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", views.index, name="index"),
    path("profile/", views.myprofile, name="myprofile"),
    path("frealancers/", views.get_frealancers, name="frealancers"),
    path("login/", views.login_page, name="login_page"),
    path("search/", views.search, name="search"),
    path("register/", views.register_page, name="register_page"),
    path("logout/", views.logout_page, name="logout_page"),
    path("inbox/", views.inbox, name="inbox"),
    path("vaild/", views.vaild_account, name="vaild_account"),
    path("vaild/<user_id>", views.vaild_account, name="vaild_account"),
    path("vaild/<user_id>/<token>", views.vaild_account, name="vaild_account"),
    path("rest_password/", auth_views.PasswordResetView.as_view(template_name = 'reset/password_reset.html', html_email_template_name='reset/password_reset_email.html'), name='reset_password'),
    path("rest_password_sent/", auth_views.PasswordChangeDoneView.as_view(), name='password_reset_done'),
    path("rest/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(template_name = 'reset/password_confirm.html'), name='password_reset_confirm'),
    path("rest_password_complete/", auth_views.PasswordResetCompleteView.as_view(template_name = 'reset/password_reset_done.html'), name='password_reset_complete'),
    ]