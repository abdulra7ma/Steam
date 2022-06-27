from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import ActivateView, LoginView, RegistrationView, ForgotPassword, UserAPIView, LogoutView
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path('users/', UserAPIView.as_view()),
    path('register/', RegistrationView.as_view()),
    path('activate/<str:activation_code>/', ActivateView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('forgot_password/', ForgotPassword.as_view(), name="forgot-password"),
    # path('forgot_password_complete/<str:email>/<str:code>/', ForgotPasswordCompleteView.as_view(), name="forgot-password-complete"),
]
