import math
import random
from typing import List, Optional, Dict, Union


class TicTacToe:
    def __init__(self) -> None:
        self.board: List[str] = [' ' for _ in range(9)]
        self.current_winner: Optional[str] = None

    def print_board(self) -> None:
        print("\nBoard:")
        for i, row in enumerate([self.board[i * 3:(i + 1) * 3] for i in range(3)]):
            printable = [
                row[j] if row[j] != ' ' else str(i * 3 + j + 1) for j in range(3)
            ]
            print('| ' + ' | '.join(printable) + ' |')

    def available_moves(self) -> List[int]:
        return [i for i, spot in enumerate(self.board) if spot == ' ']

    def empty_squares(self) -> bool:
        return ' ' in self.board

    def num_empty_squares(self) -> int:
        return self.board.count(' ')

    def make_move(self, square: int, letter: str) -> bool:
        if self.board[square] == ' ':
            self.board[square] = letter
            if self.winner(square, letter):
                self.current_winner = letter
            return True
        return False

    def winner(self, square: int, letter: str) -> bool:
        row_ind = square // 3
        row = self.board[row_ind * 3:(row_ind + 1) * 3]
        if all([s == letter for s in row]):
            return True

        col_ind = square % 3
        column = [self.board[col_ind + i * 3] for i in range(3)]
        if all([s == letter for s in column]):
            return True

        if square % 2 == 0:
            diagonal1 = [self.board[i] for i in [0, 4, 8]]
            if all([s == letter for s in diagonal1]):
                return True
            diagonal2 = [self.board[i] for i in [2, 4, 6]]
            if all([s == letter for s in diagonal2]):
                return True

        return False


class Player:
    def __init__(self, letter: str) -> None:
        self.letter: str = letter

    def get_move(self, game: TicTacToe) -> int:
        pass


class HumanPlayer(Player):
    def get_move(self, game: TicTacToe) -> int:
        valid_square = False
        val: Optional[int] = None
        while not valid_square:
            square = input(f"{self.letter}'s turn. Input move (1-9): ")
            try:
                val = int(square) - 1  # Adjust for 0-indexed board
                if val not in game.available_moves():
                    raise ValueError
                valid_square = True
            except ValueError:
                print("Invalid square. Try again.")
        return val


class AIPlayer(Player):
    def get_move(self, game: TicTacToe) -> int:
        if len(game.available_moves()) == 9:
            return random.choice(game.available_moves())  # First move random
        else:
            move = self.minimax(game, self.letter)['position']
            return move if move is not None else -1

    def minimax(self, state: TicTacToe, player: str) -> Dict[str, Union[int, Optional[int]]]:
        max_player = self.letter
        other_player = 'O' if player == 'X' else 'X'

        if state.current_winner == other_player:
            return {
                'position': None,
                'score': 1 * (state.num_empty_squares() + 1) if other_player == max_player else -1 * (
                    state.num_empty_squares() + 1)
            }

        elif not state.empty_squares():
            return {'position': None, 'score': 0}

        best: Dict[str, Union[int, Optional[int]]] = {
            'position': None,
            'score': -math.inf if player == max_player else math.inf
        }

        for possible_move in state.available_moves():
            state.make_move(possible_move, player)
            sim_score = self.minimax(state, other_player)

            state.board[possible_move] = ' '
            state.current_winner = None
            sim_score['position'] = possible_move

            if player == max_player:
                if isinstance(sim_score['score'], int) and sim_score['score'] > best['score']:
                    best = sim_score
            else:
                if isinstance(sim_score['score'], int) and sim_score['score'] < best['score']:
                    best = sim_score

        return best


def play(game: TicTacToe, x_player: Player, o_player: Player, print_game: bool = True) -> Optional[str]:
    if print_game:
        game.print_board()

    letter = 'X'

    while game.empty_squares():
        if letter == 'O':
            square = o_player.get_move(game)
        else:
            square = x_player.get_move(game)

        if game.make_move(square, letter):
            if print_game:
                print(f"\n{letter} makes a move to square {square + 1}")
                game.print_board()

            if game.current_winner:
                if print_game:
                    print(f"\n{letter} wins!")
                return letter

            letter = 'O' if letter == 'X' else 'X'

        if print_game:
            print()

    if print_game:
        print("It's a tie!")
    return None


# Entry point
if __name__ == '__main__':
    print("Welcome to Tic Tac Toe!")
    human_letter = ''
    while human_letter.upper() not in ['X', 'O']:
        human_letter = input("Do you want to be X or O? ").upper()

    ai_letter = 'O' if human_letter == 'X' else 'X'

    human_player = HumanPlayer(human_letter)
    ai_player = AIPlayer(ai_letter)

    if human_letter == 'X':
        x_player = human_player
        o_player = ai_player
    else:
        x_player = ai_player
        o_player = human_player

    t = TicTacToe()
    play(t, x_player, o_player)
