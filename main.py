import tkinter as tk
from game import ChessGame

root = tk.Tk()

root.title("Chess AI Project")

game = ChessGame(root)

root.mainloop()