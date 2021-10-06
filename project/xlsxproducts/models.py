from django.db import models


class XlsxProduct(models.Model):
    title = models.CharField(max_length=255)
    purchase_number = models.PositiveIntegerField()
    description = models.TextField()
    file = models.FileField()

    def __str__(self):
        return f"{self.title}"
