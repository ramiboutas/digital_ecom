from django.db import models
from django.template.defaultfilters import slugify

class XlsxProduct(models.Model):
    title = models.CharField(max_length=255, unique=True)
    purchase_number = models.PositiveIntegerField()
    description = models.TextField()
    file = models.FileField()
    slug = models.SlugField(null=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(XlsxProduct, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.title}'


class Screenshot(models.Model):
    product = models.ForeignKey(XlsxProduct, related_name='xlsxproducts', on_delete=models.CASCADE)
    title = models.CharField(max_length=120, blank=True, null=True)
    image = models.ImageField(upload_to='xlsxproducts/screenshots/')

    def __str__(self):
        return f'{self.title}'
