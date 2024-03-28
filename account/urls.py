from django.urls import path

from .views import CreateUserView, LoginView, PasswordResetRequestView, PasswordResetView

urlpatterns = [
    path('auth/register/', CreateUserView.as_view(), name='register'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('user/password-reset-request/', PasswordResetRequestView.as_view(), name='request-password-reset'),
    path('user/reset-password/', PasswordResetView.as_view(), name='password-reset')
]

