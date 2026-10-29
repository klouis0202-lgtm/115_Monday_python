from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from .forms import GameForm
from .models import Game, Room, STARTING_FEN


class ChessRoomTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.owner = User.objects.create_user(username="owner", password="Test-strong-92745")
        self.other = User.objects.create_user(username="other", password="Test-strong-92745")
        self.room = Room.objects.create(name="Opening practice", code="opening", owner=self.owner)
        self.detail = reverse("chess:room-detail", args=[self.room.pk])
        self.create_game = reverse("chess:game-create", args=[self.room.pk])

    def test_anonymous_must_login(self):
        for url in [reverse("chess:room-list"), reverse("chess:room-create"), self.detail]:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 302)
            self.assertIn("/accounts/login/", response.url)

    def test_other_owner_cannot_read_or_create_games(self):
        self.client.force_login(self.other)
        self.assertNotContains(self.client.get(reverse("chess:room-list")), self.room.name)
        self.assertEqual(self.client.get(self.detail).status_code, 404)
        self.assertEqual(self.client.post(self.create_game, {"player_color": "white"}).status_code, 404)
        self.assertEqual(Game.objects.count(), 0)

    def test_room_form_validates_length_and_unique_code(self):
        self.client.force_login(self.owner)
        url = reverse("chess:room-create")
        for data in [{"name": "test", "code": "x" * 20}, {"name": "test", "code": "opening"}, {"name": "", "code": "new"}]:
            self.assertEqual(self.client.post(url, data).status_code, 400)
        self.assertEqual(Room.objects.count(), 1)

    def test_create_room_sets_owner(self):
        self.client.force_login(self.owner)
        response = self.client.post(reverse("chess:room-create"), {"name": "New room", "code": "new"})
        room = Room.objects.get(code="new")
        self.assertEqual(room.owner, self.owner)
        self.assertRedirects(response, reverse("chess:room-detail", args=[room.pk]))

    def test_game_created_from_starting_position(self):
        self.client.force_login(self.owner)
        response = self.client.post(self.create_game, {"player_color": "black"})
        game = self.room.games.get()
        self.assertRedirects(response, reverse("chess:game-detail", args=[game.pk]))
        self.assertEqual(game.player_color, "black")
        self.assertEqual(game.initial_fen, STARTING_FEN)
        self.assertEqual(game.current_fen, STARTING_FEN)
        self.assertEqual(game.status, "ongoing")
        self.assertEqual(game.result, "*")

    def test_game_requires_valid_color(self):
        self.client.force_login(self.owner)
        for color in ["", "invalid"]:
            self.assertEqual(self.client.post(self.create_game, {"player_color": color}).status_code, 400)
        self.assertFalse(Game.objects.exists())
        self.assertEqual(self.client.get(self.create_game).status_code, 405)

    def test_legacy_record_is_not_presented_as_played_chess(self):
        self.client.force_login(self.owner)
        Game.objects.create(room=self.room, status="legacy", player_color="", initial_fen="", current_fen="")
        response = self.client.get(self.detail)
        self.assertContains(response, "尚無棋譜")
        self.assertNotContains(response, "東錢")

    def test_login_preserves_next(self):
        url = reverse("chess:room-create")
        response = self.client.get(reverse("account_login"), {"next": url})
        self.assertContains(response, 'name="next"')
        response = self.client.post(reverse("account_login"), {"login": "owner", "password": "Test-strong-92745", "next": url})
        self.assertRedirects(response, url)

    def test_admin_is_chess_only(self):
        self.owner.is_staff = self.owner.is_superuser = True
        self.owner.save()
        self.client.force_login(self.owner)
        response = self.client.get(reverse("admin:index"))
        self.assertContains(response, "分析房間")
        self.assertContains(response, "西洋棋對局")
        self.assertNotContains(response, "麻將")
        self.assertNotContains(response, "LINE 群組")

    def test_game_board_has_correct_orientation_and_pieces(self):
        self.client.force_login(self.owner)
        for color, first, last in [("white", "a8", "h1"), ("black", "h1", "a8")]:
            game = Game.objects.create(room=self.room, player_color=color)
            response = self.client.get(reverse("chess:game-detail", args=[game.pk]))
            self.assertEqual(response.status_code, 200)
            squares = response.context["squares"]
            self.assertEqual(len(squares), 64)
            self.assertEqual(sum(bool(s["piece"]) for s in squares), 32)
            self.assertEqual(squares[0]["coordinate"], first)
            self.assertEqual(squares[-1]["coordinate"], last)
            self.assertEqual(response.context["side_to_move"], "白方")
            self.assertContains(response, 'id="chess-board"')

    def test_game_board_is_private(self):
        game = Game.objects.create(room=self.room)
        url = reverse("chess:game-detail", args=[game.pk])
        self.assertEqual(self.client.get(url).status_code, 302)
        self.client.force_login(self.other)
        self.assertEqual(self.client.get(url).status_code, 404)

    def test_legacy_game_returns_to_room(self):
        self.client.force_login(self.owner)
        game = Game.objects.create(room=self.room, status="legacy", current_fen="")
        self.assertRedirects(self.client.get(reverse("chess:game-detail", args=[game.pk])), self.detail)

    def test_bad_fen_is_handled_without_crashing(self):
        self.client.force_login(self.owner)
        game = Game.objects.create(room=self.room, current_fen="bad fen")
        response = self.client.get(reverse("chess:game-detail", args=[game.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "目前的局面資料無法顯示")
        self.assertNotContains(response, 'id="chess-board"')

    def test_board_uses_current_fen_not_starting_fen(self):
        self.client.force_login(self.owner)
        game = Game.objects.create(room=self.room, current_fen="rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1")
        response = self.client.get(reverse("chess:game-detail", args=[game.pk]))
        squares = {s["coordinate"]: s for s in response.context["squares"]}
        self.assertEqual(squares["e4"]["piece"], "P")
        self.assertEqual(squares["e2"]["piece"], "")
        self.assertEqual(response.context["side_to_move"], "黑方")

    def test_room_links_to_existing_game(self):
        self.client.force_login(self.owner)
        game = Game.objects.create(room=self.room)
        response = self.client.get(self.detail)
        self.assertContains(response, reverse("chess:game-detail", args=[game.pk]))

    def test_special_rule_selection(self):
        from .models import SpecialRule
        rules = SpecialRule.objects.all()
        self.assertEqual(list(rules.values_list("name", flat=True)), ["王車易位", "兵的升變", "吃過路兵"])
        self.client.force_login(self.owner)
        url = reverse("chess:room-create")
        self.assertContains(self.client.get(url), 'type="checkbox"', count=3)
        ids = list(rules.values_list("id", flat=True))
        for index, selected in enumerate([[], ids[:2], ids]):
            response = self.client.post(url, {"name": "Rules", "code": "rules" + str(index), "special_rules": selected})
            self.assertEqual(response.status_code, 302)
            room = Room.objects.get(code="rules" + str(index))
            self.assertEqual(set(room.special_rules.values_list("id", flat=True)), set(selected))
        before = Room.objects.count()
        self.assertEqual(self.client.post(url, {"name": "Invalid", "code": "invalid", "special_rules": [999999]}).status_code, 400)
        self.assertEqual(Room.objects.count(), before)
