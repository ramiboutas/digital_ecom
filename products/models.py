from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse


class Category(models.Model):
    # products = models.ManyToManyField('Product', related_name='categories')
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True, help_text='Unique value for product page URL, created from name.')
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    meta_keywords = models.CharField("Meta Keywords", max_length=255, help_text='Comma-delimited set of SEO keywords for meta tag')
    meta_description = models.CharField("Meta Description", max_length=255, help_text='Content for description meta tag')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['title']
        verbose_name_plural = 'Categories'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Category, self).save(*args, **kwargs)

    # general model functions
    def __str__(self):
        return f'{self.title}'

    # url related functions
    def get_absolute_url(self):
        return reverse('products:category_detail', kwargs={'slug' : self.slug})


class Product(models.Model):
    categories = models.ManyToManyField(Category, related_name='products')
    title = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    old_price = models.IntegerField(default=0)
    price = models.PositiveIntegerField(default=500)
    is_free = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_bestseller = models.BooleanField(default=False, help_text="Bestselling products somewhere prominent, like in a side column on every page")
    is_featured = models.BooleanField(default=False, help_text="Which products to show up to the user to present to your user as soon as they arrive at your site")
    featured_as = models.CharField(max_length=10, blank=True, null=True)
    meta_keywords = models.CharField("Meta Keywords",max_length=255, help_text='Comma-delimited set of SEO keywords for meta tag')
    meta_description = models.CharField("Meta Description", max_length=255, help_text='Content for description meta tag')
    slug = models.SlugField(null=True, blank=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    file = models.FileField()

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
        return reverse('cart:create-product-checkout-session', kwargs={'slug' : self.slug})

    def add_to_cart_url(self):
        return reverse('cart:add-to-cart', kwargs={'id' : self.id})

    def create_payment_intent_url(self):
        return reverse('cart:create-product-checkout-session', kwargs={'slug' : self.slug})


class Screenshot(models.Model):
    product = models.ForeignKey(Product, related_name='screenshots', on_delete=models.CASCADE)
    title = models.CharField(max_length=120, blank=True, null=True)
    image = models.ImageField(upload_to='products/screenshots/')

    def __str__(self):
        return f'{self.title}'
