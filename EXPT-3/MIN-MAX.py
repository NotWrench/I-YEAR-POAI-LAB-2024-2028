import math
import random
import copy
from typing import List, Optional, Dict, Union


class TicTacToe:
    def __init__(self) -> None:
        self.board: List[str] = [' ' for _ in range(9)]
        self.current_winner: Optional[str] = None

    def print_board(self) -> None:
        print("\nBoard:")
        for i in range(3):
            row = self.board[i * 3:(i + 1) * 3]
            display = [str(i * 3 + j + 1) if val == ' ' else val for j, val in enumerate(row)]
            print('| ' + ' | '.join(display) + ' |')

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
            diag1 = [self.board[i] for i in [0, 4, 8]]
            diag2 = [self.board[i] for i in [2, 4, 6]]
            if all([s == letter for s in diag1]) or all([s == letter for s in diag2]):
                return True
        return False


class Player:
    def __init__(self, letter: str) -> None:
        self.letter = letter

    def get_move(self, game: TicTacToe) -> int:
        pass


class HumanPlayer(Player):
    def get_move(self, game: TicTacToe) -> int:
        val = None
        while val is None:
            move = input(f"{self.letter}'s move (1-9): ")
            try:
                square = int(move) - 1
                if square not in game.available_moves():
                    raise ValueError
                val = square
            except ValueError:
                print("Invalid move. Try again.")
        return val


class AIPlayer(Player):
    def __init__(self, letter: str) -> None:
        super().__init__(letter)
        self.memo: Dict[str, Dict[str, Union[int, Optional[int]]]] = {}

    def get_move(self, game: TicTacToe) -> int:
        if len(game.available_moves()) == 9:
            return random.choice(game.available_moves())
        result = self.minimax(game, self.letter)
        move = result['position']
        return move if move is not None else random.choice(game.available_moves())

    def board_to_key(self, board: List[str]) -> str:
        return ''.join(board)

    def minimax(self, game: TicTacToe, player: str) -> Dict[str, Union[int, Optional[int]]]:
        key = self.board_to_key(game.board)
        if key in self.memo:
            return self.memo[key]

        max_player = self.letter
        other_player = 'O' if player == 'X' else 'X'

        if game.current_winner == other_player:
            return {
                'position': None,
                'score': 1 * (game.num_empty_squares() + 1) if other_player == max_player else -1 * (game.num_empty_squares() + 1)
            }

        if not game.empty_squares():
            return {'position': None, 'score': 0}

        if player == max_player:
            best = {'position': None, 'score': -math.inf}
        else:
            best = {'position': None, 'score': math.inf}

        for move in game.available_moves():
            temp_game = copy.deepcopy(game)
            temp_game.make_move(move, player)
            sim_result = self.minimax(temp_game, other_player)

            sim_score = {'position': move, 'score': sim_result['score']}

            if player == max_player:
                if sim_score['score'] > best['score']:
                    best = sim_score
            else:
                if sim_score['score'] < best['score']:
                    best = sim_score

        self.memo[key] = best
        return best


def play(game: TicTacToe, x_player: Player, o_player: Player, print_game: bool = True) -> Optional[str]:
    if print_game:
        game.print_board()
    letter = 'X'
    while game.empty_squares():
        player = x_player if letter == 'X' else o_player
        square = player.get_move(game)
        if game.make_move(square, letter):
            if print_game:
                print(f"\n{letter} moves to square {square + 1}")
                game.print_board()
            if game.current_winner:
                if print_game:
                    print(f"\n{letter} wins!")
                return letter
            letter = 'O' if letter == 'X' else 'X'
    if print_game:
        print("It's a tie!")
    return None


if __name__ == '__main__':
    print("Welcome to Tic Tac Toe!")
    human_letter = ''
    while human_letter not in ['X', 'O']:
        human_letter = input("Choose your symbol (X or O): ").upper()
    ai_letter = 'O' if human_letter == 'X' else 'X'
    human = HumanPlayer(human_letter)
    ai = AIPlayer(ai_letter)
    x_player = human if human_letter == 'X' else ai
    o_player = ai if human_letter == 'X' else human
    game = TicTacToe()
    play(game, x_player, o_player)