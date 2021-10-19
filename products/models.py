from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse

class Category(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True, help_text='Unique value for product page URL, created from name.')
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    meta_keywords = models.CharField("Meta Keywords",max_length=255, help_text='Comma-delimited set of SEO keywords for meta tag')
    meta_description = models.CharField("Meta Description", max_length=255, help_text='Content for description meta tag')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # general model functions
    def __str__(self):
        return f'{self.title}'

    # url related functions
    def get_absolute_url(self):
        return reverse('products:category_list', kwargs={'slug' : self.slug})


class Product(models.Model):
    categories = models.ManyToManyField(Category, related_name='products')
    title = models.CharField(max_length=255, unique=True)
    old_price = models.IntegerField(default=0)
    price = models.IntegerField(default=0)
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    meta_keywords = models.CharField("Meta Keywords",max_length=255, help_text='Comma-delimited set of SEO keywords for meta tag')
    meta_description = models.CharField("Meta Description", max_length=255, help_text='Content for description meta tag')
    slug = models.SlugField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # general model functions
    def __str__(self):
        return f'{self.title}'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Product, self).save(*args, **kwargs)

    # instance related functions
    def sale_price(self):
        if self.old_price > self.price:
            return self.price
        else:
            return None

    # url related functions
    def get_display_price(self):
        return "{0:.2f}".format(self.price / 100)

    def buy_product_url(self):
        return reverse('carts:create-product-checkout-session', kwargs={'slug' : self.slug})

    def create_payment_intent_url(self):
        return reverse('carts:create-product-checkout-session', kwargs={'slug' : self.slug})


class ProductFile(models.Model):
    product = models.ForeignKey(Product, related_name='files', on_delete=models.CASCADE)
    file = models.FileField()

    def get_absolute_url(self):
        pass


class Screenshot(models.Model):
    product = models.ForeignKey(Product, related_name='screenshots', on_delete=models.CASCADE)
    title = models.CharField(max_length=120, blank=True, null=True)
    image = models.ImageField(upload_to='products/screenshots/')

    def __str__(self):
        return f'{self.title}'
