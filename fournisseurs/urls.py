from django.urls import path
from . import views

urlpatterns = [
    path('', views.fournisseurs_list, name='fournisseurs_list'),
]
