from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from .utils import generate_ref_code

class MyAccountManager(BaseUserManager):
    
    #create user with f.name, l.name, username set password and save user 
    def create_user(self, first_name, last_name, email, username, password=None):
        if not email:
            raise ValueError('User must have an email')
        
        if not username:
            raise ValueError('User must have an username')
        
        user = self.model(
            email=self.normalize_email(email),
            first_name = first_name,
            last_name  = last_name,
            username   = username,
        )

        user.set_password(password)
        user.save(using=self.db)
        return user
     
     # superuser
    def create_superuser(self, first_name, email, last_name, username, password):
        user = self.model(
            email       = self.normalize_email(email),
            first_name  = first_name,
            last_name   = last_name,
            username    = username,
            password    = password,

        )

        user.is_staff       = True
        user.is_admin       = True
        user.is_superadmin  = True
        user.is_active      = True

        user.save(using=self._db)
        return user
     
#account model 
class Accounts(AbstractBaseUser):
    first_name = models.CharField( max_length=50)
    last_name  = models.CharField(max_length=50)
    email      = models.EmailField(max_length=100, unique=True)
    username   = models.CharField(max_length=50,unique=True)
    phone_no   = models.CharField( max_length=10, unique=True, null=True)

    # mandatory field

    is_active       = models.BooleanField(default=False)
    is_staff        = models.BooleanField(default=False)
    is_superadmin   = models.BooleanField(default=False)
    is_admin        = models.BooleanField(default=False)
    date_joined     = models.DateTimeField(auto_now_add=True)
    last_login      = models.DateTimeField(auto_now_add=True)

    #email field in username
    # changed to username field
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    #telling its objects on MyAccountManager
    objects = MyAccountManager()

    #str form of model
    def __str__(self):  
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, add_label):
        return True

    def full_name(self):                                                       
        return f'{self.first_name} {self.last_name}' 
   



    #changing name
    class Meta:
        verbose_name = 'Account'
        verbose_name_plural = 'Accounts'

# model for addresses 
class  Address(models.Model):
    user            = models.ForeignKey(Accounts, on_delete=models.CASCADE)
    first_name      = models.CharField(max_length=50)
    last_name       = models.CharField(max_length=50)
    phone_no        = models.CharField(max_length=10)
    email           = models.EmailField()
    address_line_1  = models.CharField(max_length=50)
    address_line_2  = models.CharField(max_length=50, blank=True)
    country         = models.CharField(max_length=50)
    state           = models.CharField(max_length=50)
    city            = models.CharField(max_length=50)
    pin             = models.PositiveIntegerField()

    def __str__(self):
        return self.first_name

class Referral(models.Model):
    user = models.OneToOneField(Accounts, on_delete=models.CASCADE)
    code = models.CharField(max_length=12, blank=True)
    recommended_by = models.ForeignKey(Accounts, on_delete=models.CASCADE, blank=True, null=True, related_name= 'ref_by') 
    updated_at = models.DateTimeField(auto_now= True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}-{self.code}"

    def get_recommended_profiles(self):
        refs = Referral.objects.all()
        my_recommends = []
        for profile in refs:
            if profile.recommended_by == self.user:
                my_recommends.append(profile)
        return my_recommends
    def get_your_refer_code(self):
        return self.code

    def save(self, *args, **kwargs):
        if self.code == "":
            code  = generate_ref_code()
            self.code = code
        super().save(*args, **kwargs)
    
