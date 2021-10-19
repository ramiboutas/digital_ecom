from django.contrib import admin
from .models import Product, Screenshot, ProductFile, Category

class CategoryAdmin(admin.ModelAdmin):
    model = Category
    # inlines =
    readonly_fields = ['slug',]

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
    search_fields = ['title', 'description', 'meta_keywords', 'meta_description']
    exclude = ('created_at', 'updated_at',)
    ordering = ['-created_at']
    # prepopulated_fields = {'slug' : ('title',)}

admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
