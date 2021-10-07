from django.contrib import admin
from .models import XlsxProduct, Screenshot


class ScreenshotInline(admin.StackedInline):
    model = Screenshot
    extra = 1

class XlsxProductAdmin(admin.ModelAdmin):
    model = XlsxProduct
    inlines = [ScreenshotInline,]
    readonly_fields=['slug',]

admin.site.register(XlsxProduct, XlsxProductAdmin)
