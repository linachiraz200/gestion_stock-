from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.core.exceptions import ValidationError
from .models import Fournisseur


@login_required
def liste_fournisseurs(request):
    fournisseurs = Fournisseur.objects.filter(actif=True).order_by('nom')
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        fournisseurs = fournisseurs.filter(
            Q(nom__icontains=search_query) |
            Q(adresse__icontains=search_query) |
            Q(telephone__icontains=search_query)
        )
    
    # Pagination
    paginator = Paginator(fournisseurs, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'fournisseurs': page_obj,
        'page_obj': page_obj,
        'search_query': search_query,
        'total_fournisseurs': fournisseurs.count(),
    }
    return render(request, "fournisseur/liste.html", context)


@login_required
def ajouter_fournisseur(request):
    if request.method == "POST":
        try:
            # Check for duplicate name
            nom = request.POST.get("nom")
            if Fournisseur.objects.filter(nom=nom).exists():
                messages.error(request, 'Un fournisseur avec ce nom existe déjà.')
                return render(request, "fournisseur/ajouter.html")
            
            fournisseur = Fournisseur.objects.create(
                nom=nom,
                adresse=request.POST.get("adresse"),
                telephone=request.POST.get("telephone"),
                email=request.POST.get("email", "")
            )
            messages.success(request, f'Fournisseur "{fournisseur.nom}" ajouté avec succès!')
            return redirect("fournisseurs:liste_fournisseurs")
        except ValidationError as e:
            messages.error(request, f'Erreur de validation: {e}')
        except Exception as e:
            messages.error(request, f'Erreur lors de l\'ajout: {str(e)}')
    
    return render(request, "fournisseur/ajouter.html")


@login_required
def modifier_fournisseur(request, id):
    fournisseur = get_object_or_404(Fournisseur, id=id)
    
    if request.method == "POST":
        try:
            # Check for duplicate name (excluding current fournisseur)
            nom = request.POST.get("nom")
            if Fournisseur.objects.filter(nom=nom).exclude(id=fournisseur.id).exists():
                messages.error(request, 'Un autre fournisseur avec ce nom existe déjà.')
                return render(request, "fournisseur/modifier.html", {'fournisseur': fournisseur})
            
            fournisseur.nom = nom
            fournisseur.adresse = request.POST.get("adresse")
            fournisseur.telephone = request.POST.get("telephone")
            fournisseur.email = request.POST.get("email", "")
            fournisseur.save()
            
            messages.success(request, f'Fournisseur "{fournisseur.nom}" modifié avec succès!')
            return redirect("fournisseurs:liste_fournisseurs")
        except ValidationError as e:
            messages.error(request, f'Erreur de validation: {e}')
        except Exception as e:
            messages.error(request, f'Erreur lors de la modification: {str(e)}')
    
    return render(request, "fournisseur/modifier.html", {'fournisseur': fournisseur})


@login_required
def supprimer_fournisseur(request, id):
    fournisseur = get_object_or_404(Fournisseur, id=id)
    
    if request.method == "POST":
        try:
            fournisseur_nom = fournisseur.nom
            fournisseur.delete()
            messages.success(request, f'Fournisseur "{fournisseur_nom}" supprimé avec succès!')
        except Exception as e:
            messages.error(request, f'Erreur lors de la suppression: {str(e)}')
        return redirect("fournisseurs:liste_fournisseurs")
    
    return render(request, "fournisseur/supprimer.html", {'fournisseur': fournisseur})
