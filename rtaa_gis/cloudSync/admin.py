from django.contrib import admin
from .models import GDB, FeatureClass, FeatureDataset, PublisherLog, FeatureLayer,\
    WebMap, FieldObject, DomainValues

# Register your models here.
admin.site.register(GDB)
admin.site.register(DomainValues)
admin.site.register(FeatureClass)
admin.site.register(FeatureDataset)
admin.site.register(FieldObject)
admin.site.register(PublisherLog)
admin.site.register(FeatureLayer)
admin.site.register(WebMap)
