from django.urls import path

from .views import RoomCreateView, RoomDetailView, RoomListView

app_name = "chess"

urlpatterns = [
    path("rooms/", RoomListView.as_view(), name="room-list"),
    path("rooms/create/", RoomCreateView.as_view(), name="room-create"),
    path("rooms/<int:room_id>/", RoomDetailView.as_view(), name="room-detail"),
]
