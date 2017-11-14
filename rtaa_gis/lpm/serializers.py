from rest_framework import serializers
from rest_framework.reverse import reverse
from rest_framework.fields import CharField
from .models import Agreement, Space
import os


class AgreementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agreement
        fields = '__all__'

    spaces = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='space-detail'
    )

    def create(self, validated_data):
        try:
            _agg = Agreement.objects.create(**validated_data)
            _agg.save()
            return _agg
        except Exception as e:
            print(e)

    def update(self, instance, validated_data):
        try:
            # These variables are brought in from the Access Database of Tiffany
            instance.title = validated_data.get("title", instance.title)
            instance.id = validated_data.get("id", instance.id)
            instance.type = validated_data.get("type", instance.type)
            instance.status = validated_data.get("status", instance.status)
            instance.description = validated_data.get("description", instance.description)
            instance.annual_revenue = validated_data.get("annual_revenue", instance.annual_revenue)
            instance.contact1_name = validated_data.get("contact1_name", instance.contact1_name)
            instance.contact1_phone_number = validated_data.get("contact1_phone_number", instance.contact1_phone_number)
            instance.contact1_address = validated_data.get("contact1_address", instance.contact1_address)
            instance.contact2_name = validated_data.get("contact2_name", instance.contact2_name)
            instance.contact2_phone_number = validated_data.get("contact2_phone_number", instance.contact2_phone_number)
            instance.contact2_address = validated_data.get("contact2_address", instance.contact2_address)
            instance.start_date = validated_data.get("start_date", instance.start_date)
            instance.end_date = validated_data.get("end_date", instance.end_date)
            instance.save()
            return instance
        except Exception as e:
            print(e)


class SpaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Space
        fields = '__all__'
        read_only_fields = ('id',)

    def create(self, validated_data):
        try:
            _space = Space.objects.create(**validated_data)
            _space.save()
            return _space
        except Exception as e:
            print(e)

    def update(self, instance, validated_data):
        try:

            # These variables are brought in from the Access Database of Tiffany
            instance.id = validated_data.get("id", instance.id)
            instance.agreement = validated_data.get("agreement", instance.agreement)
            instance.save()
            return instance
        except Exception as e:
            print(e)

