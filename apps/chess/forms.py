from django import forms
from .models import Game, Room


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ("name", "code", "special_rules")
        widgets = {
            "special_rules": forms.CheckboxSelectMultiple(),
            "name": forms.TextInput(attrs={"placeholder": "例如：義大利開局練習"}),
            "code": forms.TextInput(attrs={"placeholder": "例如：opening01"}),
        }
        error_messages = {"code": {"unique": "這個房間代碼已被使用，請改用其他代碼。"}}


class GameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ("player_color",)
        widgets = {"player_color": forms.RadioSelect()}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["player_color"].required = True
        self.fields["player_color"].choices = Game.Color.choices
