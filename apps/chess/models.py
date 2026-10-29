from django.conf import settings
from django.db import models
from django.utils import timezone

STARTING_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"


class Room(models.Model):
    name = models.CharField(max_length=100, verbose_name="房間名稱")
    code = models.CharField(max_length=12, unique=True, verbose_name="房間代碼")
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                              related_name="owned_rooms", verbose_name="建立者")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="建立時間")

    class Meta:
        verbose_name = "分析房間"
        verbose_name_plural = "分析房間"
        ordering = ("-created_at",)

    def __str__(self):
        return self.name


class Game(models.Model):
    class Color(models.TextChoices):
        WHITE = "white", "白方"
        BLACK = "black", "黑方"

    class Status(models.TextChoices):
        ONGOING = "ongoing", "進行中"
        FINISHED = "finished", "已結束"
        LEGACY = "legacy", "舊資料（尚無棋譜）"

    class Result(models.TextChoices):
        UNFINISHED = "*", "未定"
        WHITE_WIN = "1-0", "白方勝"
        BLACK_WIN = "0-1", "黑方勝"
        DRAW = "1/2-1/2", "和棋"

    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="games", verbose_name="所屬房間")
    date = models.DateField(default=timezone.localdate, verbose_name="對局日期")
    player_color = models.CharField(max_length=5, choices=Color.choices, default=Color.WHITE, blank=True, verbose_name="我方顏色")
    initial_fen = models.CharField(max_length=100, default=STARTING_FEN, blank=True, verbose_name="起始局面 FEN")
    current_fen = models.CharField(max_length=100, default=STARTING_FEN, blank=True, verbose_name="目前局面 FEN")
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.ONGOING, verbose_name="對局狀態")
    result = models.CharField(max_length=7, choices=Result.choices, default=Result.UNFINISHED, verbose_name="對局結果")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="建立時間")

    class Meta:
        verbose_name = "西洋棋對局"
        verbose_name_plural = "西洋棋對局"
        ordering = ("-date", "-created_at")

    def __str__(self):
        return f"{self.room.name}｜{self.date}"
