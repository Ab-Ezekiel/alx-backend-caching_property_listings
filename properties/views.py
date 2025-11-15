# properties/views.py
from django.http import JsonResponse
from django.views.decorators.cache import cache_page

from .utils import get_all_properties  # import helper

@cache_page(60 * 15)  # cache the whole view for 15 minutes
def property_list(request):
    """
    Returns JSON {"data": [...]} where the list is retrieved via the
    low-level caching helper get_all_properties().
    """
    properties = get_all_properties()
    return JsonResponse({"data": properties})
