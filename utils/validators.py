from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import re


def validate_phone_number(value):
    """Validate phone number format"""
    pattern = r'^[+]?[0-9\s\-()]{8,20}$'
    if not re.match(pattern, value):
        raise ValidationError(
            _('Format de téléphone invalide. Utilisez uniquement des chiffres, espaces, tirets et parenthèses.'),
            code='invalid_phone'
        )


def validate_positive_number(value):
    """Validate that number is positive"""
    if value <= 0:
        raise ValidationError(
            _('La valeur doit être positive.'),
            code='negative_value'
        )


def validate_stock_quantity(value):
    """Validate stock quantity"""
    if value < 0:
        raise ValidationError(
            _('La quantité en stock ne peut pas être négative.'),
            code='negative_stock'
        )


def validate_price(value):
    """Validate price format"""
    if value <= 0:
        raise ValidationError(
            _('Le prix doit être supérieur à zéro.'),
            code='invalid_price'
        )
    
    # Check for reasonable price range (adjust as needed)
    if value > 999999.99:
        raise ValidationError(
            _('Le prix semble trop élevé.'),
            code='price_too_high'
        )