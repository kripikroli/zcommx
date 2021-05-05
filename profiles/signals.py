from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import CustomUser, AdminUser, StaffUser, MerchantUser, CustomerUser

@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.user_type==1:
            AdminUser.objects.create(auth_user_id=instance)
        if instance.user_type==2:
            StaffUser.objects.create(auth_user_id=instance)
        if instance.user_type==3:
            MerchantUser.objects.create(auth_user_id=instance)
        if instance.user_type==4:
            CustomerUser.objects.create(auth_user_id=instance)

@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if instance.user_type==1:
        instance.admin_users.save()
    if instance.user_type==2:
        instance.staff_users.save()
    if instance.user_type==3:
        instance.merchant_users.save()
    if instance.user_type==4:
        instance.customer_users.save()
