from django.db import models

# Create your models here.
from django.db import models
from django.contrib.postgres.fields import JSONField, ArrayField
from fernet_fields import EncryptedTextField

# Base model for adding creation and update date to other models
class BaseModel(models.Model):
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        abstract = True


class GenericConfig(BaseModel):
    id = models.BigIntegerField(unique=True, primary_key=True)
    name = models.CharField(max_length=20)
    data = EncryptedTextField()  # json.dumps output (json.loads needed to get the data)
    retries = models.IntegerField(default=0)
    max_concurrency = models.IntegerField(default=1)

    class Meta:
        db_table = 'GenericConfig'

    def get_uploader(self):
        pass

    def get_shortener(self):
        pass


class Pdf(BaseModel):
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
        ('PDF Building', 'PDF Building'),
        ('Uploading', 'Uploading'),
        ('URL Shortening', 'URL Shortening'),
        ('Deleted From Drive', 'Deleted From Drive'),
    ]

    config = models.ForeignKey(GenericConfig, on_delete=models.CASCADE, null=True, default=None)

    id = models.UUIDField(unique=True, primary_key=True)
    meta = JSONField(blank=True, null=True)
    data = JSONField(blank=True, null=True)
    tags = ArrayField(models.CharField(max_length=20, blank=True), null=True)

    # PDF URL Management
    url = models.CharField(max_length=200, blank=True)
    url_meta = models.JSONField()
    url_expiry = models.DateTimeField(null=True)
    short_url = models.CharField(max_length=50, blank=True)

    # Queue Progress
    status = models.CharField(max_length=20, choices=Q_STATUS_CHOICES, default='Queued')
    step = models.CharField(max_length=30, choices=STEP_CHOICES, default='Not Started')
    tries = models.IntegerField(default=0)

    version = models.CharField(max_length=5)

    class Meta:
        db_table = 'Pdf'

