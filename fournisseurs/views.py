from django.shortcuts import render
 # Create your views here.
  from django.shortcuts import render
   from .models import Fournisseur
   
    def fournisseurs_list(request): 
        fournisseurs = Fournisseur.objects.all() 
        return render(request, 'fournisseurs_list.html', {'fournisseurs': fournisseurs})