from django.urls import path
from . import views

urlpatterns = [
    path('', views.convert_to_mp3, name='convert_to_mp3'),
]
