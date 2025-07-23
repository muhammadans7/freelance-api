from rest_framework import serializers

class Start2FASerializer(serializers.Serializer):
    pass


class Verify2FASerializer(serializers.Serializer):
    token = serializers.CharField(min_length=6 ,max_length=6)