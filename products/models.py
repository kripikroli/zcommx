from django.db import models
from profiles.models import MerchantUser
from django.urls import reverse

class Category(models.Model):
    name=models.CharField(max_length=255)
    slug=models.SlugField()
    thumbnail=models.ImageField(upload_to='category_thumbnails', default='no_image.png')
    description=models.TextField(default='description here...')
    is_active=models.IntegerField(default=1)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse("cms:category_list_view")

    def __str__(self):
        return f"{self.name}"

class SubCategory(models.Model):
    name=models.CharField(max_length=255)
    slug=models.SlugField()
    thumbnail=models.ImageField(upload_to='category_thumbnails', default='no_image.png')
    description=models.TextField(default='description here...')
    is_active=models.IntegerField(default=1)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    category_id=models.ForeignKey(Category, related_name='subcategories', on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse("cms:sub_category_list_view")

    def __str__(self):
        return f"{self.name}"


class Product(models.Model):
    name=models.CharField(max_length=255)
    slug=models.SlugField()
    short_description=models.TextField(default='description here...')
    long_description=models.TextField(default='description here...')
    brand=models.CharField(max_length=255, blank=True, null=True)
    price=models.FloatField(help_text='in US dollars $')
    is_active=models.IntegerField(default=1)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    subcategory_id=models.ForeignKey(SubCategory, default=1, related_name='products_subcategory', on_delete=models.CASCADE)
    merchant_id=models.ForeignKey(MerchantUser, related_name='products_merchant', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}"

class ProductImage(models.Model):
    image=models.ImageField(upload_to='products', blank=True)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    product_id=models.ForeignKey(Product, related_name='product_images', on_delete=models.CASCADE)


class ProductMedia(models.Model):
    MEDIA_TYPE_CHOICES=((1,"Image"),(2,"Video"))
    media_type=models.IntegerField(choices=MEDIA_TYPE_CHOICES, default=1)
    media_content=models.FileField(upload_to='products')
    is_active=models.IntegerField(default=1)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    product_id=models.ForeignKey(Product, related_name='product_medias', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.created}"

class ProductDetail(models.Model):
    title=models.CharField(max_length=255, null=True, blank=True)
    details=models.CharField(max_length=255, null=True, blank=True)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    product_id=models.ForeignKey(Product, related_name='product_details', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title}"

class ProductAbout(models.Model):
    title=models.CharField(max_length=255, null=True, blank=True)
    details=models.CharField(max_length=255, null=True, blank=True)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    product_id=models.ForeignKey(Product, related_name='product_abouts', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title}"

class ProductVariant(models.Model):
    title=models.CharField(max_length=255, null=True, blank=True)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title}"

class ProductVariantItem(models.Model):
    name=models.CharField(max_length=255, blank=True, null=True)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    product_id=models.ForeignKey(Product, related_name='product_variant_items', on_delete=models.CASCADE)
    product_variant_id=models.ForeignKey(ProductVariant, related_name='variants', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}"

class ProductTag(models.Model):
    tag=models.CharField(max_length=120)
    product_id=models.ForeignKey(Product, related_name='product_tags', on_delete=models.CASCADE)


class ProductTransaction(models.Model):
    TRANSACTION_TYPE_CHOICES=((1,"BUY"),(2,"SELL"),(3,"SETUP"))
    transaction_type=models.IntegerField(choices=TRANSACTION_TYPE_CHOICES, default=1)
    transaction_product_count=models.IntegerField(default=1)
    transaction_description=models.CharField(max_length=255)
    created=models.DateTimeField(auto_now_add=True)
    product_id=models.ForeignKey(Product, related_name='product_transactions', on_delete=models.CASCADE)