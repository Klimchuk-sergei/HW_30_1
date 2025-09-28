from rest_framework import serializers
from .models import Course
from lesson.serializers import LessonShortSerializer


class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField(read_only=True)
    lessons = LessonShortSerializer(many=True, read_only=True)  # Убрали source="lessons"

    class Meta:
        model = Course
        fields = "__all__"
        read_only_fields = ('owner',)

    def get_lessons_count(self, obj):
        return obj.lessons.count()
