from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# ✅ صفحة تسجيل الدخول
def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')   # URL name بدل link مباشر
        else:
            return render(request, 'login.html', {
                'error': 'اسم المستخدم أو كلمة المرور غير صحيحة'
            })

    return render(request, 'login.html')


# ✅ تسجيل الخروج
@login_required
def logout_view(request):
    logout(request)
    return redirect('login')


# ✅ Dashboard مع جلب العملاء
@login_required
def dashboard(request):
    from clients.models import Client  # ✅ استيراد نموذج العملاء

    clients = Client.objects.all()  # جلب كل العملاء
    # ممكن تضيف عداد المنتجات والفواتير لاحقاً بنفس الطريقة
    return render(request, 'dashboard.html', {
        'clients': clients
    })
