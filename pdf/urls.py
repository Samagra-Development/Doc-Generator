from django.urls import path
from . import views

urlpatterns = [
    path('api/v3/pdfDoc', views.generate_pdf, name='getData'),
]