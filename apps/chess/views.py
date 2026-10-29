from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import IntegrityError, transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from .forms import GameForm, RoomForm
from .models import Game, Room
from .board import board_context


class RoomCreateView(LoginRequiredMixin, View):
    template_name = "chess/room_form.html"

    def get(self, request):
        return render(request, self.template_name, {"form": RoomForm()})

    def post(self, request):
        form = RoomForm(request.POST)
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
        rooms = Room.objects.filter(owner=request.user).select_related("owner", "owner__profile")
        if keyword:
            rooms = rooms.filter(name__icontains=keyword)
        return render(request, "chess/room_list.html", {"rooms": rooms, "keyword": keyword})


class RoomDetailView(LoginRequiredMixin, View):
    def get(self, request, room_id):
        room = get_object_or_404(Room.objects.select_related("owner", "owner__profile"), pk=room_id, owner=request.user)
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
