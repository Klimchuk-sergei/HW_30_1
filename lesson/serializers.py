from rest_framework import serializers
from .models import Lesson


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"
        read_only_fields = ("owner",)

    def validate_video_file(self, value):
        """валидация поля ссылки, проверяем что ссылка на youtube"""
        if value:
            if "youtube.com" not in value and "youtu.be" not in value:
                raise serializers.ValidationError("Допустимы только youtube ссылки")

            if not value.startswith(("http://", "https://")):
                raise serializers.ValidationError(
                    "Ссылка должна начинаться с http:// или https://"
                )

        return value


class LessonShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ["id", "title"]
