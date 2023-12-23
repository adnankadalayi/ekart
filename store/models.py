from django.db import models
from category.models import Category
from django.urls import reverse
from django.utils.text import slugify
from django.core.validators import MaxValueValidator, MinValueValidator

class Product(models.Model):
    product_name    = models.CharField(max_length=50)
    slug            = models.SlugField(max_length=50)
    description     = models.TextField(max_length=2000, blank=True)
    price           = models.DecimalField(max_digits=8, decimal_places=2)
    product_img_0   = models.ImageField(upload_to='photos/products')
    product_img_1   = models.ImageField(upload_to='photos/products')
    product_img_2   = models.ImageField(upload_to='photos/products')
    product_img_3   = models.ImageField(upload_to='photos/products')
    stock           = models.IntegerField()
    category        = models.ForeignKey(Category, on_delete= models.CASCADE)
    is_available    = models.BooleanField(default= True)
    is_trending     = models.BooleanField(default= False)
    created_date    = models.DateTimeField(auto_now_add=True)
    modified_date   = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.product_name
        
    # pass slug through url 
    def get_url(self):
        return reverse('product_detail', args=[self.category.slug, self.slug])


    # #to change auto update the slug --- not recommended
    # def save(self, *args, **kwargs):
    #     self.slug = slugify(self.product_name)
    #     super().save(*args, **kwargs)

class CategoryOffer(models.Model):
    category = models.OneToOneField(Category, related_name='cate_offers', on_delete=models.CASCADE)
    discount = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(75)])
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()

    def __str__(self):
        return self.category.category_name
    
class ProductOffer(models.Model):
    product = models.OneToOneField(Product, related_name='prod_offers', on_delete=models.CASCADE)
    discount = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(75)])
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()

    def __str__(self):
        return self.product.product_name
    