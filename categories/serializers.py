from rest_framework import serializers
from .models import Category, Icon


class IconSerializer(serializers.ModelSerializer):

    class Meta:
        model = Icon
        fields = [
            "id",
            "title",
            "icon_code",
            ]


class CategorySerializer(serializers.ModelSerializer):
    icon = IconSerializer(read_only=True)

    class Meta:
        model = Category
        fields = [
            "id",
            "title",
            "description",
            "icon",
            "slug",
            ]
