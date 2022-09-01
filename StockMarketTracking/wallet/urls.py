from django.urls import path
from wallet import views

app_name = "wallet"

urlpatterns = [
    path("add-money/", views.AddMoney.as_view(), name="AddMoney"),
]
