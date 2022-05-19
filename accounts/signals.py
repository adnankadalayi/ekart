from . models import Accounts, Referral
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender= Accounts)
def post_save_create_profile(sender, instance, created, *args, **kwargs):
    if created:
        Referral.objects.create(user=instance)