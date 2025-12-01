from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.core.exceptions import ValidationError
from .models import Client


@login_required
def liste_clients(request):
    clients = Client.objects.filter(actif=True).order_by('-date_creation')
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        clients = clients.filter(
            Q(nom__icontains=search_query) |
            Q(prenom__icontains=search_query) |
            Q(email__icontains=search_query)
        )
    
    # Pagination
    paginator = Paginator(clients, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'clients': page_obj,
        'page_obj': page_obj,
        'search_query': search_query,
        'total_clients': clients.count(),
    }
    return render(request, "clients/liste.html", context)

# دالة لإضافة عميل جديد


@login_required
def ajouter_client(request):
    if request.method == "POST":
        try:
            # Check for duplicate email
            email = request.POST.get("email")
            if Client.objects.filter(email=email).exists():
                messages.error(request, 'Un client avec cet email existe déjà.')
                return render(request, "clients/ajouter.html")
            
            client = Client.objects.create(
                nom=request.POST.get("nom"),
                prenom=request.POST.get("prenom"),
                email=email,
                telephone=request.POST.get("telephone"),
                adresse=request.POST.get("adresse")
            )
            messages.success(request, f'Client "{client.nom_complet}" ajouté avec succès!')
            return redirect("clients:liste_clients")
        except ValidationError as e:
            messages.error(request, f'Erreur de validation: {e}')
        except Exception as e:
            messages.error(request, f'Erreur lors de l\'ajout: {str(e)}')
    
    return render(request, "clients/ajouter.html")

# دالة لتعديل عميل


@login_required
def modifier_client(request, id):
    client = get_object_or_404(Client, id=id)
    
    if request.method == "POST":
        try:
            # Check for duplicate email (excluding current client)
            email = request.POST.get("email")
            if Client.objects.filter(email=email).exclude(id=client.id).exists():
                messages.error(request, 'Un autre client avec cet email existe déjà.')
                return render(request, "clients/modifier.html", {'client': client})
            
            client.nom = request.POST.get("nom")
            client.prenom = request.POST.get("prenom")
            client.email = email
            client.telephone = request.POST.get("telephone")
            client.adresse = request.POST.get("adresse")
            client.save()
            
            messages.success(request, f'Client "{client.nom_complet}" modifié avec succès!')
            return redirect("clients:liste_clients")
        except ValidationError as e:
            messages.error(request, f'Erreur de validation: {e}')
        except Exception as e:
            messages.error(request, f'Erreur lors de la modification: {str(e)}')
    
    return render(request, "clients/modifier.html", {'client': client})

# دالة لحذف عميل


@login_required
def supprimer_client(request, id):
    client = get_object_or_404(Client, id=id)
    
    if request.method == "POST":
        try:
            # Check if client is used in invoices
            from factures.models import Facture
            if Facture.objects.filter(client=client).exists():
                messages.error(request, 'Impossible de supprimer ce client car il a des factures associées.')
                return redirect('clients:liste_clients')
            
            client_nom = client.nom_complet
            client.delete()
            messages.success(request, f'Client "{client_nom}" supprimé avec succès!')
        except Exception as e:
            messages.error(request, f'Erreur lors de la suppression: {str(e)}')
        return redirect("clients:liste_clients")
    
    return render(request, "clients/supprimer.html", {'client': client})
