from rest_framework import routers
from .views import TaskViewSet

router = routers.DefaultRouter()

router.register('task', TaskViewSet, basename='task')

urlpatterns = router.urls
