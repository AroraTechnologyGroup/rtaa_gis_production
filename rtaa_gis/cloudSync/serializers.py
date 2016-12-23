from rest_framework import serializers
from rest_framework.reverse import reverse
from .models import GDB, FeatureClass, FeatureDataset, PublisherLog
import mimetypes
import os


class GDBSerializer(serializers.ModelSerializer):

    class Meta:
        model = GDB
        fields = ('baseName', 'workspaceType', 'catalogPath', 'workspaceFactoryProgID', 'release', 'domains',
                  'currentRelease', 'connectionString')

    def create(self, validated_data):
        return validated_data

    def update(self, instance, validated_data):
        return instance


class FClassSerializer(serializers.ModelSerializer):

    class Meta:
        model = FeatureClass
        fields = ('catalogPath', 'baseName', 'count', 'featureType', 'hasM', 'hasZ', 'hasSpatialIndex',
                  'shapeFieldName', 'shapeType')

    def create(self, validated_data):
        return validated_data

    def update(self, instance, validated_data):
        return instance


class FDatasetSerializer(serializers.ModelSerializer):

    class Meta:
        model = FeatureDataset
        fields = ('baseName', 'changeTracked', 'datasetType', 'isVersioned', 'spatialReference',
                  'children')

    def create(self, validated_data):
        return validated_data

    def update(self, instance, validated_data):
        return instance


class PLogSerializer(serializers.ModelSerializer):

    class Meta:
        model = PublisherLog
        fields = ('serviceName', 'folder', 'timestamp', 'action')

    def create(self, validated_data):
        return validated_data

    def update(self, instance, validated_data):
        return instance
