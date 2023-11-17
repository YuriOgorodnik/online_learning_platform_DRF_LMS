from rest_framework import serializers

from course.models import Course, Lesson, Subscription
from course.validators import validator_scam_url


class LessonSerializer(serializers.ModelSerializer):
    url = serializers.URLField(validators=[validator_scam_url])

    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):
    num_lessons = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True, source="lesson_set")

    class Meta:
        model = Course
        fields = "__all__"

    def get_num_lessons(self, obj):
        return obj.lesson_set.count()


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = "__all__"
