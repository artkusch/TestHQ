from rest_framework import serializers
from .models import Lesson
from user.models import UserLessonProgress


class UserLessonProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserLessonProgress
        fields = ('watched', 'watch_time')


class LessonSerializer(serializers.ModelSerializer):
    watch_time = serializers.IntegerField(source='userlessonprogress__watch_time', read_only=True)
    watched = serializers.BooleanField(source='userlessonprogress__watched', read_only=True)

    class Meta:
        model = Lesson
        fields = ('id', 'name', 'duration', 'watch_time', 'watched')