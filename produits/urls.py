from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # الصفحة الرئيسية
    path('produits/', views.produits_list, name='produits_list'),  # صفحة المنتجات
]


