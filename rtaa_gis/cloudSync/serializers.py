from rest_framework import serializers
from .models import GDB, FeatureClass, FeatureDataset,FieldObject,\
    PublisherLog, FeatureLayer, WebMap


class GDBSerializer(serializers.ModelSerializer):

    class Meta:
        model = GDB
        fields = '__all__'

    datasets = serializers.HyperlinkedRelatedField(
        many=True,
        view_name='dataset-detail',
        read_only=True
    )

    def create(self, validated_data):
        return validated_data

    def update(self, instance, validated_data):
        return instance


class FDatasetSerializer(serializers.ModelSerializer):

    class Meta:
        model = FeatureDataset
        fields = '__all__'

    feature_classes = serializers.HyperlinkedRelatedField(
        many=True,
        view_name='fclass-detail',
        read_only=True
    )

    def create(self, validated_data):
        return validated_data

    def update(self, instance, validated_data):
        return instance


class FClassSerializer(serializers.ModelSerializer):

    class Meta:
        model = FeatureClass
        fields = '__all__'

    fields = serializers.HyperlinkedRelatedField(
        many=True,
        view_name='field-detail',
        read_only=True
    )

    def create(self, validated_data):
        return validated_data

    def update(self, instance, validated_data):
        return instance


class FieldSerializer(serializers.ModelSerializer):

    class Meta:
        model = FieldObject
        fields = '__all__'

    def create(self, validated_data):
        return validated_data

    def update(self, instance, validated_data):
        return instance


class FLayerSerializer(serializers.ModelSerializer):

    class Meta:
        model = FeatureLayer
        fields = '__all__'

    def create(self, validated_data):
        return validated_data

    def update(self, instance, validated_data):
        return instance


class WebMapSerializer(serializers.ModelSerializer):

    class Meta:
        model = WebMap
        fields = '__all__'

    def create(self, validated_data):
        return validated_data

    def update(self, instance, validated_data):
        return instance


class PLogSerializer(serializers.ModelSerializer):

    class Meta:
        model = PublisherLog
        fields = '__all__'

    def create(self, validated_data):
        return validated_data

    def update(self, instance, validated_data):
        return instance
