from django.urls import path
from . import views

app_name = 'produits'

urlpatterns = [
    path('', views.liste_produits, name='liste_produits'),
    path('ajouter/', views.ajouter_produit, name='ajouter_produit'),
    path('modifier/<int:id>/', views.modifier_produit, name='modifier_produit'),
    path('supprimer/<int:id>/', views.supprimer_produit, name='supprimer_produit'),
    path('export/csv/', views.export_produits_csv, name='export_produits_csv'),
]
