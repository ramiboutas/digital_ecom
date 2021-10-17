from django.db import models
from django.template.defaultfilters import slugify



class Product(models.Model):
    title = models.CharField(max_length=255, unique=True)
    price = models.IntegerField(default=0)
    type =  models.CharField(max_length=20)
    description = models.TextField()
    slug = models.SlugField(null=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.title}'

    def get_display_price(self):
        return "{0:.2f}".format(self.price / 100)

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
