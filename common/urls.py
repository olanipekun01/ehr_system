from . import views
from django.urls import path, include
from django.conf.urls import handler404

app_name = 'common'

# from .views import (
#     PasswordResetOTPEmailView,
#     PasswordResetConfirmationView,
# )

# Define the custom 404 view
# Define the custom 404 view
def custom_404_view(request, exception):
    return render(request, '404.html', status=404)

# Set the handler for 404 errors
handler404 = custom_404_view

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