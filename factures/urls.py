from django.urls import path
from . import views

app_name = 'factures'

urlpatterns = [
    path('', views.liste_factures, name='liste_factures'),
    path('creer/', views.creer_facture, name='creer_facture'),
    path('<int:id>/', views.detail_facture, name='detail_facture'),
    path('<int:id>/supprimer/', views.supprimer_facture, name='supprimer_facture'),
    path('<int:id>/print/', views.print_facture, name='print_facture'),
    path('<int:id>/pdf/', views.generate_pdf_facture, name='generate_pdf_facture'),
]