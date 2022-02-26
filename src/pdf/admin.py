from django.contrib import admin

from .models import Audit, Doc, GenericConfig


class AuditAdmin(admin.ModelAdmin):
    fields = ['id', 'status', 'pdf']


class DocAdmin(admin.ModelAdmin):
    fields = ["id", "meta", "data", "tags", "url", "url_meta", "url_expiry", "short_url", "status", "step", "tries", "version"]


class GenericConfigAdmin(admin.ModelAdmin):
    fields = ['name', 'data', 'uploader_ref', 'shortener_ref', 'retries', 'max_concurrency']


admin.site.register(Doc, DocAdmin)
admin.site.register(Audit, AuditAdmin)
admin.site.register(GenericConfig, GenericConfigAdmin)

