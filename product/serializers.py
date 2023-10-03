from rest_framework import serializers
from lesson.models import Lesson


class LessonSerializer(serializers.ModelSerializer):
    watch_time = serializers.IntegerField(source='userlessonprogress__watch_time', read_only=True)
    watched = serializers.BooleanField(source='userlessonprogress__watched', read_only=True)
    last_view = serializers.BooleanField(source='userlessonprogress__last_view', read_only=True)

    class Meta:
        model = Lesson
        fields = ('id', 'name', 'duration', 'watch_time', 'watched', 'last_view')