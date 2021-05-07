from django.urls import path

from .views import (
    cms_login_view,
    cms_logout_view,
    home_view,
    CategoryListView,
    CategoryCreateView,
    CategoryUpdateView,
    SubCategoryListView,
    SubCategoryCreateView,
    SubCategoryUpdateView
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

]