from django.contrib import admin
from .models import (
    Category,
    SubCategory,
    Product,
    ProductImage,
    ProductMedia,
    ProductDetail,
    ProductAbout,
    ProductVariant,
    ProductVariantItem,
    ProductTag,
    ProductTransaction,
)

admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(ProductMedia)
admin.site.register(ProductDetail)
admin.site.register(ProductAbout)
admin.site.register(ProductVariant)
admin.site.register(ProductVariantItem)
admin.site.register(ProductTag)
admin.site.register(ProductTransaction)