from rest_framework import serializers

from .models import Url, UrlWatchResult


class UrlSerializer(serializers.ModelSerializer):
    class Meta:
        model = Url
        fields = "__all__" # ["creator_uuid", "url", "every", "period",]


class GetUrlSerializer(serializers.ModelSerializer):
    class Meta:
        model = Url
        fields = ["creator_uuid", "url",]


class UrlWatchResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = UrlWatchResult
        fields = "__all__"


class CreatorSerializer(serializers.Serializer):
    """
    Serialize the creator_uuid
    """
    creator_uuid = serializers.UUIDField(format='hex_verbose')
