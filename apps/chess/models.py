from django.db import models


class Room(models.Model):
    name = models.CharField(max_length=100, verbose_name="房間名稱")
    code = models.CharField(max_length=12, unique=True, verbose_name="房間代碼")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="建立時間")

    class Meta:
        verbose_name = "麻將房間"
        verbose_name_plural = "麻將房間"
        ordering = ("-created_at",)

    def __str__(self):
        return self.name


