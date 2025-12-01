from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('search/', views.global_search, name='global_search'),
    path('alerts/', views.stock_alerts_view, name='stock_alerts'),
]