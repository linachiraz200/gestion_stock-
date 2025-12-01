from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse
import csv
from .models import Produit, Category


@login_required
def liste_produits(request):
    # Get all products and categories
    all_produits = Produit.objects.select_related('category').all()
    categories = Category.objects.prefetch_related('produits').all()
    
    # Initialize filtered products
    produits = all_produits
    
    # Get filter parameters
    search_query = request.GET.get('search', '')
    category_id = request.GET.get('category')
    selected_category_obj = None
    
    # Apply search filter
    if search_query:
        produits = produits.filter(
            Q(nom__icontains=search_query) |
            Q(category__name__icontains=search_query)
        )
    
    # Apply category filter
    if category_id:
        if category_id == 'none':
            # Filter for uncategorized products
            produits = produits.filter(category__isnull=True)
        else:
            try:
                selected_category_obj = Category.objects.get(id=category_id)
                produits = produits.filter(category_id=category_id)
            except Category.DoesNotExist:
                category_id = None
    
    # Calculate statistics based on filtered results
    low_stock_threshold = getattr(settings, 'LOW_STOCK_THRESHOLD', 5)
    filtered_products_list = list(produits)
    
    total_quantity = sum(p.quantite for p in filtered_products_list)
    total_stock_value = sum(p.quantite * p.prix for p in filtered_products_list)
    low_stock_count = sum(1 for p in filtered_products_list if p.quantite <= low_stock_threshold)
    
    # Pagination
    paginator = Paginator(produits, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Count uncategorized products
    uncategorized_count = Produit.objects.filter(category__isnull=True).count()
    
    context = {
        'page_obj': page_obj,
        'produits': page_obj,
        'categories': categories,
        'selected_category': category_id,
        'selected_category_obj': selected_category_obj,
        'search_query': search_query,
        'low_stock_threshold': low_stock_threshold,
        'low_stock_count': low_stock_count,
        'total_quantity': total_quantity,
        'total_stock_value': total_stock_value,
        'total_products': len(filtered_products_list),
        'uncategorized_count': uncategorized_count,
    }
    return render(request, 'produits/liste.html', context)


@login_required
def ajouter_produit(request):
    if request.method == "POST":
        try:
            category_id = request.POST.get('category')
            Produit.objects.create(
                nom=request.POST['nom'],
                quantite=int(request.POST['quantite']),
                prix=float(request.POST['prix']),
                category_id=category_id if category_id else None
            )
            messages.success(request, 'Produit ajouté avec succès!')
            return redirect('produits:liste_produits')
        except Exception as e:
            messages.error(request, f'Erreur lors de l\'ajout: {str(e)}')
    
    categories = Category.objects.all().order_by('name')
    return render(request, 'produits/ajouter.html', {'categories': categories})


@login_required
def modifier_produit(request, id):
    produit = get_object_or_404(Produit, id=id)
    if request.method == "POST":
        try:
            produit.nom = request.POST['nom']
            produit.quantite = int(request.POST['quantite'])
            produit.prix = float(request.POST['prix'])
            category_id = request.POST.get('category')
            produit.category_id = category_id if category_id else None
            produit.save()
            messages.success(request, 'Produit modifié avec succès!')
            return redirect('produits:liste_produits')
        except Exception as e:
            messages.error(request, f'Erreur lors de la modification: {str(e)}')
    
    categories = Category.objects.all().order_by('name')
    return render(request, 'produits/modifier.html', {'produit': produit, 'categories': categories})


@login_required
def supprimer_produit(request, id):
    produit = get_object_or_404(Produit, id=id)
    if request.method == "POST":
        try:
            # Check if product is used in any invoices
            from factures.models import FactureItem
            if FactureItem.objects.filter(produit=produit).exists():
                messages.error(request, 'Impossible de supprimer ce produit car il est utilisé dans des factures.')
                return redirect('produits:liste_produits')
            
            produit_nom = produit.nom
            produit.delete()
            messages.success(request, f'Produit "{produit_nom}" supprimé avec succès!')
        except Exception as e:
            messages.error(request, f'Erreur lors de la suppression: {str(e)}')
        return redirect('produits:liste_produits')
    return render(request, 'produits/supprimer.html', {'produit': produit})


@login_required
def export_produits_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="produits_export.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Nom', 'Catégorie', 'Quantité', 'Prix (DZD)', 'Stock Status'])
    
    low_stock_threshold = getattr(settings, 'LOW_STOCK_THRESHOLD', 5)
    produits = Produit.objects.select_related('category').all()
    
    for produit in produits:
        stock_status = 'Faible' if produit.quantite <= low_stock_threshold else 'Normal'
        category_name = produit.category.name if produit.category else 'Non classé'
        writer.writerow([
            produit.nom,
            category_name,
            produit.quantite,
            produit.prix,
            stock_status
        ])
    
    return response
