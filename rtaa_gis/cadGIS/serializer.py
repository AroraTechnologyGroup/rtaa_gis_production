from rest_framework import serializers


class MySerializer(serializers.Serializer):
    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

    group = serializers.CharField(max_length=200)
    cad_layer_name = serializers.CharField(max_length=200)
    shape = serializers.CharField(max_length=200)
    status = serializers.CharField(max_length=200)
    repaired = serializers.CharField(max_length=200)
    cad_file_name = serializers.CharField(max_length=200)
