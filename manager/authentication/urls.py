from rest_framework import routers
from .views import TokenViewSet, UserViewSet

router = routers.DefaultRouter()

router.register('user', UserViewSet, basename='user')
router.register('token', TokenViewSet, basename='token')

urlpatterns = router.urls
