from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.db.models import JSONField
import datetime
from fernet_fields import EncryptedTextField


# Base model for adding creation and update date to other models
class BaseModel(models.Model):
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        abstract = True


class GenericConfig(BaseModel):
    UPLOADERS = [
        ('minio', 'Minio'),
    ]
    SHORTENERS = [
        ('yaus', 'YAUS'),
    ]
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    data = EncryptedTextField()  # json.dumps output (json.loads needed to get the data)
    uploader_ref = models.CharField(choices=UPLOADERS, null=True, blank=True, max_length=20)
    shortener_ref = models.CharField(choices=SHORTENERS, null=True, blank=True, max_length=20)
    retries = models.IntegerField(default=0)
    max_concurrency = models.IntegerField(default=1)

    class Meta:
        db_table = 'GenericConfig'
        verbose_name = "Generic Config"
        verbose_name_plural = "Generic Configs"
        app_label = 'pdf'

    def serialize(self):
        __dict__ = {
            "id": self.id,
            "name": self.name,
            "data": self.data,
            "uploader_ref": self.uploader_ref,
            "shortener_ref": self.shortener_ref,
            "retries": self.retries,
            "max_concurrency": self.max_concurrency
        }

    def get_uploader(self):
        pass

    def get_shortener(self):
        pass


class Doc(BaseModel):
    Q_STATUS_CHOICES = [
        ('Queued', 'Queued'),
        ('Processing', 'Processing'),
        ('Failed', 'Failed'),
        ('Complete', 'Complete'),
        ('Error', 'Error'),
    ]

    STEP_CHOICES = [
        ('Not Started', 'Not Started'),
        ('Data Fetching', 'Data Fetching'),
        ('Mapping Fetching', 'Mapping Fetching'),
        ('Template Processing', 'Template Processing'),
        ('Doc Building', 'Doc Building'),
        ('Uploading', 'Uploading'),
        ('URL Shortening', 'URL Shortening'),
        ('Completed', 'Completed'),
    ]

    config = models.ForeignKey(GenericConfig, on_delete=models.CASCADE, null=True, default=None)

    id = models.UUIDField(unique=True, primary_key=True)
    meta = JSONField(blank=True, null=True)
    data = JSONField(blank=True, null=True)
    tags = ArrayField(models.CharField(max_length=20, blank=True), null=True)
    isActive = models.BooleanField(default=True, blank=True, null=True)
    plugin = models.CharField(max_length=50, null=True, blank=True)

    # PDF URL Management
    url = models.CharField(max_length=255, null=True, blank=True)
    url_meta = models.JSONField(null=True, blank=True)
    url_expiry = models.DateTimeField(null=True)
    short_url = models.CharField(max_length=255, blank=True)

    # Queue Progress
    status = models.CharField(max_length=20, choices=Q_STATUS_CHOICES, default='Queued')
    step = models.CharField(max_length=30, choices=STEP_CHOICES, default='Not Started')
    tries = models.IntegerField(default=0)

    version = models.CharField(max_length=5, default="1.0.0")
    retry = models.BooleanField(default=True, null=True, blank=True)

    class Meta:
        db_table = 'Doc'
        verbose_name = "DOC"
        verbose_name_plural = "DOCs"
        app_label = 'pdf'

    def serialize(self):
        __dict__ = {
            "id": self.id,
            "meta": self.meta,
            "data": self.data,
            "tags": self.tags,
            "isActive": self.isActive,
            "plugin": self.plugin,
            "url": self.url,
            "url_meta": self.url_meta,
            "url_expiry": self.url_expiry,
            "short_url": self.short_url,
            "status": self.status,
            "step": self.step,
            "retry": self.retry,
            "tries": self.tries,
            "version": self.version,
        }
        return __dict__


class Audit(BaseModel):
    _Q_EVENT_CHOICES = [
        ('Queued', 'Queued'),
        ('Processing', 'Processing'),
        ('Failed', 'Failed'),
        ('Complete', 'Complete'),
        ('Error', 'Error'),
        ('None', 'None'),
    ]
    id = models.BigIntegerField(unique=True, primary_key=True)
    pdf = models.ForeignKey(Doc, on_delete=models.CASCADE, null=True, default=None)
    status = models.CharField(max_length=20, choices=_Q_EVENT_CHOICES, default='None')
    stacktrace = models.JSONField(null=True)

    class Meta:
        db_table = 'Audit'
        verbose_name = "Audit"
        verbose_name_plural = "Audits"
        app_label = 'pdf'
