from simpleai.search import SearchProblem, astar
from simpleai.search.viewers import ConsoleViewer

# Define the board positions and mills (winning conditions)
BOARD_POSITIONS = [
    'a1', 'a4', 'a7', 'b2', 'b4', 'b6', 'c3', 'c4', 'c5', 'd1', 'd2', 'd3', 'd5', 'd6', 'd7',
    'e3', 'e4', 'e5', 'f2', 'f4', 'f6', 'g1', 'g4', 'g7'
]

# Define all the possible mill combinations
MILLS = [
    # Horizontal mills
    ['a1', 'a4', 'a7'], ['b2', 'b4', 'b6'], ['c3', 'c4', 'c5'],
    ['d1', 'd2', 'd3'], ['d5', 'd6', 'd7'], ['e3', 'e4', 'e5'],
    ['f2', 'f4', 'f6'], ['g1', 'g4', 'g7'],

    # Vertical mills
    ['a1', 'd1', 'g1'], ['b2', 'd2', 'f2'], ['c3', 'd3', 'e3'],
    ['a4', 'b4', 'c4'], ['e4', 'f4', 'g4'], ['c5', 'd5', 'e5'],
    ['b6', 'd6', 'f6'], ['a7', 'd7', 'g7']
]

# Modify input handling so that the player can input strings like 'a1' instead of index numbers
def get_player_input():
    while True:
        player_input = input("Enter position for X (e.g., 'a1', 'b4'): ").strip().lower()
        if player_input in BOARD_POSITIONS:
            return BOARD_POSITIONS.index(player_input)
        else:
            print("Invalid position. Please enter a valid board position (e.g., 'a1', 'b4').")

# Helper function to get adjacent positions
# Helper function to get adjacent positions
def get_adjacent_positions(pos):
    adjacent = {
        'a1': ['a4', 'd1'],
        'a4': ['a1', 'a7', 'b4'],
        'a7': ['a4', 'd7'],
        'b2': ['b4', 'd2'],
        'b4': ['a4', 'b2', 'b6', 'c4'],
        'b6': ['b4', 'd6'],
        'c3': ['c4', 'd3'],
        'c4': ['c3', 'c5', 'b4'],
        'c5': ['c4', 'd5'],
        'd1': ['a1', 'd2', 'g1'],
        'd2': ['b2', 'd1', 'd3', 'f2'],
        'd3': ['c3', 'd2', 'e3'],
        'd5': ['c5', 'd6', 'e5'],
        'd6': ['b6', 'd5', 'f6', 'd7'],
        'd7': ['a7', 'd6', 'g7'],
        'e3': ['d3', 'e4'],
        'e4': ['e3', 'e5', 'f4'],
        'e5': ['e4', 'd5'],
        'f2': ['f4', 'd2'],
        'f4': ['f2', 'f6', 'e4', 'g4'],
        'f6': ['f4', 'd6'],
        'g1': ['d1', 'g4'],
        'g4': ['g1', 'g7', 'f4'],
        'g7': ['g4', 'd7']
    }
    return adjacent.get(pos, [])

# Helper function to check if a mill is formed
def is_mill(board, player, pos):
    for mill in MILLS:
        if pos in mill and all(board[BOARD_POSITIONS.index(p)] == player for p in mill):
            return True
    return False

# Define the search problem
class NineMensMorrisProblem(SearchProblem):
    def __init__(self, initial):
        self.board = [' '] * len(BOARD_POSITIONS)  # Initialize an empty board
        self.current_player = 'X'
        self.phase = 'placement'
        self.pieces_to_place = {'X': 9, 'O': 9}
        self.removal_phase = False
        super().__init__(initial)

    def actions(self, state):
        board, current_player, phase, pieces_to_place = state

        if phase == 'placement':
            return [pos for pos in range(len(board)) if board[pos] == ' ']
        elif phase == 'movement':
            player_positions = [i for i, p in enumerate(board) if p == current_player]
            actions = []
            for piece in player_positions:
                adj_positions = get_adjacent_positions(BOARD_POSITIONS[piece])
                for adj in adj_positions:
                    adj_index = BOARD_POSITIONS.index(adj)
                    if board[adj_index] == ' ':
                        actions.append((piece, adj_index))
            return actions
        return []

    def result(self, state, action):
        board, current_player, phase, pieces_to_place = state
        board = list(board)

        if phase == 'placement':
            board[action] = current_player
            pieces_to_place[current_player] -= 1

            if is_mill(board, current_player, BOARD_POSITIONS[action]):
                phase = 'removal'
            else:
                current_player = 'O' if current_player == 'X' else 'X'

            if pieces_to_place['X'] == 0 and pieces_to_place['O'] == 0:
                phase = 'movement'

        elif phase == 'movement':
            board[action[1]] = current_player
            board[action[0]] = ' '

            if is_mill(board, current_player, BOARD_POSITIONS[action[1]]):
                phase = 'removal'
            else:
                current_player = 'O' if current_player == 'X' else 'X'

        return tuple(board), current_player, phase, pieces_to_place

    def is_goal(self, state):
        board, current_player, phase, pieces_to_place = state
        # Goal: One player has only two pieces left or no valid moves
        return (pieces_to_place['X'] < 3 or pieces_to_place['O'] < 3)

    def cost(self, state1, action, state2):
        return 1

    def heuristic(self, state):
        board, current_player, phase, pieces_to_place = state
        return 0

    def print_board(self, board):
        print(f"{board[0]}--------{board[1]}--------{board[2]}")
        print("|         |         |")
        print(f"|   {board[3]}-----{board[4]}-----{board[5]}   |")
        print("|   |     |     |   |")
        print(f"{board[6]}---{board[7]}-----{board[8]}---{board[9]}")
        print("|   |     |     |   |")
        print(f"|   {board[10]}-----{board[11]}-----{board[12]}   |")
        print("|         |         |")
        print(f"{board[13]}--------{board[14]}--------{board[15]}")
        print()

# Function to play the game
def play_game():
    initial_board = tuple([' '] * len(BOARD_POSITIONS))
    initial_state = (initial_board, 'X', 'placement', {'X': 9, 'O': 9})
    problem = NineMensMorrisProblem(initial_state)

    current_state = initial_state
    while not problem.is_goal(current_state):
        problem.print_board(current_state[0])
        current_player = current_state[1]

        if current_player == 'X':
            # Human player
            action = get_player_input()
            current_state = problem.result(current_state, action)
        else:
            # AI player
            print("AI is thinking...")
            result = astar(problem)
            current_state = result.state

        problem.print_board(current_state[0])

    print("Game Over!")
    if current_state[1] == 'X':
        print("Player X wins!")
    else:
        print("Player O wins!")

if __name__ == "__main__":
    play_game()
