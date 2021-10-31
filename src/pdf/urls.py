from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from .views import current_datetime

urlpatterns = [
    path(r'ht/', include('health_check.urls')),
    path('grappelli/', include('grappelli.urls')),  # Admin grappelli URLS
    path('admin/', admin.site.urls),
    path('test-page/', current_datetime),
]
