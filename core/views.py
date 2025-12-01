from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator
from produits.models import Produit, Category
from clients.models import Client
from fournisseurs.models import Fournisseur
from factures.models import Facture


@login_required
def global_search(request):
    """Global search across all models"""
    query = request.GET.get('q', '').strip()
    results = {}
    
    if query:
        # Search products
        results['produits'] = Produit.objects.filter(
            Q(nom__icontains=query) |
            Q(category__name__icontains=query)
        ).select_related('category')[:10]
        
        # Search clients
        results['clients'] = Client.objects.filter(
            Q(nom__icontains=query) |
            Q(prenom__icontains=query) |
            Q(email__icontains=query)
        )[:10]
        
        # Search suppliers
        results['fournisseurs'] = Fournisseur.objects.filter(
            Q(nom__icontains=query) |
            Q(adresse__icontains=query)
        )[:10]
        
        # Search invoices
        results['factures'] = Facture.objects.filter(
            Q(numero__icontains=query) |
            Q(client__nom__icontains=query) |
            Q(client__prenom__icontains=query)
        ).select_related('client')[:10]
        
        # Count total results
        total_results = sum(len(result) for result in results.values())
    else:
        total_results = 0
    
    context = {
        'query': query,
        'results': results,
        'total_results': total_results,
    }
    
    return render(request, 'core/search_results.html', context)


@login_required
def stock_alerts_view(request):
    """View for stock alerts management"""
    from core.notifications import get_stock_alerts
    
    alerts = get_stock_alerts()
    
    context = {
        'low_stock_products': alerts['low_stock'],
        'out_of_stock_products': alerts['out_of_stock'],
        'critical_stock_products': alerts['critical_stock'],
    }
    
    return render(request, 'core/stock_alerts.html', context)