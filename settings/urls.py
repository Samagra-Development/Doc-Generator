from django.contrib import admin
from django.urls import include, path
from django.conf.urls import url
from rest_framework import permissions
from drf_yasg2.views import get_schema_view
from drf_yasg2 import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Doc-Generator",
        default_version='v1',
        description="Doc-Generator API's",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="radhay@samagragovernance.in"),
        license=openapi.License(name="Test License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'', include('pdf.urls')),
    url('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
