from rest_framework import serializers
from .models import GDB, FeatureClass, FeatureDataset, FieldObject,\
    PublisherLog, FeatureLayer, WebMap, DomainValues


class BuilderSerializer(serializers.Serializer):
    gdb = serializers.CharField(
        max_length=255,
        required=True
    )
    dataset = serializers.CharField(
        max_length=100,
        required=False,
        allow_blank=True
    )
    featureClass = serializers.CharField(
        max_length=100,
        required=False,
        allow_blank=True
    )
    field = serializers.CharField(
        max_length=100,
        required=False,
        allow_blank=True
    )


class GDBSerializer(serializers.ModelSerializer):

    class Meta:
        model = GDB
        fields = '__all__'

    datasets = serializers.HyperlinkedRelatedField(
        many=True,
        queryset=FeatureDataset.objects.all(),
        view_name='dataset-detail',
        read_only=False,
        required=False
    )

    domains = serializers.HyperlinkedRelatedField(
        many=True,
        queryset=DomainValues.objects.all(),
        view_name='domain-detail',
        read_only=False,
        required=False
    )

    connection_string = serializers.CharField(allow_blank=True)

    def create(self, validated_data):
        return GDB.objects.create(**validated_data)

    def update(self, instance, validated_data):
        return instance


class DomainSerializer(serializers.ModelSerializer):

    class Meta:
        model = DomainValues
        fields = '__all__'

    fields = serializers.HyperlinkedRelatedField(
        many=True,
        view_name='field-detail',
        read_only=True,
        allow_null=True
    )

    def create(self, validated_data):
        return DomainValues.objects.create(**validated_data)

    def update(self, instance, validated_data):
        return instance


class FDatasetSerializer(serializers.ModelSerializer):

    class Meta:
        model = FeatureDataset
        fields = '__all__'

    feature_classes = serializers.HyperlinkedRelatedField(
        many=True,
        queryset=FeatureClass.objects.all(),
        view_name='fclass-detail',
        read_only=False,
        required=False
    )

    gcs_name = serializers.CharField(allow_blank=True)
    gcs_code = serializers.CharField(allow_blank=True)

    def create(self, validated_data):
        return FeatureDataset.objects.create(**validated_data)

    def update(self, instance, validated_data):
        return instance


class FClassSerializer(serializers.ModelSerializer):

    class Meta:
        model = FeatureClass
        fields = '__all__'

    fields = serializers.HyperlinkedRelatedField(
        many=True,
        queryset=FieldObject.objects.all(),
        view_name='field-detail',
        read_only=False,
        required=False
    )

    def create(self, validated_data):
        return FeatureClass.objects.create(**validated_data)

    def update(self, instance, validated_data):
        return instance


class FieldSerializer(serializers.ModelSerializer):

    class Meta:
        model = FieldObject
        fields = '__all__'

    default_value = serializers.CharField(allow_null=True)

    def create(self, validated_data):
        return FieldObject.objects.create(**validated_data)

    def update(self, instance, validated_data):
        return instance


class FLayerSerializer(serializers.ModelSerializer):

    class Meta:
        model = FeatureLayer
        fields = '__all__'

    def create(self, validated_data):
        return FeatureLayer.objects.create(**validated_data)

    def update(self, instance, validated_data):
        return instance


class WebMapSerializer(serializers.ModelSerializer):

    class Meta:
        model = WebMap
        fields = '__all__'

    def create(self, validated_data):
        return WebMap.objects.create(**validated_data)

    def update(self, instance, validated_data):
        return instance


class PLogSerializer(serializers.ModelSerializer):

    class Meta:
        model = PublisherLog
        fields = '__all__'

    def create(self, validated_data):
        return PublisherLog.objects.create(**validated_data)

    def update(self, instance, validated_data):
        return instance
