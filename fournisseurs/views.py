from django.shortcuts import render, redirect, get_object_or_404
from .models import Fournisseur

def liste_fournisseurs(request):
    fournisseurs = Fournisseur.objects.all()
    return render(request, "fournisseur/liste.html", {'fournisseurs': fournisseurs})

def ajouter_fournisseur(request):
    if request.method == "POST":
        nom = request.POST.get("nom")
        adresse = request.POST.get("adresse")
        telephone = request.POST.get("telephone")
        Fournisseur.objects.create(nom=nom, adresse=adresse, telephone=telephone)
        return redirect("liste_fournisseurs")
    return render(request, "fournisseur/ajouter.html")

def modifier_fournisseur(request, id):
    fournisseur = get_object_or_404(Fournisseur, id=id)
    if request.method == "POST":
        fournisseur.nom = request.POST.get("nom")
        fournisseur.adresse = request.POST.get("adresse")
        fournisseur.telephone = request.POST.get("telephone")
        fournisseur.save()
        return redirect("liste_fournisseurs")
    return render(request, "fournisseur/modifier.html", {'fournisseur': fournisseur})

def supprimer_fournisseur(request, id):
    fournisseur = get_object_or_404(Fournisseur, id=id)
    if request.method == "POST":
        fournisseur.delete()
        return redirect("liste_fournisseurs")
    return render(request, "fournisseur/supprimer.html", {'fournisseur': fournisseur})

