from django.shortcuts import render, redirect, get_object_or_404
from .models import Client

# دالة لعرض قائمة العملاء
def liste_clients(request):
    clients = Client.objects.all()
    return render(request, "clients/liste.html", {'clients': clients})

# دالة لإضافة عميل جديد
def ajouter_client(request):
    if request.method == "POST":
        nom = request.POST.get("nom")
        prenom = request.POST.get("prenom")
        email = request.POST.get("email")
        telephone = request.POST.get("telephone")
        adresse = request.POST.get("adresse")

        Client.objects.create(
            nom=nom,
            prenom=prenom,
            email=email,
            telephone=telephone,
            adresse=adresse
        )
        return redirect("clients:liste_clients")  # ✅ namespace مستخدم

    return render(request, "clients/ajouter.html")

# دالة لتعديل عميل
def modifier_client(request, id):
    client = get_object_or_404(Client, id=id)
    
    if request.method == "POST":
        client.nom = request.POST.get("nom")
        client.prenom = request.POST.get("prenom")
        client.email = request.POST.get("email")
        client.telephone = request.POST.get("telephone")
        client.adresse = request.POST.get("adresse")
        client.save()
        
        return redirect("clients:liste_clients")  # ✅ namespace مستخدم
    
    return render(request, "clients/modifier.html", {'client': client})

# دالة لحذف عميل
def supprimer_client(request, id):
    client = get_object_or_404(Client, id=id)
    
    if request.method == "POST":
        client.delete()
        return redirect("clients:liste_clients")  # ✅ namespace مستخدم
    
    return render(request, "clients/supprimer.html", {'client': client})
