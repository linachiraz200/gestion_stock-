from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.login_view, name='login'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),

    path('produits/', include('produits.urls')),
    path('fournisseur/', include('fournisseurs.urls')),
    path('clients/', include('clients.urls', namespace='clients')),
    path('factures/', include('factures.urls')),
    path('core/', include('core.urls')),
]

