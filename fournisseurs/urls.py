from django.urls import path
from . import views

urlpatterns = [
    path('', views.liste_fournisseurs, name='liste_fournisseurs'),
    path('ajouter/', views.ajouter_fournisseur, name='ajouter_fournisseur'),
    path('modifier/<int:id>/', views.modifier_fournisseur, name='modifier_fournisseur'),
    path('supprimer/<int:id>/', views.supprimer_fournisseur, name='supprimer_fournisseur'),
]
