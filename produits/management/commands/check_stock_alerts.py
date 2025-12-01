from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings
from produits.models import Produit


class Command(BaseCommand):
    help = 'Check for low stock products and send alerts'

    def handle(self, *args, **options):
        low_stock_threshold = getattr(settings, 'LOW_STOCK_THRESHOLD', 5)
        low_stock_products = Produit.objects.filter(quantite__lte=low_stock_threshold)
        
        if low_stock_products.exists():
            message = "Produits en stock faible:\n\n"
            for product in low_stock_products:
                message += f"- {product.nom}: {product.quantite} unités restantes\n"
            
            try:
                send_mail(
                    'Alerte Stock Faible - Gestion Stock',
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    ['admin@example.com'],  # Replace with actual admin email
                    fail_silently=False,
                )
                self.stdout.write(
                    self.style.SUCCESS(f'Alert sent for {low_stock_products.count()} products')
                )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'Failed to send email: {e}')
                )
        else:
            self.stdout.write(
                self.style.SUCCESS('No low stock products found')
            )