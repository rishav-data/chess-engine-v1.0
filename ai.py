import copy

from rules import is_valid_move , is_in_check , is_checkmate, raw_move_is_valid

# =========================
# PIECE VALUES
# =========================

PIECE_VALUES = {
    "p": 1,
    "n": 3,
    "b": 3,
    "r": 5,
    "q": 9,
    "k": 1000
}

KNIGHT_TABLE = [
[-5,-4,-3,-3,-3,-3,-4,-5],
[-4,-2,0,0,0,0,-2,-4],
[-3,0,1,1.5,1.5,1,0,-3],
[-3,0.5,1.5,2,2,1.5,0.5,-3],
[-3,0,1.5,2,2,1.5,0,-3],
[-3,0.5,1,1.5,1.5,1,0.5,-3],
[-4,-2,0,0.5,0.5,0,-2,-4],
[-5,-4,-3,-3,-3,-3,-4,-5]
]

# =========================
# BOARD EVALUATION
# =========================

def evaluate_board(board):

    score = 0

    for row in range(8):

        for col in range(8):

            piece = board[row][col]

            if piece is None:
                continue

            value = PIECE_VALUES[piece[1]]

            # Material
            if piece[0] == "b":
                score += value
            else:
                score -= value

            # =========================
            # CENTER CONTROL BONUS
            # =========================

            center_distance = abs(row - 3.5) + abs(col - 3.5)
            bonus = max(0, 1.5 - center_distance) * 0.3

            if piece[0] == "b":
                score += bonus
            else:
                score -= bonus
            
            # =========================
            # PAWN ADVANCEMENT BONUS
            # =========================

            if piece[1] == "p":

                if piece[0] == "b":
                    score += row * 0.1
                else:
                    score -= (7 - row) * 0.1

            # =========================
            # KNIGHT DEVELOPMENT
            # =========================

            if piece[1] == "n":

                value = KNIGHT_TABLE[row][col]

                if piece[0] == "b":
                    score += value
                else:
                    score -= value

            # =========================
            # BISHOP DEVELOPMENT
            # =========================

            if piece[1] == "b":

                if piece[0] == "b":

                    if row > 0:
                        score += 0.3

                else:

                    if row < 7:
                        score -= 0.3

            # making the king safer (DO NOT QUESTION MY COMMENTING IM TIRED)
            if piece == "bk":

                if row > 1:
                    score += 2
            
            elif piece == "wk":
                if row < 6:
                    score -= 2

    return score
# =========================
# ALL LEGAL MOVES
# =========================

def get_all_legal_moves(board, color):

    moves = []

    prefix = "b" if color == "black" else "w"

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

                        moves.append(
                            (
                                old_row,
                                old_col,
                                new_row,
                                new_col
                            )
                        )

    return moves

# =========================
# DEFENSE
#==========================

def square_is_attacked(board, row, col, attacker_color):

    prefix = "w" if attacker_color == "white" else "b"

    for old_row in range(8):

        for old_col in range(8):

            piece = board[old_row][old_col]

            if piece is None:
                continue

            if piece[0] != prefix:
                continue

            if raw_move_is_valid(
                board,
                old_row,
                old_col,
                row,
                col
            ):
                return True

    return False

# =========================
# EVALUATE MOVE
# =========================

def evaluate_move(board, move):

    old_row, old_col, new_row, new_col = move

    score = 0

    captured_piece = board[new_row][new_col]

    # =========================
    # CAPTURE BONUS
    # =========================

    if captured_piece is not None:

        score += (
            PIECE_VALUES[captured_piece[1]]
            * 5
        )

    test_board = copy.deepcopy(board)

    piece = test_board[old_row][old_col]

    test_board[new_row][new_col] = piece
    test_board[old_row][old_col] = None

    # =========================
    # POSITIONAL EVALUATION
    # =========================

    score += evaluate_board(test_board)

    # Hanging piece penalty
    if square_is_attacked(
        test_board,
        new_row,
        new_col,
        "white"):
            score -= (
        PIECE_VALUES[piece[1]]
        * 8
        )
            
    # Defended piece bonus
    if square_is_attacked(
        test_board,
        new_row,
        new_col,
        "black"
        ):
        score += 2



    # =========================
    # CHECK BONUS
    # =========================

    if is_in_check(test_board, "white"):
        score += 50

    # =========================
    # CHECKMATE BONUS
    # =========================

    if is_checkmate(test_board, "white"):
        score += 100000

    # =========================
    # MOBILITY BONUS
    # =========================

    score += (
        len(
            get_all_legal_moves(
                test_board,
                "black"
            )
        )
        * 0.1
    )

    # =========================
    # CENTER CONTROL BONUS
    # =========================

    if new_row in [3, 4] and new_col in [3, 4]:
        score += 1

    # =========================
    # DEVELOPMENT BONUS
    # =========================

    if piece[1] in ["n", "b"]:

        if old_row == 0:
            score += 2

    # =========================
    # ADVANCING PAWNS
    # =========================

    if piece[1] == "p":
        score += new_row * 0.3

    return score

# =========================
# AI MOVE SELECTION
# =========================

def get_ai_move(board):

    legal_moves = get_all_legal_moves(
        board,
        "black"
    )

    if not legal_moves:
        return None

    best_move = None
    best_score = -999999

    for move in legal_moves:

        score = evaluate_move(
            board,
            move
        )

        if score > best_score:

            best_score = score
            best_move = move

    return best_move