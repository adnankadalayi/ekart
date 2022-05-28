from django.db import models
from cloudinary.models import CloudinaryField

class Banner(models.Model):
    image       = CloudinaryField('image')
    subtitle    = models.CharField(max_length=20, blank=True, null=True)
    title       = models.CharField(max_length=50)
    price       = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.title