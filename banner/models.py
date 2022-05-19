from django.db import models

# Create your models here.

class Banner(models.Model):
    image       = models.ImageField(upload_to='photos/banners')
    subtitle    = models.CharField(max_length=20, blank=True, null=True)
    title       = models.CharField(max_length=50)
    price       = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.title