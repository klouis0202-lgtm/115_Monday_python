from django.urls import path

from .views import RoomDetailView, RoomListView

app_name = "chess"

urlpatterns = [
    path("rooms/", RoomListView.as_view(), name="room-list"),
    path("rooms/<int:room_id>/", RoomDetailView.as_view(), name="room-detail"),
]

