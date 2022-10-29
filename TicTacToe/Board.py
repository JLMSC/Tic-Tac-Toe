import tkinter as tk
from tkinter import font
from Move import Move
from TicTacToe.Game import Game

from copy import deepcopy


class Board:
    """Representa o tabuleiro (3x3)
    do jogo da velha."""

    def __init__(self, master) -> None:
        """Construtor base."""
        # Referência à janela pai.
        self.master = master
        # Objeto responsável pela lógica do jogo.
        self._game = Game()
        # As posições ('row' e 'col') dos botões.
        self._cells = {}
        # Cria um 'Frame' para os Textos.
        self._create_board_display()
        # Cria o 'Grid' do tabuleiro.
        self._create_board_grid()

    def check_game_state(self) -> None:
        """Verifica o estado atual do jogo, caso não
        tenha terminado, indicando se há vitória ou
        empate."""
        # Verifica se o jogo não terminou.
        if not self._game._game_ended:
            # Verifica por vencedores.
            self._game.check_move()

            # Indica, no caso de vitória, o vencedor e a
            # sequência que o levou à vitória.
            if self._game._has_winner:
                # Marca a sequência vitoriosa.
                self._highlight_cells()
                self._game.next_turn()
                msg = f"{self._game._get_player_label()} venceu!"
                color = self._game._get_player_color()
                self._update_display(msg, color)
                self._game._game_ended = True
            # Indica que, no estado atual do jogo, houve
            # empate.
            elif self._game.is_tied():
                self._update_display(
                    "Empate!", "yellow"
                )
                self._game._game_ended = True

    def user_play(self, event) -> None:
        """Registra a jogada e verifica se houve
        empate ou vencedores, passando o turno caso
        contrário."""
        # Verifica o estado do jogo, indicando
        # se há vitória, empate ou não.
        self.check_game_state()

        # Verifica se o jogo não terminou.
        if not self._game._game_ended:
            # Pega o botão que foi clicado, junto com
            # as suas posições.
            clicked_button = event.widget
            row, col = self._cells[clicked_button]
            # Cria um 'movimento' para determinado
            # botão.
            move = Move(
                row,
                col,
                self._game._get_player_label(),
            )

            # Verifica se o local selecionado é válido.
            if self._game.is_move_valid(move):
                # Atualiza o conteúdo do botão.
                self._update_button(clicked_button)

                # Registra a jogada feita pelo jogador.
                self._game._update_moves(move)

                # Passa o turno.
                self._game.next_turn()

                # Informa de quem é a vez, via texto.
                self._update_display(
                    self._game._get_player_label(),
                    self._game._get_player_color(),
                )

                # Faz o 'bot' jogar.
                self.bot_play()

    def _minimax_check_move(self, pos) -> bool:
        """Verifica se algum jogador fez uma sequência
        vitoriosa no estado atual do jogo.

        Args:
            pos: O estado atual do jogo.

        Returns:
            bool: Se algum jogador venceu com alguma
            sequência."""
        # Itera sobre todas as sequências vitoriosas
        # do jogo.
        for combo in self._game.winning_positions:
            results = set()
            # Itera sobre as sequências vitoriosas,
            # obtendo os 'símbolos' de cada jogada da
            # sequência.
            for item in combo:
                (n, m) = item
                results.add(pos[n][m].label)

            # Verifica se na sequência, existe somente
            # um 'símbolo' e se o 'símbolo' é válido.
            is_win = (
                len(results) == 1
                and "" not in results
            )
            if is_win:
                return True
        return False

    def _minimax_tie(self, pos, has_winner) -> bool:
        """Verifica se o estado atual do jogo está
        empatado.

        Args:
            pos: O estado atual do jogo.
            has_winner: Se o jogo possui
            vencedores.

        Returns:
            bool: Se o estado atual do jogo está
            empatado ou não."""
        played_moves = (
            move.label for row in pos for move in row
        )
        return has_winner and all(played_moves)

    def _minimax_heuristic(self, pos, isMax) -> int:
        """Retorna a heurística do estado atual.

        Args:
            pos: O estado atual do jogo.
            isMax: Indica se está no turno de
            'X' ou 'O'.

        Returns:
            int: Um valor heurística referente ao
            estado atual do jogo."""
        # Verifica se existe vencedores no estado
        # atual do jogo.
        has_winner = self._minimax_check_move(pos)

        # Verifica se o estado atual do jogo está
        # empatado e, então, retorna 0.
        if self._minimax_tie(pos, not has_winner):
            return 0
        # Verifica se o estado atual do jogo possui
        # vencedores e, então, retorna 1 (caso o 'X'
        # vença) ou -1 (caso o 'O' vença).
        elif has_winner:
            return -1 if isMax else 1
        # Se o jogo não tiver terminado, retorna -2.
        else:
            return -2

    def _max(self, pos, alpha, beta):
        """Ramo de maximização, turno de 'X'.

        Args:
            pos: O estado atual do tabuleiro.
            alpha: O melhor valor para alfa.
            beta: O melhor valor para beta.

        Returns:
            O melhor valor encontrado, para jogada de
            maximização, e, também, a melhor jogada
            ('x' e 'y')."""
        # Pega a heurística da posição atual.
        heuristic = self._minimax_heuristic(pos, True)
        # Indica que o jogo terminou, isto é, não
        # existe mais 'folhas' para serem exploradas.
        if heuristic != -2:
            # Retorna a heurística do estado atual.
            return (heuristic, None)
        # Caso o jogo não tenha terminado...
        else:
            # Valores bases (para melhor valor
            # encontrado e melhor jogada).
            best_value = float("-inf")
            best_move = None

            # Itera sobre TODAS as possibilidades,
            # isto é, as posições que 'X' pode jogar.
            for row in pos:
                for move in row:
                    # Verifica se a posição está
                    # disponível.
                    if move.label == "":
                        # Cria uma jogada (objeto) para
                        # a posição escolhida.
                        temp_move = Move(
                            move.row,
                            move.col,
                            "X",
                        )

                        # Registra o movimento,
                        # alterando o estado atual do
                        # jogo.
                        pos[move.row][
                            move.col
                        ] = temp_move

                        # Passa para o ramo de 'min',
                        # pegando o menor valor possível.
                        value = self._min(
                            pos, alpha, beta
                        )[0]

                        # Restaura a posição alterada
                        # previamente.
                        pos[move.row][move.col] = move

                        # Verifica se o valor
                        # encontrado no ramo de 'min'
                        # é melhor que 'best_value'.
                        if value > best_value:
                            # Altera o melhor valor
                            # encontrado, junto com a
                            # melhor sequência.
                            best_value = value
                            best_move = (
                                move.row,
                                move.col,
                            )

                        # Escolhe o maior valor para
                        # 'alpha'.
                        alpha = max(alpha, best_value)

                        # Se 'beta' <= 'alpha', a
                        # podagem é realizada neste
                        # ramo, isto é, a jogada atual.
                        if beta <= alpha:
                            break
            # Retorna o melhor valor encontrado e a
            # melhor jogada.
            return (best_value, best_move)

    def _min(self, pos, alpha, beta):
        """Ramo de minimização, turno de 'O'.

        Args:
            pos: O estado atual do tabuleiro.
            alpha: O melhor valor para alfa.
            beta: O melhor valor para beta.

        Returns:
            O melhor valor encontrado, para jogada de
            minimização, e, também, a melhor jogada
            ('x' e 'y')."""
        # Pega a heurística da posição atual.
        heuristic = self._minimax_heuristic(
            pos, False
        )
        # Indica que o jogo terminou, isto é, não
        # existe mais 'folhas' para serem exploradas.
        if heuristic != -2:
            # Retorna a heurística do estado atual.
            return (heuristic, None)
        # Caso o jogo não tenha terminado...
        else:
            # Valores bases (para melhor valor
            # encontrado e melhor jogada).
            best_value = float("inf")
            best_move = None

            # Itera sobre TODAS as possibilidades,
            # isto é, as posições que 'O' pode jogar.
            for row in pos:
                for move in row:
                    # Verifica se a posição está
                    # disponível.
                    if move.label == "":
                        # Cria uma jogada (objeto) para
                        # a posição escolhida.
                        temp_move = Move(
                            move.row,
                            move.col,
                            "O",
                        )

                        # Registra o movimento,
                        # alterando o estado atual do
                        # jogo.
                        pos[move.row][
                            move.col
                        ] = temp_move

                        # Passa para o ramo de 'max',
                        # pegando o maior valor possível.
                        value = self._max(
                            pos, alpha, beta
                        )[0]

                        # Restaura a posição alterada
                        # previamente.
                        pos[move.row][move.col] = move

                        # Verifica se o valor
                        # encontrado no ramo de 'max'
                        # é melhor que 'best_value'.
                        if value < best_value:
                            # Altera o melhor valor
                            # encontrado, junto com a
                            # melhor sequência.
                            best_value = value
                            best_move = (
                                move.row,
                                move.col,
                            )

                        # Escolhe o menor valor para
                        # 'beta'.
                        beta = min(beta, best_value)

                        # Se 'beta' <= 'alpha', a
                        # podagem é realizada neste
                        # ramo, isto é, a jogada atual.
                        if beta <= alpha:
                            break
            # Retorna o melhor valor encontrado e a
            # melhor jogada.
            return (best_value, best_move)

    def _minimax(self, pos, isMax, alpha, beta):
        """Algoritmo de 'Minimax', com podagem
        alfa-beta.

        Args:
            pos: O estado atual do tabuleiro.
            isMax: Se a jogada é de maximização
            ou de minimização.
            alpha: O melhor valor para alfa.
            beta: O melhor valor para beta.

        Returns:
            O melhor valor encontrado, para jogada de
            maximização ou minimização, e, também, a
            melhor jogada ('x' e 'y')."""
        # Vez de 'X'.
        if isMax:
            return self._max(pos, alpha, beta)
        # Vez de 'O'.
        else:
            return self._min(pos, alpha, beta)

    def bot_play(self) -> None:
        """Aplica o algoritmo de 'Minimax' com podagem
        alfa-beta, para escolher a melhor jogada para
        o 'bot'."""
        # Verifica o estado do jogo, indicando
        # se há vitória, empate ou não.
        self.check_game_state()

        # Verifica se o jogo não terminou.
        if not self._game._game_ended:

            # Aplica o algoritmo de 'Minimax' com
            # poda alfa-beta, retornando o melhor
            # valor encontrando e as coordenadas
            # ('x' e 'y') da melhor jogada.
            res = self._minimax(
                deepcopy(self._game._current_moves),
                False,
                float("-inf"),
                float("inf"),
            )
            best_move = res[1]

            # Cria uma jogada (objeto Move) para o bot.
            bot_move = Move(
                best_move[0],
                best_move[1],
                self._game._get_player_label(),
            )

            # Procura pelo botão correspondente as
            # coordenadas ('x' e 'y') da jogada
            # escolhida pelo 'bot'.
            button = list(self._cells.keys())[
                list(self._cells.values()).index(
                    (bot_move.row, bot_move.col)
                )
            ]

            # Atualiza as informações do botão, isto é,
            # o movimento escolhido pelo 'bot'.
            self._update_button(button)

            # Registra o movimento do 'bot'.
            self._game._update_moves(bot_move)

            # Passa o turno.
            self._game.next_turn()

            # Informa de quem é a vez, via texto.
            self._update_display(
                self._game._get_player_label(),
                self._game._get_player_color(),
            )

            # Verifica o estado do jogo, indicando
            # se há vitória, empate ou não.
            self.check_game_state()

    def _update_button(self, clicked_button) -> None:
        """Atualiza as informações de um botão."""
        # Altera o texto do botão para o 'símbolo' do
        # jogador.
        clicked_button.config(
            text=self._game._get_player_label()
        )
        # Altera a cor do texto do botão, para a cor
        # do 'símbolo' do jogador.
        clicked_button.config(
            fg=self._game._get_player_color()
        )

    def _update_display(
        self, msg: str, color: str = "black"
    ) -> None:
        """Atualiza o texto do 'display'.

        Args:
            msg (str): A nova mensagem a ser inserida
            no 'display'.
            color (str, optional): A cor do texto a
            ser inserido no 'display'.
            Valor padrão: "black".
        """
        self.display["text"] = msg
        self.display["fg"] = color

    def _highlight_cells(self) -> None:
        """Altera a cor de fundo dos botões na
        sequência vitoriosa."""
        for button, coords in self._cells.items():
            if coords in self._game.winner_combo:
                button.config(
                    highlightbackground="black"
                )

    def _create_board_display(self) -> None:
        """Cria um 'Frame' no topo da janela pai."""
        # Cria o 'Frame', ocupando todo o eixo 'X',
        # no topo da janela pai.
        display_frame = tk.Frame(master=self.master)
        display_frame.pack(fill=tk.X)
        # Cria um 'Label' para o 'Frame'.
        self.display = tk.Label(
            master=display_frame,
            text="",
            font=font.Font(size=28, weight="bold"),
        )
        # Exibe o 'Label' no 'Frame' recentemente
        # criado, com um 'pady' de 10.
        self.display.pack(pady=10)

    def _create_board_grid(self) -> None:
        """Cria um 'Frame' para o 'Grid' na janela pai
        e adiciona os botões, referentes ao espaços
        para o 'X' e/ou 'O'."""
        # Cria um 'Frame' para o 'Grid' e exibe-o.
        grid_frame = tk.Frame(master=self.master)
        grid_frame.pack()

        # Itera sobre as linhas do tabuleiro, máximo 3.
        for row in range(3):
            # Configura o posicionamento nas linhas.
            self.master.rowconfigure(
                row, weight=1, minsize=50
            )
            # Configura o posicionamento nas colunas.
            self.master.columnconfigure(
                row, weight=1, minsize=75
            )
            # Itera sobre as colunas do tabuleiro,
            # máximo 3.
            for col in range(3):
                # Cria e configura o botão, responsável
                # pelo 'Grid' na posição 'row' e 'col'.
                button = tk.Button(
                    master=grid_frame,
                    text="",
                    font=font.Font(
                        size=36, weight="bold"
                    ),
                    fg="black",
                    width=3,
                    height=2,
                    highlightbackground="lightblue",
                )
                # Adiciona o botão, junto com as suas
                # posições ('row' e 'col'), em '_cells'.
                self._cells[button] = (row, col)
                # Atribui uma 'key' ao botão, sendo
                # este o botão esquerdo do mouse.
                button.bind(
                    "<ButtonPress-1>", self.user_play
                )
                # Ajusta a posição do botão, conforme
                # o 'row' e 'col'.
                button.grid(
                    row=row,
                    column=col,
                    padx=5,
                    pady=5,
                    sticky="nsew",
                )
