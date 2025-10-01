from rest_framework.routers import SimpleRouter
from course.views import CourseViewSet, SubscriptionAPIView
from django.urls import path

app_name = "course"

router = SimpleRouter()
router.register("", CourseViewSet)

urlpatterns = [
    path('subscription/', SubscriptionAPIView.as_view(), name='subscription'),
]
urlpatterns += router.urls
