from django.urls import path, reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from . import views
from .services import block_user

app_name = "users"

urlpatterns = [
    path('login/', LoginView.as_view(template_name = 'users/login.html',
                                    success_url='/'), name='login'),
    path('register/', views.UserCreate.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('password-reset/', 
        PasswordResetView.as_view(template_name = "users/password_reset_form.html",
                                email_template_name = 'users/password_reset_email.html',
                                success_url = reverse_lazy('users:password_reset_done')),
        name='password_reset'),
    path('password-reset/done/',
        PasswordResetDoneView.as_view(template_name = "users/password_reset_done.html"),
        name='password_reset_done'),
    path('password-reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name="users/password_reset_confirm.html",
                                                                            success_url = reverse_lazy('users:password_reset_complete')),
        name='password_reset_confirm'),
    path('password-reset/complete/', PasswordResetCompleteView.as_view(template_name="users/password_reset_complete.html"),
        name='password_reset_complete'),
    path("list", views.UserList.as_view(), name="user_list"),
    path("block_user/<int:pk>", block_user, name="block_user"),
    ]