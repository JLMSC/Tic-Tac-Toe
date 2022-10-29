import tkinter as tk
from TicTacToe.Board import Board


class Window(tk.Tk):
    """A janela principal."""

    def __init__(self) -> None:
        """Construtor base."""
        super().__init__()
        # Define o título da janela.
        self.title("Jogo da Velha")
        # Objeto responsável pelo tabuleiro.
        self.board = Board(master=self)
