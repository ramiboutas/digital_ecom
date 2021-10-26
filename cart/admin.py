from django.contrib import admin
from django.contrib.sessions.models import Session

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


class SessionAdmin(admin.ModelAdmin):
    def _session_data(self, obj):
        return obj.get_decoded()
    list_display = ['session_key', '_session_data', 'expire_date']

admin.site.register(Session, SessionAdmin)


admin.site.register(Item, ItemAdmin)
admin.site.register(Cart, CartAdmin)
