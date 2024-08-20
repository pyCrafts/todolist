from goals.models import GoalCategory
from django.contrib import admin
 
@admin.register(GoalCategory)
class GoalCatAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "user", "is_deleted")
    list_display_links = ("title", )
    search_fields = ("title", )
    list_filter = ("is_deleted", )
    readonly_fields = ("created", "updated")