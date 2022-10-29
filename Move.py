from typing import NamedTuple


class Move(NamedTuple):
    """Representação abstrata de um movimento."""

    # O índice da linha do movimento.
    row: int
    # O índice da coluna do movimento.
    col: int
    # O 'símbolo' do jogador responsável pelo movimento.
    label: str = ""
