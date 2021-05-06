from django.contrib import admin
from .models import (
    Category,
    SubCategory,
    Product,
    ProductImage,
    ProductDetail,
    ProductAbout,
    ProductVariant,
    ProductVariantItem
)

admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(ProductDetail)
admin.site.register(ProductAbout)
admin.site.register(ProductVariant)
admin.site.register(ProductVariantItem)