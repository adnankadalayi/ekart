from django.db import models
from django.urls import reverse
# from django.utils.text import slugify


# Create your models here.

class Category(models.Model):
    category_name   = models.CharField(max_length=50, unique=True)
    slug            = models.SlugField(max_length=50, unique=True )
    category_img    = models.ImageField(upload_to='photos/categories')


    class Meta:
        verbose_name        = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.category_name
    
    #to get url and pass slug 
    def get_url(self):
        return reverse('products_by_category', args=[self.slug])

    #to change auto update the slug --- not recommended
    # def save(self, *args, **kwargs):
    #     self.slug = slugify(self.category_name)
    #     super().save(*args, **kwargs)