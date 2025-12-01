from django.contrib import messages
from django.shortcuts import redirect
from django.core.paginator import Paginator
from django.db.models import Q


class SearchMixin:
    """Mixin for adding search functionality to views"""
    search_fields = []
    
    def get_search_query(self, request):
        return request.GET.get('search', '')
    
    def apply_search(self, queryset, search_query):
        if search_query and self.search_fields:
            search_filter = Q()
            for field in self.search_fields:
                search_filter |= Q(**{f"{field}__icontains": search_query})
            queryset = queryset.filter(search_filter)
        return queryset


class PaginationMixin:
    """Mixin for adding pagination to views"""
    paginate_by = 10
    
    def paginate_queryset(self, queryset, request):
        paginator = Paginator(queryset, self.paginate_by)
        page_number = request.GET.get('page')
        return paginator.get_page(page_number)


class MessageMixin:
    """Mixin for standardized success/error messages"""
    
    def success_message(self, request, message):
        messages.success(request, message)
    
    def error_message(self, request, message):
        messages.error(request, message)
    
    def validation_error(self, request, error):
        messages.error(request, f'Erreur de validation: {error}')
    
    def generic_error(self, request, error):
        messages.error(request, f'Une erreur est survenue: {str(error)}')


class CRUDMixin(SearchMixin, PaginationMixin, MessageMixin):
    """Combined mixin for common CRUD operations"""
    model = None
    template_name = None
    redirect_url = None
    
    def get_queryset(self):
        if hasattr(self.model, 'actif'):
            return self.model.objects.filter(actif=True)
        return self.model.objects.all()