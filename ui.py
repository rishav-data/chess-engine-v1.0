from constants import *

# =========================
# DRAW BOARD
# =========================

def draw_board(
    canvas,
    checked_king=None,
    selected_piece=None
):

    for row in range(BOARD_SIZE):

        for col in range(BOARD_SIZE):

            x1 = col * SQUARE_SIZE
            y1 = row * SQUARE_SIZE

            x2 = x1 + SQUARE_SIZE
            y2 = y1 + SQUARE_SIZE

            # Default colors
            if (row + col) % 2 == 0:
                color = LIGHT_COLOR
            else:
                color = DARK_COLOR

            # Highlight selected piece
            if selected_piece == (row, col):
                color = "green"

            # Highlight checked king
            if checked_king == (row, col):
                color = "red"

            canvas.create_rectangle(
                x1,
                y1,
                x2,
                y2,
                fill=color,
                outline=color
            )

# =========================
# DRAW PIECES
# =========================

def draw_pieces(canvas, board, images):

    for row in range(8):

        for col in range(8):

            piece = board[row][col]

            if piece is not None:

                x = col * SQUARE_SIZE
                y = row * SQUARE_SIZE

                canvas.create_image(
                    x,
                    y,
                    image=images[piece],
                    anchor="nw"
                )

# =========================
# DRAW CAPTURED PIECES
# =========================

def draw_captured_pieces(
    canvas,
    images,
    white_captured,
    black_captured
):

    panel_x = BOARD_SIZE * SQUARE_SIZE + 20

    canvas.create_text(
        panel_x,
        20,
        text="Captured Pieces",
        font=("Arial", 18, "bold"),
        anchor="nw"
    )

    piece_labels = {
        "p": "Pawns",
        "r": "Rooks",
        "n": "Knights",
        "b": "Bishops",
        "q": "Queens"
    }

    # =========================
    # WHITE CAPTURED
    # =========================

    canvas.create_text(
        panel_x,
        60,
        text="White Captured",
        font=("Arial", 14, "bold"),
        anchor="nw"
    )

    y = 100

    for piece_type, label in piece_labels.items():

        canvas.create_text(
            panel_x,
            y,
            text=label + ":",
            font=("Arial", 11, "bold"),
            anchor="nw"
        )

        x = panel_x + 100

        for piece in white_captured:

            if piece[1] == piece_type:

                canvas.create_image(
                    x,
                    y,
                    image=images[piece],
                    anchor="nw"
                )

                x += 35

        y += 50

    # =========================
    # BLACK CAPTURED
    # =========================

    canvas.create_text(
        panel_x,
        380,
        text="Black Captured",
        font=("Arial", 14, "bold"),
        anchor="nw"
    )

    y = 420

    for piece_type, label in piece_labels.items():

        canvas.create_text(
            panel_x,
            y,
            text=label + ":",
            font=("Arial", 11, "bold"),
            anchor="nw"
        )

        x = panel_x + 100

        for piece in black_captured:

            if piece[1] == piece_type:

                canvas.create_image(
                    x,
                    y,
                    image=images[piece],
                    anchor="nw"
                )

                x += 35

        y += 50