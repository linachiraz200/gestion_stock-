from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from clients.models import Client
from produits.models import Produit, Category
from fournisseurs.models import Fournisseur
from factures.models import Facture
from core.notifications import get_stock_alerts


def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')   # URL name بدل link مباشر
        else:
            return render(request, 'login.html', {
                'error': 'اسم المستخدم أو كلمة المرور غير صحيحة'
            })

    return render(request, 'login.html')


# ✅ تسجيل الخروج
@login_required
def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def dashboard(request):
    try:
        # Optimize queries with single database call
        clients = Client.objects.order_by('-date_creation')[:5]
        
        # Get counts efficiently
        produits_count = Produit.objects.count()
        fournisseurs_count = Fournisseur.objects.count()
        
        # Low stock calculation
        low_stock_threshold = getattr(settings, 'LOW_STOCK_THRESHOLD', 5)
        low_stock_count = Produit.objects.filter(
            quantite__lte=low_stock_threshold
        ).count()
        
        # Calculate total stock value
        total_stock_value = sum(
            p.quantite * p.prix for p in Produit.objects.only('quantite', 'prix')
        )
        
        # Get stock alerts
        alerts = get_stock_alerts()
        recent_factures = Facture.objects.select_related('client').order_by('-date_creation')[:5]
        
        context = {
            'clients': clients,
            'recent_factures': recent_factures,
            'produits_count': produits_count,
            'fournisseurs_count': fournisseurs_count,
            'low_stock_count': alerts['low_stock'].count(),
            'out_of_stock_count': alerts['out_of_stock'].count(),
            'low_stock_products': alerts['low_stock'][:10],
            'low_stock_threshold': low_stock_threshold,
            'total_stock_value': total_stock_value,
        }
        
        return render(request, 'dashboard.html', context)
        
    except Exception as e:
        messages.error(request, 'Erreur lors du chargement du tableau de bord')
        return render(request, 'dashboard.html', {})
