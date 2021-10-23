from django.contrib import admin

from .models import Item

class ItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'cart_id']

admin.site.register(Item, ItemAdmin)
