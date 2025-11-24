from django.http import HttpResponse

def home(request):
    return HttpResponse("مرحبا بكم في تطبيق إدارة المنتجات 🚀")