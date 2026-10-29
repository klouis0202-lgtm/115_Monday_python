from django import forms

from .models import UserProfile


class ProfileSignupForm(forms.Form):
    display_name = forms.CharField(
        max_length=50,
        label="顯示名稱",
        help_text="這個名稱會顯示在ChessOracle中。",
    )

    def signup(self, request, user):
        UserProfile.objects.create(
            user=user,
            display_name=self.cleaned_data["display_name"],
        )
