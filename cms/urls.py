from django.urls import path

from .views import (

    home_view,

    cms_login_view,
    cms_logout_view,

    CategoryListView,
    CategoryCreateView,
    CategoryUpdateView,

    SubCategoryListView,
    SubCategoryCreateView,
    SubCategoryUpdateView,

    UserMerchantListView,
    UserMerchantCreateView,
    UserMerchantUpdateView,
    
    ProductListView,
    ProductCreateView,
)

app_name = 'cms'

urlpatterns = [

    # Login
    path('', cms_login_view, name='cms_login_view'),
    path('logout/', cms_logout_view, name='cms_logout_view'),

    # Dashboard
    path('dashboard/', home_view, name='cms_home'),

    # Categories
    path('dashboard/category_list', CategoryListView.as_view(), name='category_list_view'),
    path('dashboard/category_create', CategoryCreateView.as_view(), name='category_create_view'),
    path('dashboard/category_update/<slug:pk>', CategoryUpdateView.as_view(), name='category_update_view'),

    # SubCategories
    path('dashboard/sub_category_list', SubCategoryListView.as_view(), name='sub_category_list_view'),
    path('dashboard/sub_category_create', SubCategoryCreateView.as_view(), name='sub_category_create_view'),
    path('dashboard/sub_category_update/<slug:pk>', SubCategoryUpdateView.as_view(), name='sub_category_update_view'),

    # Merchants
    path('dashboard/user_merchant_list', UserMerchantListView.as_view(), name='user_merchant_list_view'),
    path('dashboard/user_merchant_create', UserMerchantCreateView.as_view(), name='user_merchant_create_view'),
    path('dashboard/user_merchant_update/<slug:pk>', UserMerchantUpdateView.as_view(), name='user_merchant_update_view'),

    # Products
    path('dashboard/product_list', ProductListView.as_view(),name="product_list_view"),
    path('dashboard/product_create', ProductCreateView.as_view(),name="product_create_view"),
]