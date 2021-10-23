from rest_framework import routers
from .views import GoalViewSet

router = routers.DefaultRouter()

router.register('goal', GoalViewSet, basename='goal')

urlpatterns = router.urls
