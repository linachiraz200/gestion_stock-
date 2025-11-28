from django.shortcuts import render

def fournisseurs_list(request):
    return render(request, 'fournisseurs_list.html')
