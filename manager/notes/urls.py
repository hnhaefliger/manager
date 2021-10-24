from rest_framework import routers
from .views import NoteViewSet

router = routers.DefaultRouter()

router.register('note', NoteViewSet, basename='note')

urlpatterns = router.urls
