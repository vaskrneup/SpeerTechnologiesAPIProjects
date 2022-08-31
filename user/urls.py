from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from user import views

app_name = "user"

urlpatterns = [
    path("register/", views.RegisterView.as_view(), name="RegisterView"),
    path("get-refresh-token/", TokenObtainPairView.as_view(), name="GetRefreshToken"),
    path("get-access-token/", TokenRefreshView.as_view(), name="GetAccessToken"),
]
