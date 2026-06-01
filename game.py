import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

from constants import *

from ai import get_ai_move

from ui import (
    draw_board,
    draw_pieces,
    draw_captured_pieces
)

from rules import (
    is_valid_move,
    is_in_check,
    is_checkmate,
    is_stalemate,
    find_king
)


class ChessGame:

    def choose_promotion(self, color):

        choice = tk.StringVar()

        window = tk.Toplevel(self.root)
        window.title("Pawn Promotion")
        window.grab_set()

        tk.Label(
            window,
            text="Choose promotion piece:"
        ).pack(padx=10, pady=10)

        options = [
            ("Queen", "q"),
            ("Rook", "r"),
            ("Bishop", "b"),
            ("Knight", "n")
        ]

        for text, value in options:
            tk.Radiobutton(
                window,
                text=text,
                variable=choice,
                value=value
            ).pack(anchor="w")

        choice.set("q")

        def confirm():
            window.destroy()

        tk.Button(
            window,
            text="OK",
            command=confirm
        ).pack(pady=10)

        self.root.wait_window(window)

        return color + choice.get()

    def make_ai_move(self):

        move = get_ai_move(self.board)

        if move is None:

            if is_checkmate(self.board, "black"):

                play_again = messagebox.askyesno(
                    "CHECKMATE",
                    "White wins!\n\nPlay Again?"
                )

                if play_again:
                    self.reset_game()
                else:
                    self.root.destroy()

                return

            if is_stalemate(self.board, "black"):

                play_again = messagebox.askyesno(
                    "STALEMATE",
                    "It's a draw!\n\nPlay Again?"
                )

                if play_again:
                    self.reset_game()
                else:
                    self.root.destroy()

                return

            return

        old_row, old_col, row, col = move

        piece = self.board[old_row][old_col]
        target = self.board[row][col]

        if target is not None:

            if target[0] == "w":
                self.white_captured.append(target)
            else:
                self.black_captured.append(target)

        self.board[row][col] = piece
        self.board[old_row][old_col] = None

        if piece == "bp" and row == 7:
            self.board[row][col] = "bq"

        self.current_turn = "white"

        self.redraw()

        if is_checkmate(self.board, "white"):

            play_again = messagebox.askyesno(
                "CHECKMATE",
                "Black wins!\n\nPlay Again?"
            )

            if play_again:
                self.reset_game()
            else:
                self.root.destroy()

            return

        if is_stalemate(self.board, "white"):

            play_again = messagebox.askyesno(
                "STALEMATE",
                "It's a draw!\n\nPlay Again?"
            )

            if play_again:
                self.reset_game()
            else:
                self.root.destroy()

            return

    def __init__(self, root):

        self.root = root

        self.canvas = tk.Canvas(
            root,
            width=WINDOW_WIDTH,
            height=WINDOW_HEIGHT
        )

        self.canvas.pack()

        self.images = {}

        self.load_images()

        self.board = self.create_board()

        self.selected_piece = None

        self.current_turn = "white"

        self.white_captured = []
        self.black_captured = []

        self.white_king_moved = False
        self.black_king_moved = False

        self.white_left_rook_moved = False
        self.white_right_rook_moved = False

        self.black_left_rook_moved = False
        self.black_right_rook_moved = False

        self.canvas.bind("<Button-1>", self.handle_click)

        self.redraw()

    def load_images(self):

        pieces = [
            "wp", "wr", "wn", "wb", "wq", "wk",
            "bp", "br", "bn", "bb", "bq", "bk"
        ]

        for piece in pieces:

            image = Image.open(f"assets/{piece}.png")

            image = image.resize((SQUARE_SIZE, SQUARE_SIZE))

            self.images[piece] = ImageTk.PhotoImage(image)

    def create_board(self):

        board = [[None for _ in range(8)] for _ in range(8)]

        board[0] = ["br", "bn", "bb", "bq", "bk", "bb", "bn", "br"]
        board[1] = ["bp"] * 8

        board[6] = ["wp"] * 8
        board[7] = ["wr", "wn", "wb", "wq", "wk", "wb", "wn", "wr"]

        return board

    def reset_game(self):

        self.board = self.create_board()

        self.selected_piece = None

        self.current_turn = "white"

        self.white_captured = []
        self.black_captured = []

        self.redraw()

    def redraw(self):

        self.canvas.delete("all")

        checked_king = None

        if is_in_check(self.board, "white"):
            checked_king = find_king(self.board, "white")

        if is_in_check(self.board, "black"):
            checked_king = find_king(self.board, "black")

        draw_board(
            self.canvas,
            checked_king,
            self.selected_piece
        )

        draw_pieces(
            self.canvas,
            self.board,
            self.images
        )

        draw_captured_pieces(
            self.canvas,
            self.images,
            self.white_captured,
            self.black_captured
        )

    def handle_click(self, event):

        if event.x >= BOARD_SIZE * SQUARE_SIZE:
            return

        col = event.x // SQUARE_SIZE
        row = event.y // SQUARE_SIZE

        clicked_piece = self.board[row][col]

        if self.selected_piece is None:

            if clicked_piece is not None:

                piece_color = (
                    "white"
                    if clicked_piece[0] == "w"
                    else "black"
                )

                if piece_color == self.current_turn:

                    self.selected_piece = (row, col)
                    self.redraw()

        else:

            old_row, old_col = self.selected_piece

            piece = self.board[old_row][old_col]

            if is_valid_move(
                self.board,
                old_row,
                old_col,
                row,
                col
            ):

                old_target = self.board[row][col]

                self.board[row][col] = piece
                self.board[old_row][old_col] = None

                if old_target is not None:

                    if old_target[0] == "w":
                        self.white_captured.append(old_target)
                    else:
                        self.black_captured.append(old_target)

                if piece == "wp" and row == 0:
                    self.board[row][col] = self.choose_promotion("w")

                elif piece == "bp" and row == 7:
                    self.board[row][col] = self.choose_promotion("b")

                if self.current_turn == "white":

                    self.current_turn = "black"

                    self.redraw()

                    self.root.after(
                        300,
                        self.make_ai_move
                    )

                else:

                    self.current_turn = "white"

                    self.redraw()

                    if is_checkmate(
                        self.board,
                        self.current_turn
                    ):

                        winner = (
                            "Black"
                            if self.current_turn == "white"
                            else "White"
                        )

                        play_again = messagebox.askyesno(
                            "CHECKMATE",
                            f"{winner} wins!\n\nPlay Again?"
                        )

                        if play_again:
                            self.reset_game()
                        else:
                            self.root.destroy()

                        return

                    if is_stalemate(
                        self.board,
                        self.current_turn
                    ):

                        play_again = messagebox.askyesno(
                            "STALEMATE",
                            "It's a draw!\n\nPlay Again?"
                        )

                        if play_again:
                            self.reset_game()
                        else:
                            self.root.destroy()

                        return

            else:

                print("Invalid move")

            self.selected_piece = None

            if self.root.winfo_exists():
                self.redraw()
