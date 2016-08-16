from rest_framework import serializers


class WebApplicationSerializer(serializers.Serializer):
    """format the data retrieved from AGOL before returning
    it to the client side application"""
    title = serializers.CharField(max_length=200)
    url = serializers.CharField(max_length=200)

