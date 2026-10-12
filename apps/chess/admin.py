from django.contrib import admin

from .models import LineGroup, Room, Game, Rule


@admin.register(LineGroup)
class LineGroupAdmin(admin.ModelAdmin):
    list_display = ("display_name", "group_id", "created_at")
    search_fields = ("display_name", "group_id")
    readonly_fields = ("created_at",)


@admin.register(Rule)
class RuleAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at")
    search_fields = ("name",)
    readonly_fields = ("created_at",)


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "line_group", "created_at")
    search_fields = ("name", "code")
    list_filter = ("created_at",)
    filter_horizontal = ("rules",)
    readonly_fields = ("created_at",)



@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ("room", "date", "dong_money", "rounds", "created_at")
    list_filter = ("room", "date")
    search_fields = ("room__name", "room__code")
    readonly_fields = ("created_at",)
