from django.shortcuts import render

def home(request):
    return render(request, 'home.html')

def produits_list(request):
    # مثال: منتجات ثابتة، يمكن تعديلها لاحقًا لتجلب من DB
    produits = [
        {'nom': 'Produit 1', 'prix': 10},
        {'nom': 'Produit 2', 'prix': 20},
        {'nom': 'Produit 3', 'prix': 30},
    ]
    return render(request, 'produits.html', {'produits': produits})
