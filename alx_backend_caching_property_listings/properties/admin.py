from django.contrib import admin

# Register your models here.

from .models import Property

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('title', 'location', 'price', 'created_at')
    search_fields = ('title', 'location')
    list_filter = ('created_at',)
    ordering = ('-created_at',)
admin.site.site_header = "Property Listings Admin"
admin.site.site_title = "Property Listings Admin Portal"
admin.site.index_title = "Welcome to the Property Listings Admin Portal"
