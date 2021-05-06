from django.urls import path

from .views import (
    cms_login_view,
    cms_logout_view,
    home_view,
)

app_name = 'cms'

urlpatterns = [
    path('', cms_login_view, name='cms_login_view'),
    path('logout/', cms_logout_view, name='cms_logout_view'),
    path('dashboard/', home_view, name='cms_home'),
]