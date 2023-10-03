from django.shortcuts import render
from django.db.models import Sum
from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from lesson.models import Lesson
from user.models import UserLessonProgress, User
from .models import Product
from access.models import Access


class ProductLessonListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = self.request.user
        product_id = 2
        product = get_object_or_404(Product, pk=product_id)

        if not user.access_set.filter(product=product, access=True).exists():
            return Response({'detail': 'У вас нет доступа к этому продукту.'}, status=403)

        lessons = Lesson.objects.filter(product=product)

        lesson_data = []

        for lesson in lessons:
            try:
                progress = UserLessonProgress.objects.get(user=user, lesson=lesson)
                watched = progress.watched
                watch_time = progress.watch_time
                last_viewed_date = progress.last_view
            except UserLessonProgress.DoesNotExist:
                watched = False
                watch_time = 0
                last_viewed_date = None

            lesson_data.append({
                'id': lesson.id,
                'name': lesson.name,
                'duration': lesson.duration,
                'watched': watched,
                'watch_time': watch_time,
                'last_viewed_date': last_viewed_date
            })

        return render(request, 'lesson_by_product_list.html', {'lessons': lesson_data})


class ProductStatsView(APIView):

    def get(self, request):
        products = Product.objects.all()

        product_stats = []
        for product in products:
            total_watched_lessons = UserLessonProgress.objects.filter(lesson__product=product, watched=True).count()

            total_watch_time = UserLessonProgress.objects.filter(lesson__product=product).aggregate(total_watch_time=Sum('watch_time'))['total_watch_time'] or 0

            total_students = Access.objects.filter(product=product, access=True).count()

            total_users = User.objects.count()
            access_count = Access.objects.filter(product=product, access=True).count()
            purchase_percentage = (access_count / total_users) * 100 if total_users > 0 else 0

            product_stat = {
                'product_name': product.name,
                'total_watched_lessons': total_watched_lessons,
                'total_watch_time_minutes': total_watch_time,
                'total_students': total_students,
                'purchase_percentage': purchase_percentage
            }
            product_stats.append(product_stat)

        return render(request, 'product_stats.html', {'product_stats': product_stats})