from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Produit

@login_required
def liste_produits(request):
    produits = Produit.objects.all()
    return render(request, 'produits/liste.html', {'produits': produits})

@login_required
def ajouter_produit(request):
    if request.method == "POST":
        Produit.objects.create(
            nom=request.POST['nom'],
            quantite=request.POST['quantite'],
            prix=request.POST['prix']
        )
        return redirect('liste_produits')
    return render(request, 'produits/ajouter.html')

@login_required
def modifier_produit(request, id):
    produit = get_object_or_404(Produit, id=id)
    if request.method == "POST":
        produit.nom = request.POST['nom']
        produit.quantite = request.POST['quantite']
        produit.prix = request.POST['prix']
        produit.save()
        return redirect('liste_produits')
    return render(request, 'produits/modifier.html', {'produit': produit})

@login_required
def supprimer_produit(request, id):
    produit = get_object_or_404(Produit, id=id)
    if request.method == "POST":
        produit.delete()
        return redirect('liste_produits')
    return render(request, 'produits/supprimer.html', {'produit': produit})

