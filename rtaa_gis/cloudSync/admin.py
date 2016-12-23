from django.contrib import admin
from .models import GDB, FeatureClass, FeatureDataset, PublisherLog

# Register your models here.
admin.site.register(GDB)
admin.site.register(FeatureClass)
admin.site.register(FeatureDataset)
admin.site.register(PublisherLog)
