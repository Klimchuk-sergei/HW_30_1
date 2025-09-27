from rest_framework import serializers
from .models import Lesson


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"
        read_only_fields = ("owner",)


class LessonShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ["id", "title"]
