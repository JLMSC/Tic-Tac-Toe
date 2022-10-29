import tkinter as tk
from itertools import cycle
from tkinter import font
from typing import Any
from Move import Move

from Player import Player


class Game:
    """Representa toda a lógica do jogo da velha."""

    def __init__(self) -> None:
        """Construtor base."""
        # Um iterador cíclico sobre os jogadores do
        # jogo da velha.
        self._players = cycle(
            (
                Player(label="X", color="red"),
                Player(label="O", color="blue"),
            )
        )
        # O jogador do turno atual.
        self._current_player = next(self._players)
        # O estado atual do jogo.
        self._current_moves = [
            [Move(row, col) for col in range(3)]
            for row in range(3)
        ]
        # As sequências das posições que definem uma
        # vitória.
        self.winning_positions = (
            self._get_winning_positions()
        )
        # A sequência, feita por um jogador, que o
        # levou à vitória.
        self.winner_combo = []
        # Indica se existe um vencedor.
        self._has_winner = False
        # Indica se o jogo já terminou.
        self._game_ended = False

    def _get_player_label(self) -> str:
        """Retorna o 'símbolo' do jogador atual.

        Returns:
            str: O 'símbolo' do jogador atual.
        """
        return self._current_player.label

    def _get_player_color(self) -> str:
        """Retorna a cor do 'símbolo' do jogador atual.

        Returns:
            str: A cor do 'símbolo' do jogador atual.
        """
        return self._current_player.color

    def _get_winning_positions(self) -> list[Any]:
        """Retorna todas as sequência de posições
        vitoriosas.

        Returns:
            list[Any]: Uma lista contendo as
            sequências das posições vitoriosas."""
        # As sequências de vitória nas linhas.
        wins_on_row = [
            [(move.row, move.col) for move in row]
            for row in self._current_moves
        ]
        # As sequências de vitória nas colunas.
        wins_on_col = [
            list(col) for col in zip(*wins_on_row)
        ]
        # As sequências de vitória nas diagonais.
        wins_on_diagonals = [
            [
                row[i]
                for i, row in enumerate(wins_on_row)
            ]
        ]
        wins_on_diagonals.extend(
            [
                [
                    col[j]
                    for j, col in enumerate(
                        reversed(wins_on_col)
                    )
                ]
            ]
        )
        # Retorna todas as sequências de vitória.
        return (
            wins_on_row
            + wins_on_col
            + wins_on_diagonals
        )

    def is_move_valid(self, move: Move) -> bool:
        """Verifica se determinada posição é válida.

        Args:
            move (Move): A posição escolhida pelo
            jogador.

        Returns:
            bool: Se a posição é válida ou não."""
        row, col = move.row, move.col
        current_move_label = self._get_label(row, col)
        return (
            not self._has_winner
            and current_move_label == ""
        )

    def is_tied(self) -> bool:
        """Verifica se há empate no estado atual do
        jogo.

        Returns:
            bool: Se existe empate no estado atual do
            jogo."""
        # Verifica se ninguém ganhou.
        no_winner = not self._has_winner
        # Verifica se todas as posições no tabuleiro
        # (3x3) foram preenchidas, por 'X' ou 'O'.
        played_moves = (
            move.label
            for row in self._current_moves
            for move in row
        )
        # Retorna um valor booleano indicando empate.
        return no_winner and all(played_moves)

    def next_turn(self) -> None:
        """Passa o turno."""
        self._current_player = next(self._players)

    def _get_label(self, row: int, col: int) -> str:
        """Extrai o 'símbolo', de algum jogador,
        contido em uma jogada.

        Args:
            row (int): O índice da linha da jogada.
            col (int): O índice da coluna da jogada.

        Returns:
            str: O 'símbolo' contido na jogada.
        """
        return self._current_moves[row][col].label

    def _update_moves(self, move: Move) -> None:
        """Registra o último movimento feito por algum
        jogador.

        Args:
            move (Any): A jogada feita por algum
            jogador."""
        self._current_moves[move.row][move.col] = move

    def _reset_move(self, move: Move) -> None:
        """Reseta uma jogada.

        Args:
            move (Move): Uma jogada qualquer, feita
            por algum jogador.
        """
        default_move = Move(move.row, move.col, "")
        self._current_moves[move.row][
            move.col
        ] = default_move

    def check_move(self) -> None:
        """Verifica se algum jogador fez uma sequência
        vitoriosa no estado atual do jogo."""
        # Itera sobre todas as sequências vitoriosas
        # do jogo.
        for combo in self.winning_positions:
            results = set()
            # Itera sobre as sequências vitoriosas,
            # obtendo os 'símbolos' de cada jogada da
            # sequência.
            for item in combo:
                (n, m) = item
                results.add(self._get_label(n, m))

            # Verifica se na sequência, existe somente
            # um 'símbolo' e se o 'símbolo' é válido.
            is_win = (
                len(results) == 1
                and "" not in results
            )
            if is_win:
                # Indica que há um vencedor e qual a 
                # sequência usada pelo vencedor.
                self._has_winner = True
                self.winner_combo = combo
                break
