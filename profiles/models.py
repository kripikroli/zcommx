from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES=((1, "Admin"), (2, "Staff"), (3, "Merchant"), (4, "Customer"))
    user_type=models.IntegerField(choices=USER_TYPE_CHOICES, default=1)

class AdminUser(models.Model):
    profile_pic=models.ImageField(upload_to='avatars', default='no_photo.png')
    auth_user_id=models.OneToOneField(CustomUser, related_name='admin_users', on_delete=models.CASCADE)
    bio=models.TextField(default="no bio...")
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Admin: {self.auth_user_id}"

class StaffUser(models.Model):
    profile_pic=models.ImageField(upload_to='avatars', default='no_photo.png')
    auth_user_id=models.OneToOneField(CustomUser, related_name='staff_users', on_delete=models.CASCADE)
    bio=models.TextField(default="no bio...")
    address_line_1=models.CharField(max_length=255, null=True, blank=True)
    address_line_2=models.CharField(max_length=255, null=True, blank=True)
    address_town=models.CharField(max_length=120, null=True, blank=True)
    address_region=models.CharField(max_length=120, null=True, blank=True)
    address_country=models.CharField(max_length=120, null=True, blank=True)
    address_zip_code=models.CharField(max_length=20, null=True, blank=True)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Staff: {self.auth_user_id}"


class MerchantUser(models.Model):
    profile_pic=models.ImageField(upload_to='avatars', default='no_photo.png')
    auth_user_id=models.OneToOneField(CustomUser, related_name='merchant_users', on_delete=models.CASCADE)
    bio=models.TextField(default="no bio...")
    gst_details=models.CharField(max_length=255, null=True, blank=True)
    address_line_1=models.CharField(max_length=255, null=True, blank=True)
    address_line_2=models.CharField(max_length=255, null=True, blank=True)
    address_town=models.CharField(max_length=120, null=True, blank=True)
    address_region=models.CharField(max_length=120, null=True, blank=True)
    address_country=models.CharField(max_length=120, null=True, blank=True)
    address_zip_code=models.CharField(max_length=20, null=True, blank=True)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Merchant: {self.auth_user_id}"

class CustomerUser(models.Model):
    profile_pic=models.ImageField(upload_to='avatars', default='no_photo.png')
    auth_user_id=models.OneToOneField(CustomUser, related_name='customer_users', on_delete=models.CASCADE)
    address_line_1=models.CharField(max_length=255, null=True, blank=True)
    address_line_2=models.CharField(max_length=255, null=True, blank=True)
    address_town=models.CharField(max_length=120, null=True, blank=True)
    address_region=models.CharField(max_length=120, null=True, blank=True)
    address_country=models.CharField(max_length=120, null=True, blank=True)
    address_zip_code=models.CharField(max_length=20, null=True, blank=True)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Customer: {self.auth_user_id}"
