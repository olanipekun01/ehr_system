from . import views
from django.urls import path, include


app_name = 'common'

# from .views import (
#     PasswordResetOTPEmailView,
#     PasswordResetConfirmationView,
# )

urlpatterns = [
    # path('register/', views.RegisterView.as_view(), name='register'),
    path('', views.Login, name='login'),
    path('login/', views.Login, name='login'),
    path('logout/', views.Logout, name='logout'),
    # path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    #password reset
#     path('reset-password-email/', PasswordResetOTPEmailView.as_view(), name='reset-password-email'),
#     path('reset-password-confirmation/', PasswordResetConfirmationView.as_view(), name='reset-passsword-confirmation'),
]