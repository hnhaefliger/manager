from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/authentication/', include('authentication.urls')),
    path('api/goals/', include('goals.urls')),
    path('api/schedule/', include('schedule.urls')),
]
