from django.urls import path

from . import views

app_name = "quizes"
urlpatterns = [
    path('', views.index, name="index"),
]