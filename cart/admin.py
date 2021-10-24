from django.contrib import admin

from .models import Item, Cart

class ItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'cart_id']


class ItemInline(admin.StackedInline):
    model = Item


class CartAdmin(admin.ModelAdmin):
    model = Cart
    inlines = [ItemInline, ]
    readonly_fields=['cookie_value',]
    search_fields = ['cookie_value']


admin.site.register(Item, ItemAdmin)
admin.site.register(Cart, CartAdmin)
