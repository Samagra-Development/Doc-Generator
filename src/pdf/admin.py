from django.contrib import admin

from .models import Audit, Pdf


class AuditAdmin(admin.ModelAdmin):
    fields = ['id', 'status', 'pdf']


class PdfAdmin(admin.ModelAdmin):
    fields = ['id', 'status', 'tries']


admin.site.register(Audit, AuditAdmin)
admin.site.register(Pdf, PdfAdmin)
