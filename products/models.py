from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse

class AbstractProduct(models.Model):
    title = models.CharField(max_length=255, unique=True)
    price = models.IntegerField(default=0)
    type =  models.CharField(max_length=20)
    description = models.TextField()
    slug = models.SlugField(null=True, blank=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Product, self).save(*args, **kwargs)

class XlsxProduct(AbstractProduct):
    year_versions = models.CharField(max_length=255) # implement: multiple choices!

    def __str__(self):
        return f'{self.title}'

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
