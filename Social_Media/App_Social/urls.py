from django.urls import path
from App_Social import views

app_name = 'App_Social'

urlpatterns = [
    path("", views.home, name="home"),
]