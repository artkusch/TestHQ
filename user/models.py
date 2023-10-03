from django.db import models
from lesson.models import Lesson


class User(models.Model):
    username = models.CharField(max_length=255, blank=False, null=False)
    email = models.EmailField(max_length=255,blank=False, null=False)


class UserLessonProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    watch_time = models.IntegerField(default=0)
    watched = models.BooleanField(default=False)
    last_view = models.DateField(auto_created=True, blank=False, null=True)



