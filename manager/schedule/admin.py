from django.contrib import admin
from .models import Task


class TaskAdmin(admin.ModelAdmin):
    fields = ('id', 'user_id', 'start', 'end', 'text', 'task_type', 'created_on', 'scheduled_for')
    readonly_fields = ('id', 'user_id',)

    def id(self, obj): return obj.id
    def user_id(self, obj): return str(obj.user_id.id)


admin.site.register(Task, TaskAdmin)
