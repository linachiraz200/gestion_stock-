from django.db import models

class Client(models.Model):
    nom = models.CharField(max_length=100, verbose_name="الاسم")
    prenom = models.CharField(max_length=100, verbose_name="اللقب")
    email = models.EmailField(verbose_name="البريد الإلكتروني")
    telephone = models.CharField(max_length=20, verbose_name="رقم الهاتف")
    adresse = models.TextField(verbose_name="العنوان")
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ التسجيل")

    def __str__(self):
        return f"{self.prenom} {self.nom}"

    class Meta:
        verbose_name = "عميل"
        verbose_name_plural = "العملاء"