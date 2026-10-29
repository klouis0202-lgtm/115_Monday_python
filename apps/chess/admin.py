from django.contrib import admin
from .models import Game, Room, SpecialRule

admin.site.site_header = "ChessOracle 管理"
admin.site.site_title = "ChessOracle 後台"
admin.site.index_title = "網站管理"


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    filter_horizontal = ("special_rules",)
    list_display = ("name", "code", "owner", "created_at")
    search_fields = ("name", "code", "owner__username")
    list_filter = ("created_at",)
    readonly_fields = ("created_at",)
    list_select_related = ("owner",)


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ("room", "date", "player_color", "status", "result", "created_at")
    list_filter = ("status", "player_color", "result", "date")
    search_fields = ("room__name", "room__code")
    readonly_fields = ("initial_fen", "current_fen", "created_at")
    list_select_related = ("room",)


@admin.register(SpecialRule)
class SpecialRuleAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "order")
    search_fields = ("name", "code")
