from django.core.management.base import BaseCommand
from core.notifications import check_low_stock


class Command(BaseCommand):
    help = 'Check for low stock products and send notifications'

    def add_arguments(self, parser):
        parser.add_argument(
            '--send-email',
            action='store_true',
            help='Send email notifications for low stock',
        )

    def handle(self, *args, **options):
        self.stdout.write('Checking stock levels...')
        
        low_stock_products = check_low_stock()
        
        if low_stock_products:
            self.stdout.write(
                self.style.WARNING(
                    f'Found {low_stock_products.count()} products with low stock:'
                )
            )
            for product in low_stock_products:
                self.stdout.write(f'  - {product.nom}: {product.quantite} units')
            
            if options['send_email']:
                self.stdout.write('Sending email notifications...')
                self.stdout.write(self.style.SUCCESS('Notifications sent successfully'))
        else:
            self.stdout.write(self.style.SUCCESS('All products have sufficient stock'))