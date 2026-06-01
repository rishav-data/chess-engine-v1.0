import copy

# =========================
# PATH CHECKING
# =========================

def is_path_clear(board, old_row, old_col, new_row, new_col):

    row_step = 0
    col_step = 0

    if new_row > old_row:
        row_step = 1
    elif new_row < old_row:
        row_step = -1

    if new_col > old_col:
        col_step = 1
    elif new_col < old_col:
        col_step = -1

    current_row = old_row + row_step
    current_col = old_col + col_step

    while (current_row, current_col) != (new_row, new_col):

        if board[current_row][current_col] is not None:
            return False

        current_row += row_step
        current_col += col_step

    return True


# =========================
# FIND KING
# =========================

def find_king(board, color):

    king = "wk" if color == "white" else "bk"

    for row in range(8):

        for col in range(8):

            if board[row][col] == king:
                return (row, col)

    return None


# =========================
# RAW MOVE VALIDATION
# =========================

def raw_move_is_valid(board, old_row, old_col, new_row, new_col):

    piece = board[old_row][old_col]

    if piece is None:
        return False

    piece_type = piece[1]

    target = board[new_row][new_col]

    # Prevent capturing own pieces
    if target is not None:

        if target[0] == piece[0]:
            return False

    row_diff = new_row - old_row
    col_diff = new_col - old_col

        # =========================
    # PAWN
    # =========================

    if piece_type == "p":

        direction = -1 if piece[0] == "w" else 1

        start_row = 6 if piece[0] == "w" else 1

        # Move 1 square forward
        if (
            col_diff == 0
            and row_diff == direction
            and target is None
        ):

            return True

        # Move 2 squares on first move
        if (
            col_diff == 0
            and old_row == start_row
            and row_diff == 2 * direction
            and target is None
        ):

            middle_row = old_row + direction

            if board[middle_row][old_col] is None:
                return True

        # Capture diagonally
        if (
            abs(col_diff) == 1
            and row_diff == direction
            and target is not None
        ):

            return True

    # =========================
    # ROOK
    # =========================

    elif piece_type == "r":

        if old_row == new_row or old_col == new_col:

            return is_path_clear(
                board,
                old_row,
                old_col,
                new_row,
                new_col
            )

    # =========================
    # BISHOP
    # =========================

    elif piece_type == "b":

        if abs(row_diff) == abs(col_diff):

            return is_path_clear(
                board,
                old_row,
                old_col,
                new_row,
                new_col
            )

    # =========================
    # KNIGHT
    # =========================

    elif piece_type == "n":

        if (
            (abs(row_diff) == 2 and abs(col_diff) == 1)
            or
            (abs(row_diff) == 1 and abs(col_diff) == 2)
        ):
            return True

    # =========================
    # QUEEN
    # =========================

    elif piece_type == "q":

        if (
            old_row == new_row
            or old_col == new_col
            or abs(row_diff) == abs(col_diff)
        ):

            return is_path_clear(
                board,
                old_row,
                old_col,
                new_row,
                new_col
            )

    # =========================
    # KING
    # =========================
    elif piece_type == "k":
        if abs(row_diff) <= 1 and abs(col_diff) <= 1:
            return True
        
    return False


# =========================
# CHECK DETECTION
# =========================

def is_in_check(board, color):

    king_position = find_king(board, color)

    if king_position is None:
        return False

    king_row, king_col = king_position

    enemy_color = "b" if color == "white" else "w"

    for row in range(8):

        for col in range(8):

            piece = board[row][col]

            if piece is not None:

                if piece[0] == enemy_color:

                    if raw_move_is_valid(
                        board,
                        row,
                        col,
                        king_row,
                        king_col
                    ):
                        return True

    return False


# =========================
# FULL LEGAL MOVE CHECK
# =========================

def is_valid_move(board, old_row, old_col, new_row, new_col):

    # First check movement rules
    if not raw_move_is_valid(
        board,
        old_row,
        old_col,
        new_row,
        new_col
    ):
        return False

    piece = board[old_row][old_col]

    original_piece = board[new_row][new_col]

    # Simulate move
    board[new_row][new_col] = piece
    board[old_row][old_col] = None

    color = "white" if piece[0] == "w" else "black"

    # Check if own king becomes checked
    illegal = is_in_check(board, color)

    # Undo move
    board[old_row][old_col] = piece
    board[new_row][new_col] = original_piece

    # Illegal self-check move
    if illegal:
        return False

    return True


# =========================
# SIMPLE CHECKMATE DETECTION
# =========================

def is_checkmate(board, color):

    if not is_in_check(board, color):
        return False

    prefix = "w" if color == "white" else "b"

    # Try every piece
    for old_row in range(8):

        for old_col in range(8):

            piece = board[old_row][old_col]

            if piece is None:
                continue

            if piece[0] != prefix:
                continue

            # Try every destination
            for new_row in range(8):

                for new_col in range(8):

                    if is_valid_move(
                        board,
                        old_row,
                        old_col,
                        new_row,
                        new_col
                    ):

                        moving_piece = board[old_row][old_col]
                        captured_piece = board[new_row][new_col]

                        # Simulate move
                        board[new_row][new_col] = moving_piece
                        board[old_row][old_col] = None

                        still_checked = is_in_check(
                            board,
                            color
                        )

                        # Undo move
                        board[old_row][old_col] = moving_piece
                        board[new_row][new_col] = captured_piece

                        # Found an escape
                        if not still_checked:
                            return False

    return True

# =========================
# SIMPLE STALEMATE DETECTION
# =========================

def is_stalemate(board, color):

    if is_in_check(board, color):
        return False

    prefix = "w" if color == "white" else "b"

    for old_row in range(8):
        for old_col in range(8):

            piece = board[old_row][old_col]

            if piece is None:
                continue

            if piece[0] != prefix:
                continue

            for new_row in range(8):
                for new_col in range(8):

                    if is_valid_move(
                        board,
                        old_row,
                        old_col,
                        new_row,
                        new_col
                    ):
                        return False

    return True