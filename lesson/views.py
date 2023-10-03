from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from .models import Lesson
from user.models import UserLessonProgress


class LessonListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = self.request.user
        accessible_products = user.access_set.filter(access=True).values_list('product', flat=True)

        lessons = Lesson.objects.filter(product__in=accessible_products)

        lesson_data = []

        for lesson in lessons:
            progress_entries = UserLessonProgress.objects.filter(user=user, lesson=lesson)

            watched = False
            watch_time = 0

            if progress_entries.exists():
                latest_progress = progress_entries.order_by('-id').first()
                watched = latest_progress.watched
                watch_time = latest_progress.watch_time

            lesson_data.append({
                'name': lesson.name,
                'duration': lesson.duration,
                'watched': watched,
                'watch_time': watch_time,
            })

        return render(request, 'lessons_list.html', {'lessons': lesson_data})
