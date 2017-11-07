from rest_framework import serializers
from rest_framework.reverse import reverse
from rest_framework.fields import CharField
from .models import Agreement, Space
import os


class AgreementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agreement
        fields = ('id', 'title', 'type', 'description', 'annual_revenue', 'contact1_name', 'contact1_phone_number', 'contact1_address',
                  'contact2_name', 'contact2_phone_number', 'contact2_address', 'start_date', 'end_date')

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
        fields = ('id', 'agreement', 'tenant', 'type', 'gis_area', 'leased_area',
                  'notes', 'start_date', 'end_date')
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
            instance.tenant = validated_data.get("tenant", instance.tenant)
            instance.type = validated_data.get("type", instance.type)
            instance.gis_area = validated_data.get("gis_area", instance.gis_area)
            instance.leased_area = validated_data.get("leased_area", instance.leased_area)
            instance.notes = validated_data.get("notes", instance.notes)
            instance.start_date = validated_data.get("start_date", instance.start_date)
            instance.end_date = validated_data.get("end_date", instance.end_date)
            instance.save()
            return instance
        except Exception as e:
            print(e)

