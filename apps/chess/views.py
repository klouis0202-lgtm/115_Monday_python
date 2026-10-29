from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import IntegrityError, transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from .forms import GameForm, RoomForm, RoomGroupForm
from .models import Game, Room, RoomGroup
from .board import board_context


class RoomCreateView(LoginRequiredMixin, View):
    template_name = "chess/room_form.html"

    def get(self, request):
        return render(request, self.template_name, {"form": RoomForm(user=request.user)})

    def post(self, request):
        form = RoomForm(request.POST, user=request.user)
        if form.is_valid():
            try:
                with transaction.atomic():
                    room = form.save(commit=False)
                    room.owner = request.user
                    room.save()
                    form.save_m2m()
            except IntegrityError:
                form.add_error("code", "房間代碼無法使用，請換一個代碼再試一次。")
            else:
                return redirect("chess:room-detail", room_id=room.id)
        return render(request, self.template_name, {"form": form}, status=400)


class RoomListView(LoginRequiredMixin, View):
    def get(self, request):
        keyword = request.GET.get("q", "").strip()
        rooms = Room.objects.filter(owner=request.user).select_related("owner", "owner__profile", "group")
        if keyword:
            rooms = rooms.filter(name__icontains=keyword)
        return render(request, "chess/room_list.html", {"rooms": rooms, "keyword": keyword})


class RoomDetailView(LoginRequiredMixin, View):
    def get(self, request, room_id):
        room = get_object_or_404(Room.objects.select_related("owner", "owner__profile", "group"), pk=room_id, owner=request.user)
        return render(request, "chess/room_detail.html", {"room": room, "game_form": GameForm()})


class GameCreateView(LoginRequiredMixin, View):
    def post(self, request, room_id):
        room = get_object_or_404(Room, pk=room_id, owner=request.user)
        form = GameForm(request.POST)
        if form.is_valid():
            game = form.save(commit=False)
            game.room = room
            game.save()
            messages.success(request, "對局已建立，棋盤已準備完成。")
            return redirect("chess:game-detail", game_id=game.id)
        return render(request, "chess/room_detail.html", {"room": room, "game_form": form}, status=400)


class GameDetailView(LoginRequiredMixin, View):
    def get(self, request, game_id):
        game = get_object_or_404(Game.objects.select_related("room", "room__owner"),
                                 pk=game_id, room__owner=request.user)
        if game.status == Game.Status.LEGACY:
            messages.info(request, "這筆舊資料沒有西洋棋局面，請建立新對局。")
            return redirect("chess:room-detail", room_id=game.room_id)
        context = {"game": game, "room": game.room}
        context.update(board_context(game.current_fen, game.player_color))
        return render(request, "chess/game_detail.html", context)


class RoomGroupCreateView(LoginRequiredMixin, View):
    template_name = "chess/group_form.html"

    def get(self, request):
        return render(request, self.template_name, {"form": RoomGroupForm()})

    def post(self, request):
        form = RoomGroupForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    group = form.save(commit=False)
                    group.owner = request.user
                    group.save()
            except IntegrityError:
                form.add_error("name", "你已建立同名群組，請使用其他名稱。")
            else:
                messages.success(request, "群組已建立，現在可以選擇此群組建立房間。")
                return redirect("chess:room-create")
        return render(request, self.template_name, {"form": form}, status=400)


class RoomGroupListView(LoginRequiredMixin, View):
    def get(self, request):
        from django.db.models import Count, Q
        keyword = request.GET.get("q", "").strip()
        groups = RoomGroup.objects.filter(owner=request.user).annotate(
            room_count=Count("rooms", filter=Q(rooms__owner=request.user)))
        if keyword:
            groups = groups.filter(name__icontains=keyword)
        return render(request, "chess/group_list.html", {"groups": groups, "keyword": keyword})


class RoomGroupDetailView(LoginRequiredMixin, View):
    def get(self, request, group_id):
        group = get_object_or_404(RoomGroup, pk=group_id, owner=request.user)
        rooms = group.rooms.filter(owner=request.user).select_related("owner", "owner__profile")
        return render(request, "chess/group_detail.html", {"group": group, "rooms": rooms})
