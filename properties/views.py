# properties/views.py
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.cache import cache_page

from .models import Property

@cache_page(60 * 15)  # cache the whole view for 15 minutes
def property_list(request):
    """
    Returns a JSON list of all properties.
    Cached in Redis for 15 minutes via django cache backend.
    """
    qs = Property.objects.all().order_by('-created_at').values(
        'id', 'title', 'description', 'price', 'location', 'created_at'
    )
    # values() returns a QuerySet of dicts which JsonResponse can serialize
    return JsonResponse(list(qs), safe=False)
