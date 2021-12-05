from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('after_index', views.after_index, name='after_index'),
]
