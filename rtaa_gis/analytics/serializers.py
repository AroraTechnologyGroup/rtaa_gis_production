from rest_framework import serializers
from .models import Record


class RecordSerializer(serializers.ModelSerializer):
    username = serializers.CharField(read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = Record
        fields = ('app_name', 'username', 'method', 'date_time')
