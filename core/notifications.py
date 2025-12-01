from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
from produits.models import Produit
import logging

logger = logging.getLogger(__name__)


def check_low_stock():
    """Check for low stock products and send notifications"""
    threshold = getattr(settings, 'LOW_STOCK_THRESHOLD', 5)
    low_stock_products = Produit.objects.filter(quantite__lte=threshold)
    
    if low_stock_products.exists():
        send_low_stock_notification(low_stock_products)
        return low_stock_products
    return None


def send_low_stock_notification(products):
    """Send email notification for low stock products"""
    try:
        # Get admin users
        admin_users = User.objects.filter(is_staff=True, email__isnull=False).exclude(email='')
        
        if not admin_users.exists():
            logger.warning("No admin users with email found for stock notifications")
            return
        
        # Prepare email content
        product_list = "\n".join([
            f"- {p.nom}: {p.quantite} unités restantes"
            for p in products
        ])
        
        subject = f"Alerte Stock - {products.count()} produit(s) en rupture"
        message = f"""
Bonjour,

Les produits suivants ont un stock faible:

{product_list}

Seuil d'alerte configuré: {getattr(settings, 'LOW_STOCK_THRESHOLD', 5)} unités

Veuillez réapprovisionner ces produits.

Cordialement,
Système de Gestion de Stock
        """
        
        # Send to all admin users
        recipient_emails = [user.email for user in admin_users]
        
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=recipient_emails,
            fail_silently=False,
        )
        
        logger.info(f"Low stock notification sent to {len(recipient_emails)} admin(s)")
        
    except Exception as e:
        logger.error(f"Failed to send low stock notification: {e}")


def get_stock_alerts():
    """Get current stock alerts for dashboard"""
    threshold = getattr(settings, 'LOW_STOCK_THRESHOLD', 5)
    
    alerts = {
        'low_stock': Produit.objects.filter(quantite__lte=threshold),
        'out_of_stock': Produit.objects.filter(quantite=0),
        'critical_stock': Produit.objects.filter(quantite__lte=threshold//2),
    }
    
    return alerts