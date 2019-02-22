from django.urls import path

from . import views

urlpatterns = [
    path(' ', views.index, name='index'),
    path('<str:ad_location>/', views.city, name='city')
]