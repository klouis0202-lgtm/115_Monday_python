"""Render stored FEN as a board. This is display parsing, not move validation."""
SYMBOLS = {"k": "♚", "q": "♛", "r": "♜", "b": "♝", "n": "♞", "p": "♟"}
NAMES = {"k": "王", "q": "后", "r": "車", "b": "象", "n": "馬", "p": "兵"}


def board_context(fen, player_color):
    try:
        fields = fen.split()
        if len(fields) != 6 or fields[1] not in ("w", "b"):
            raise ValueError("Invalid FEN fields")
        rows = fields[0].split("/")
        if len(rows) != 8:
            raise ValueError("Invalid ranks")
        cells = []
        for row_index, row in enumerate(rows):
            pieces = []
            for token in row:
                if token in "12345678":
                    pieces.extend([""] * int(token))
                elif token.lower() in SYMBOLS:
                    pieces.append(token)
                else:
                    raise ValueError("Invalid piece")
            if len(pieces) != 8:
                raise ValueError("Invalid files")
            rank = str(8 - row_index)
            for col, piece in enumerate(pieces):
                file = "abcdefgh"[col]
                color = "white" if piece and piece.isupper() else "black"
                label = (("白" if color == "white" else "黑") + NAMES[piece.lower()]) if piece else "空格"
                cells.append({"coordinate": file + rank, "file": file, "rank": rank,
                              "dark": bool((row_index + col) % 2), "piece": piece,
                              "symbol": SYMBOLS.get(piece.lower(), ""), "color": color,
                              "label": file + rank + "，" + label})
        if player_color == "black":
            cells.reverse()
        return {"squares": cells, "board_error": "", "side_to_move": "白方" if fields[1] == "w" else "黑方"}
    except (AttributeError, TypeError, ValueError):
        return {"squares": [], "board_error": "目前的局面資料無法顯示。請返回房間建立新對局，或請管理員檢查這筆紀錄。", "side_to_move": "無法判定"}
