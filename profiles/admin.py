from django.contrib import admin
from .models import CustomUser, AdminUser, StaffUser, MerchantUser, CustomerUser

admin.site.register(CustomUser)
admin.site.register(AdminUser)
admin.site.register(StaffUser)
admin.site.register(MerchantUser)
admin.site.register(CustomerUser)