from django.shortcuts import get_object_or_404, render
from django.views import View

from .models import Room


class RoomDetailView(View):
    def get(self, request, room_id):
        room = get_object_or_404(Room, id=room_id)
        return render(request, "chess/room_detail.html", {"room": room})


class RoomListView(View):
    def get(self, request):
        keyword = request.GET.get("q", "").strip()
        rooms = Room.objects.all()

        if keyword:
            rooms = rooms.filter(name__icontains=keyword)

        context = {
            "rooms": rooms,
            "keyword": keyword,
        }
        return render(request, "chess/room_list.html", context)
