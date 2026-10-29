from django import forms
from .models import Game, Room, RoomGroup


class RoomForm(forms.ModelForm):
    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["group"].queryset = RoomGroup.objects.filter(owner=user) if user and user.is_authenticated else RoomGroup.objects.none()
        self.fields["group"].empty_label = "無"


    class Meta:
        model = Room
        fields = ("name", "code", "group", "special_rules")
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


class RoomGroupForm(forms.ModelForm):
    class Meta:
        model = RoomGroup
        fields = ("name",)
        widgets = {"name": forms.TextInput(attrs={"placeholder": "例如：開局練習小組"})}
