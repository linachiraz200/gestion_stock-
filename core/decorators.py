from functools import wraps
from django.contrib import messages
from django.shortcuts import redirect
import logging

logger = logging.getLogger(__name__)


def handle_exceptions(redirect_url=None):
    """Decorator to handle exceptions in views"""
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            try:
                return view_func(request, *args, **kwargs)
            except Exception as e:
                logger.error(f"Error in {view_func.__name__}: {str(e)}")
                messages.error(request, f'Une erreur est survenue: {str(e)}')
                if redirect_url:
                    return redirect(redirect_url)
                return redirect('dashboard')
        return wrapper
    return decorator


def log_action(action_name):
    """Decorator to log user actions"""
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            logger.info(f"User {request.user.username} performed {action_name}")
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator