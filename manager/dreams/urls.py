from rest_framework import routers
from .views import DreamViewSet

router = routers.DefaultRouter()

router.register('task', DreamViewSet, basename='task')

urlpatterns = router.urls
