from django.contrib import admin
from .models import Product, Screenshot, ProductFile

class ScreenshotInline(admin.StackedInline):
    model = Screenshot
    extra = 1

class FileInline(admin.StackedInline):
    model = ProductFile
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    model = Product
    inlines = [ScreenshotInline, FileInline]
    readonly_fields=['slug',]

admin.site.register(Product, ProductAdmin)
