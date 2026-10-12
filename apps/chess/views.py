from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from .models import Room, Rule


class RoomCreateView(View):
    template_name = "chess/room_form.html"

    def get(self, request):
        return render(request, self.template_name, {"rules": Rule.objects.all()})

    def post(self, request):
    
        name = request.POST.get("name", "").strip()
        code = request.POST.get("code", "").strip()
        selected_rule_ids = request.POST.getlist("rules")

        context = {
            "rules": Rule.objects.all(),
            "name": name,
            "code": code,
            "selected_rule_ids": selected_rule_ids,
        }

        if not name or not code:
            context["error"] = "請填寫房間名稱與房間代碼。"
            return render(request, self.template_name, context, status=400)

        if Room.objects.filter(code=code).exists():
            context["error"] = "這個房間代碼已被使用，請改用其他代碼。"
            return render(request, self.template_name, context, status=400)

        room = Room.objects.create(name=name, code=code)
        room.rules.set(Rule.objects.filter(id__in=selected_rule_ids))

        return redirect("chess:room-detail", room_id=room.id)

class RoomListView(View):
    def get(self, request):
        keyword = request.GET.get("q", "").strip()
        rooms = Room.objects.all()

        if keyword:
            rooms = rooms.filter(name__icontains=keyword)

        return render(request, "chess/room_list.html", {
            "rooms": rooms,
            "keyword": keyword,
        })


class RoomDetailView(View):
    def get(self, request, room_id):
        room = get_object_or_404(Room, pk=room_id)

        return render(request, "chess/room_detail.html", {
            "room": room,
        })