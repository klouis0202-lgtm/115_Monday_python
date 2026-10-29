from django.urls import path
from .views import GameDetailView, GameCreateView, RoomCreateView, RoomDetailView, RoomListView

app_name = "chess"
urlpatterns = [
    path("games/<int:game_id>/", GameDetailView.as_view(), name="game-detail"),
    path("rooms/", RoomListView.as_view(), name="room-list"),
    path("rooms/create/", RoomCreateView.as_view(), name="room-create"),
    path("rooms/<int:room_id>/", RoomDetailView.as_view(), name="room-detail"),
    path("rooms/<int:room_id>/games/create/", GameCreateView.as_view(), name="game-create"),
]
