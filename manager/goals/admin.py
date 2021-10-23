from django.contrib import admin
from .models import Goal


class GoalAdmin(admin.ModelAdmin):
    fields = ('id', 'user_id', 'text', 'category', 'created_on', 'scheduled_for')
    readonly_fields = ('id', 'user_id',)

    def id(self, obj): return obj.id
    def user_id(self, obj): return str(obj.user_id.id)


admin.site.register(Goal, GoalAdmin)
