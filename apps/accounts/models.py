from django.conf import settings
from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
        verbose_name="使用者",
    )
    display_name = models.CharField(
        max_length=50,
        blank=True,
        verbose_name="顯示名稱",
    )

    class Meta:
        verbose_name = "使用者個人資料"
        verbose_name_plural = "使用者個人資料"

    def __str__(self):
        return self.display_name or self.user.username
