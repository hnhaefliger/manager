from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse


def empty(request):
    return HttpResponse('wakemydyno', content_type="text/plain")


urlpatterns = [
    path('admin/', admin.site.urls),
    path('wakemydyno.txt', empty),
    path('api/authentication/', include('authentication.urls')),
    path('api/goals/', include('goals.urls')),
    path('api/schedule/', include('schedule.urls')),
    path('api/dreams/', include('dreams.urls')),
    path('api/notes/', include('notes.urls')),
]
