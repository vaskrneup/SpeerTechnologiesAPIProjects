from django.urls import path
from share_manager import views

app_name = "share_manager"

urlpatterns = [
    path("get-all-scrips/", views.GetAllScrips.as_view(), name="GetAllScrips"),
    path("portfolio/", views.GetPortfolio.as_view(), name="GetPortfolio"),
]
