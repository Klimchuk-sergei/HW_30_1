from rest_framework.routers import SimpleRouter
from course.views import CourseViewSet

app_name = "course"

router = SimpleRouter()
router.register("", CourseViewSet)

urlpatterns = []
urlpatterns += router.urls
