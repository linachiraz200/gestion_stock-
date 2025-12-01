from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template.loader import get_template
from django.contrib import messages
from .models import Facture, FactureItem
from clients.models import Client
from produits.models import Produit
import json


@login_required
def liste_factures(request):
    from django.core.paginator import Paginator
    from django.db.models import Q
    
    factures = Facture.objects.select_related('client', 'created_by').order_by('-date_creation')
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        factures = factures.filter(
            Q(numero__icontains=search_query) |
            Q(client__nom__icontains=search_query) |
            Q(client__prenom__icontains=search_query)
        )
    
    # Pagination
    paginator = Paginator(factures, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'factures/liste.html', {
        'factures': page_obj,
        'page_obj': page_obj,
        'search_query': search_query
    })


@login_required
def creer_facture(request):
    if request.method == 'POST':
        try:
            client_id = request.POST.get('client')
            items_data = request.POST.get('items')
            
            if not client_id or not items_data:
                messages.error(request, 'Veuillez sélectionner un client et ajouter des produits.')
                return redirect('factures:creer_facture')
            
            client = get_object_or_404(Client, id=client_id)
            items = json.loads(items_data)
            
            # Validate stock before creating facture
            for item in items:
                produit = get_object_or_404(Produit, id=item['produit_id'])
                if produit.quantite < item['quantite']:
                    messages.error(request, f'Stock insuffisant pour {produit.nom}. Stock disponible: {produit.quantite}')
                    return redirect('factures:creer_facture')
            
            # Create facture
            facture = Facture.objects.create(client=client, created_by=request.user)
            
            # Create items and update stock
            for item in items:
                produit = get_object_or_404(Produit, id=item['produit_id'])
                FactureItem.objects.create(
                    facture=facture,
                    produit=produit,
                    quantite=item['quantite'],
                    prix_unitaire=item['prix_unitaire']
                )
                produit.quantite -= item['quantite']
                produit.save()
            
            messages.success(request, f'Facture {facture.numero} créée avec succès.')
            return redirect('factures:detail_facture', id=facture.id)
            
        except Exception as e:
            messages.error(request, f'Erreur lors de la création de la facture: {str(e)}')
            return redirect('factures:creer_facture')
    
    clients = Client.objects.filter(actif=True).order_by('nom', 'prenom')
    produits = Produit.objects.filter(quantite__gt=0).order_by('nom')
    return render(request, 'factures/creer.html', {
        'clients': clients,
        'produits': produits
    })


@login_required
def detail_facture(request, id):
    facture = get_object_or_404(Facture, id=id)
    return render(request, 'factures/detail.html', {'facture': facture})


@login_required
def supprimer_facture(request, id):
    facture = get_object_or_404(Facture, id=id)
    if request.method == 'POST':
        try:
            # Restore stock
            for item in facture.items.all():
                item.produit.quantite += item.quantite
                item.produit.save()
            facture.delete()
            messages.success(request, 'Facture supprimée avec succès.')
        except Exception as e:
            messages.error(request, f'Erreur lors de la suppression: {str(e)}')
        return redirect('factures:liste_factures')
    return render(request, 'factures/supprimer.html', {'facture': facture})


@login_required
def print_facture(request, id):
    facture = get_object_or_404(Facture, id=id)
    return render(request, 'factures/print.html', {'facture': facture})


@login_required
def generate_pdf_facture(request, id):
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.units import cm
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.lib import colors
    from io import BytesIO
    
    facture = get_object_or_404(Facture, id=id)
    
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []
    
    # Header
    title = Paragraph(f"<b>FACTURE {facture.numero}</b>", styles['Title'])
    story.append(title)
    story.append(Spacer(1, 0.5*cm))
    
    # Client info
    client_info = f"<b>Client:</b><br/>{facture.client.prenom} {facture.client.nom}<br/>{facture.client.email}"
    story.append(Paragraph(client_info, styles['Normal']))
    story.append(Spacer(1, 0.5*cm))
    
    # Items table
    data = [['Produit', 'Quantité', 'Prix unitaire', 'Total']]
    for item in facture.items.all():
        data.append([item.produit.nom, str(item.quantite), f"{item.prix_unitaire} DZD", f"{item.total} DZD"])
    
    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    story.append(table)
    story.append(Spacer(1, 0.5*cm))
    
    # Totals
    totals = f"<b>Total HT:</b> {facture.total_ht} DZD<br/><b>Total TTC:</b> {facture.total_ttc} DZD"
    story.append(Paragraph(totals, styles['Normal']))
    
    doc.build(story)
    buffer.seek(0)
    
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="facture_{facture.numero}.pdf"'
    return response