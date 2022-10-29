from typing import NamedTuple


class Player(NamedTuple):
    """Representação abstrata de um jogador."""

    # O 'símbolo' do jogador, sendo 'X' ou 'O'.
    label: str
    # A cor do 'símbolo' do jogador.
    color: str
