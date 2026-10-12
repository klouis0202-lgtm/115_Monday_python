from django.db import models


class LineGroup(models.Model):
    group_id = models.CharField(max_length=50, unique=True, verbose_name="LINE 群組 ID")
    display_name = models.CharField(max_length=100, verbose_name="群組顯示名稱")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="建立時間")

    class Meta:
        verbose_name = "LINE 群組"
        verbose_name_plural = "LINE 群組"

    def __str__(self):
        return self.display_name

class Rule(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="規則名稱")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="建立時間")

    class Meta:
        verbose_name = "麻將規則"
        verbose_name_plural = "麻將規則"
        ordering = ("name",)

    def __str__(self):
        return self.name


class Room(models.Model):
    name = models.CharField(max_length=100, verbose_name="房間名稱")
    code = models.CharField(max_length=12, unique=True, verbose_name="房間代碼")
    line_group = models.OneToOneField(
        LineGroup,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="room",
        verbose_name="LINE 群組",
    )
    rules = models.ManyToManyField(
        Rule,
        related_name="rooms",
        blank=True,
        verbose_name="麻將規則",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="建立時間")

    class Meta:
        verbose_name = "麻將房間"
        verbose_name_plural = "麻將房間"
        ordering = ("-created_at",)

    def __str__(self):
        return self.name

class Game(models.Model):
    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        related_name="games",
        verbose_name="所屬房間",
    )
    date = models.DateField(verbose_name="對局日期")
    dong_money = models.PositiveIntegerField(verbose_name="東錢")
    rounds = models.PositiveSmallIntegerField(verbose_name="局數")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="建立時間")

    class Meta:
        verbose_name = "對局紀錄"
        verbose_name_plural = "對局紀錄"
        ordering = ("-date", "-created_at")

    def __str__(self):
        return f"{self.room.name}｜{self.date}"
