from django.urls import path
from . import views

app_name = 'clients'  # ✅ لازم باش namespace يخدم

urlpatterns = [
    path('', views.liste_clients, name='liste_clients'),
    path('ajouter/', views.ajouter_client, name='ajouter_client'),
    path('<int:id>/modifier/', views.modifier_client, name='modifier_client'),
    path('<int:id>/supprimer/', views.supprimer_client, name='supprimer_client'),
]
