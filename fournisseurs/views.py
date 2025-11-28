from django.shortcuts import render, redirect, get_object_or_404
from .models import Fournisseur

# دالة لعرض قائمة الموردين
def liste_fournisseurs(request):
    fournisseurs = Fournisseur.objects.all()
    return render(request, "fournisseur/liste.html", {'fournisseurs': fournisseurs})

# دالة لإضافة مورد جديد
def ajouter_fournisseur(request):
    if request.method == "POST":
        nom = request.POST.get("nom")
        adresse = request.POST.get("adresse")
        telephone = request.POST.get("telephone")

        Fournisseur.objects.create(
            nom=nom,
            adresse=adresse,
            telephone=telephone
        )
        return redirect("liste_fournisseurs")  # غيرت المسار

    return render(request, "fournisseur/ajouter.html")

# دالة لتعديل مورد
def modifier_fournisseur(request, id):
    fournisseur = get_object_or_404(Fournisseur, id=id)
    
    if request.method == "POST":
        fournisseur.nom = request.POST.get("nom")
        fournisseur.adresse = request.POST.get("adresse")
        fournisseur.telephone = request.POST.get("telephone")
        fournisseur.save()
        
        return redirect("liste_fournisseurs")
    
    return render(request, "fournisseur/modifier.html", {'fournisseur': fournisseur})

# دالة لحذف مورد
def supprimer_fournisseur(request, id):
    fournisseur = get_object_or_404(Fournisseur, id=id)
    
    if request.method == "POST":
        fournisseur.delete()
        return redirect("liste_fournisseurs")
    
    return render(request, "fournisseur/supprimer.html", {'fournisseur': fournisseur})