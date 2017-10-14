from rest_framework import serializers
from rest_framework.reverse import reverse
from .models import AgreementModel
import os


class AgreementSerializer(serializers.ModelSerializer):

    class Meta:
        model = AgreementModel
        fields = ('id', 'title', 'type', 'description', 'annual_revenue', 'contact1_name', 'contact1_phone_number', 'contact1_address',
                  'contact2_name', 'contact2_phone_number', 'contact2_address', 'start_date', 'end_date')

    def create(self, validated_data):
        try:

            _agg = AgreementModel.objects.create(**validated_data)
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
