from django.db import models


class GDB(models.Model):
    def __unicode__(self):
        return "%s" % self.baseName

    class Meta:
        ordering = ('workspaceType',)
        app_label = 'cloudSync'

    baseName = models.CharField(max_length=255)

    catalogPath = models.CharField(max_length=255, unique=True)

    workspaceType = models.CharField(max_length=25)

    workspaceFactoryProgID = models.CharField(max_length=255)

    release = models.CharField(max_length=255)

    domains = models.CharField(max_length=255)

    currentRelease = models.CharField(max_length=255)

    connectionString = models.CharField(max_length=255)


class FeatureClass(models.Model):

    def __unicode__(self):
        return "%s" % self.baseName

    class Meta:
        ordering = ('baseName', )
        app_label = 'cloudSync'

    catalogPath = models.CharField(max_length=255, unique=True)

    baseName = models.CharField(max_length=255)

    count = models.IntegerField(null=True)

    featureType = models.CharField(max_length=25)

    hasM = models.CharField(max_length=2)

    hasZ = models.CharField(max_length=2)

    hasSpatialIndex = models.CharField(max_length=2)

    shapeFieldName = models.CharField(max_length=25)

    shapeType = models.CharField(max_length=25)


class FeatureDataset(models.Model):
    def __unicode__(self):
        return "%s" % self.baseName

    class Meta:
        ordering = ('baseName',)
        app_label = 'cloudSync'

    baseName = models.CharField(max_length=50, unique=True)

    changeTracked = models.CharField(max_length=2)

    datasetType = models.CharField(max_length=25)

    isVersioned = models.CharField(max_length=2)

    spatialReference = models.CharField(max_length=255)

    children = models.CharField(max_length=255)


class PublisherLog(models.Model):
    def __unicode__(self):
        return "%s" % self.serviceName

    class Meta:
        ordering = ('timestamp',)
        app_label = 'cloudSync'

    PUB_ACTIONS = (
        ('New', 'New'),
        ('R', 'Replace'),
        ('D', 'Drop')
    )
    serviceName = models.CharField(max_length=255)

    folder = models.CharField(max_length=25)

    timestamp = models.DateField(auto_now=True)

    action = models.CharField(max_length=3, choices=PUB_ACTIONS)
