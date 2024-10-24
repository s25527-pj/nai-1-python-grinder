from enum import Enum
import os
import random
from colorama import init
from termcolor import colored


class NodeState(Enum):
    EMPTY = 0
    PLAYER1 = 1
    PLAYER2 = 2


class Node:
    """
    Represents a node on the board with a position and neighboring node relationships.

    Attributes:
    - position: The position of the node on the board (1-24).
    - horizontal_neighbours_positions: List of positions of horizontally neighboring nodes.
    - vertical_neighbours_positions: List of positions of vertically neighboring nodes.
    - state: The current state of the node (EMPTY, PLAYER1, PLAYER2).
    """

    state = NodeState.EMPTY

    def __init__(
        self,
        position: int,
        horizontal_neighbours_positions: list[int],
        vertical_neighbours_positions: list[int],
    ):
        """
        Initializes a Node with its position and neighboring nodes.
        """
        self.position = position
        self.horizontal_neighbours_positions = horizontal_neighbours_positions
        self.vertical_neighbours_positions = vertical_neighbours_positions

    def __str__(self):
        """
        Returns a string representation of the Node, showing its position and color based on its state.
        """
        if self.state == NodeState.EMPTY:
            return str(self.position)
        else:
            color = "red" if self.state == NodeState.PLAYER1 else "green"
            return colored(str(self.position), color)

    def get_matching_neighbour_count(
        self, horizontal: bool, excluded_neighbour_position: int = None
    ):
        """
        Recursively counts the number of neighboring nodes with the same state, either horizontally or vertically.

        Args:
        - horizontal: True to check horizontal neighbors, False to check vertical neighbors.
        - excluded_neighbour_position: The position of the neighboring node to exclude from the check (optional).

        Returns:
        The count of neighboring nodes with the same state.
        """
        sum = 0
        neighbours_positions = (
            self.horizontal_neighbours_positions
            if horizontal
            else self.vertical_neighbours_positions
        )

        for position in neighbours_positions:
            if position is excluded_neighbour_position:
                continue

            neighbouring_node = board[position - 1]

            if self.state == neighbouring_node.state:
                sum += 1
                sum += neighbouring_node.get_matching_neighbour_count(
                    horizontal, self.position
                )

        return sum


# Initialize the game board with 24 nodes and their respective neighbors.
board = [
    Node(1, [2], [10]),
    Node(2, [1, 3], [5]),
    Node(3, [2], [15]),
    Node(4, [5], [11]),
    Node(5, [4, 6], [2, 8]),
    Node(6, [5], [14]),
    Node(7, [8], [12]),
    Node(8, [7, 9], [5]),
    Node(9, [8], [13]),
    Node(10, [11], [1, 22]),
    Node(11, [10, 12], [4, 19]),
    Node(12, [11], [7, 16]),
    Node(13, [14], [9, 18]),
    Node(14, [13, 15], [6, 21]),
    Node(15, [14], [3, 24]),
    Node(16, [17], [12]),
    Node(17, [16, 18], [20]),
    Node(18, [17], [13]),
    Node(19, [20], [11]),
    Node(20, [19, 21], [17, 23]),
    Node(21, [20], [14]),
    Node(22, [23], [10]),
    Node(23, [22, 24], [20]),
    Node(24, [23], [15]),
]

player_1_checkers = 9
player_2_checkers = 9


def get_board_representation():
    """
    Returns a string representation of the current game board, showing each node's position and state.
    """
    return f"""
{board[0]}            {board[1]}            {board[2]}
    {board[3]}        {board[4]}        {board[5]}
         {board[6]}   {board[7]}    {board[8]}
{board[9]}  {board[10]}  {board[11]}        {board[12]}  {board[13]}  {board[14]}
        {board[15]}   {board[16]}   {board[17]}
    {board[18]}       {board[19]}       {board[20]}
{board[21]}           {board[22]}           {board[23]}
"""


def put_checker_on_board(player: int):
    """
    Allows the current player to place a checker on an empty position on the board.
    If the player forms a mill (3 checkers in a row), the player can remove one of the opponent's checkers.

    Args:
    - player: The current player (1 or 2).
    """
    position = int(
        input(
            f"Player {player}, enter the position (1-24) where you'd like to place your checker: "
        )
    )

    try:
        node = board[position - 1]
    except IndexError:
        print(f"Invalid position {position}. Please enter a number between 1 and 24.")
        put_checker_on_board(player)
        return

    if node.state != NodeState.EMPTY:
        print(
            f"Position {position} is already occupied. Please choose another position."
        )
        put_checker_on_board(player)
        return

    node.state = NodeState(player)

    os.system("cls")
    print(get_board_representation())

    if (
        node.get_matching_neighbour_count(True) == 2
        or node.get_matching_neighbour_count(False) == 2
    ):
        print(f"Player {player}, you scored a point!")

        if player == 1:
            global player_2_checkers
            player_2_checkers -= 1
        else:
            global player_1_checkers
            player_1_checkers -= 1

        remove_checker_from_board(player)


def move_checker_on_board(player: int):
    """
    Allows the current player to move one of their checkers to an adjacent empty position on the board.
    If the move forms a mill, the player can remove one of the opponent's checkers.

    Args:
    - player: The current player (1 or 2).
    """
    from_position = int(
        input(f"Player {player}, enter the position of the checker you want to move: ")
    )
    to_position = int(
        input(
            f"Player {player}, enter the position where you want to move the checker: "
        )
    )

    try:
        from_node = board[from_position - 1]
        to_node = board[to_position - 1]
    except IndexError:
        print(f"Invalid position. Please enter numbers between 1 and 24.")
        move_checker_on_board(player)
        return

    if from_node.state != NodeState(player):
        print(f"Invalid move. You can only move your own checker, Player {player}.")
        move_checker_on_board(player)
        return

    if (
        from_node.position not in to_node.horizontal_neighbours_positions
        and from_node.position not in to_node.vertical_neighbours_positions
    ):
        print(
            f"Invalid move. You can only move to a neighboring position. Position {to_position} is not adjacent to position {from_position}."
        )
        move_checker_on_board(player)
        return

    if to_node.state != NodeState.EMPTY:
        print(
            f"Invalid move. Position {to_position} is already occupied. Please choose another position."
        )
        move_checker_on_board(player)
        return

    from_node.state = NodeState.EMPTY
    to_node.state = NodeState(player)

    os.system("cls")
    print(get_board_representation())

    if (
        to_node.get_matching_neighbour_count(True) == 2
        or to_node.get_matching_neighbour_count(False) == 2
    ):
        print(f"Player {player}, you scored a point!")

        if player == 1:
            global player_2_checkers
            player_2_checkers -= 1
        else:
            global player_1_checkers
            player_1_checkers -= 1

        remove_checker_from_board(player)


def remove_checker_from_board(player: int):
    """
    Allows the current player to remove one of the opponent's checkers after scoring a point.

    Args:
    - player: The current player (1 or 2).
    """
    opponent = 2 if player == 1 else 1
    position = int(
        input(f"Enter the position (1-24) of Player {opponent}'s checker to remove: ")
    )

    try:
        node = board[position - 1]
    except IndexError:
        print(f"Invalid position {position}. Please enter a number between 1 and 24.")
        remove_checker_from_board(player)
        return

    if node.state != NodeState(opponent):
        print(
            f"Invalid move. You can only remove Player {opponent}'s checker. Please choose another position."
        )
        remove_checker_from_board(player)
        return

    node.state = NodeState.EMPTY

    os.system("cls")
    print(get_board_representation())


def evaluate_board():
    """
    Evaluates the board state for Player 2 (AI).
    Gives higher scores for checkers in good positions (near mills, etc.).
    Returns a positive score if Player 2 is in a better position,
    negative if Player 1 is in a better position.
    """
    player_2_score = 0
    player_1_score = 0

    for node in board:
        if node.state == NodeState.PLAYER2:
            # Add score for Player 2's checkers
            player_2_score += 1

            # Check if this checker is part of a potential mill
            if (
                node.get_matching_neighbour_count(True) == 2
                or node.get_matching_neighbour_count(False) == 2
            ):
                player_2_score += 5  # Higher value for forming or being near a mill

        elif node.state == NodeState.PLAYER1:
            # Subtract score for Player 1's checkers
            player_1_score += 1

            # Check if Player 1 is near forming a mill
            if (
                node.get_matching_neighbour_count(True) == 2
                or node.get_matching_neighbour_count(False) == 2
            ):
                player_1_score += 5  # Penalize Player 1's strong positions

    # Final evaluation: higher is better for Player 2 (AI)
    return player_2_score - player_1_score


def generate_possible_moves(player: int):
    """
    Generate a list of all possible moves for the current player (placement or movement).
    """
    possible_moves = []

    # For placement phase, find all empty positions
    for node in board:
        if node.state == NodeState.EMPTY:
            possible_moves.append(node.position)

    # Add movement phase logic if needed

    return possible_moves


def minimax(depth, is_maximizing_player):
    """
    Minimax algorithm to evaluate the best move for the AI (Player 2).
    """
    if depth == 0 or player_1_checkers == 2 or player_2_checkers == 2:
        return evaluate_board()

    if is_maximizing_player:
        max_eval = float("-inf")
        for move in generate_possible_moves(2):  # Player 2
            # Simulate placing a checker
            board[move - 1].state = NodeState.PLAYER2
            eval = minimax(depth - 1, False)
            board[move - 1].state = NodeState.EMPTY  # Undo the move
            max_eval = max(max_eval, eval)
        return max_eval
    else:
        min_eval = float("inf")
        for move in generate_possible_moves(1):  # Player 1
            # Simulate placing a checker
            board[move - 1].state = NodeState.PLAYER1
            eval = minimax(depth - 1, True)
            board[move - 1].state = NodeState.EMPTY  # Undo the move
            min_eval = min(min_eval, eval)
        return min_eval


def ai_place_checker():
    """
    AI (Player 2) places the best checker using minimax and removes Player 1's checker if a mill is formed.
    """
    best_value = float("-inf")
    best_moves = []

    # AI evaluates the best possible move for placing a checker
    for move in generate_possible_moves(2):
        board[move - 1].state = NodeState.PLAYER2  # Simulate the move
        move_value = minimax(3, False)  # AI thinks 3 moves ahead
        board[move - 1].state = NodeState.EMPTY  # Undo the move

        if move_value > best_value:
            best_value = move_value
            best_moves = [move]  # Clear and add new best move
        elif move_value == best_value:
            best_moves.append(move)  # Add to the list of equally good moves

    # Randomly choose from equally valued moves
    best_move = random.choice(best_moves)

    # Place the checker in the best position
    board[best_move - 1].state = NodeState.PLAYER2
    print(f"AI placed a checker at position {best_move}")
    os.system("cls")
    print(get_board_representation())

    # Check if AI formed a mill and remove a Player 1's checker
    node = board[best_move - 1]
    if (
        node.get_matching_neighbour_count(True) == 2
        or node.get_matching_neighbour_count(False) == 2
    ):
        print("AI scored a point!")
        global player_1_checkers
        player_1_checkers -= 1
        ai_remove_player_1_checker()  # Call AI's strategic removal function


def ai_move_checker():
    """
    AI (Player 2) chooses the best move during the movement phase using the minimax algorithm.
    """
    best_move = None
    best_value = float("-inf")

    # Iterate through all checkers belonging to Player 2
    for from_node in board:
        if from_node.state == NodeState.PLAYER2:
            # Generate possible moves (empty neighboring positions)
            for to_position in (
                from_node.horizontal_neighbours_positions
                + from_node.vertical_neighbours_positions
            ):
                to_node = board[to_position - 1]
                if to_node.state == NodeState.EMPTY:
                    # Simulate moving the checker
                    from_node.state = NodeState.EMPTY
                    to_node.state = NodeState.PLAYER2
                    move_value = minimax(3, False)  # AI thinks 3 moves ahead
                    # Undo the move
                    from_node.state = NodeState.PLAYER2
                    to_node.state = NodeState.EMPTY

                    # Choose the move with the best evaluation
                    if move_value > best_value:
                        best_value = move_value
                        best_move = (from_node.position, to_node.position)

    # Perform the best move
    if best_move:
        from_position, to_position = best_move
        board[from_position - 1].state = NodeState.EMPTY
        board[to_position - 1].state = NodeState.PLAYER2
        print(
            f"AI moved checker from position {from_position} to position {to_position}"
        )
        os.system("cls")
        print(get_board_representation())

        # Check if AI formed a mill after the move
        to_node = board[to_position - 1]
        if (
            to_node.get_matching_neighbour_count(True) == 2
            or to_node.get_matching_neighbour_count(False) == 2
        ):
            print(f"Player 2 (AI) scored a point!")
            global player_1_checkers
            player_1_checkers -= 1
            ai_remove_player_1_checker()


def ai_remove_player_1_checker():
    """
    AI (Player 2) strategically removes one of Player 1's checkers after forming a mill.
    The priority is to remove checkers that are part of Player 1's potential mills.
    """
    # Identify Player 1's checkers on the board
    player_1_checkers_positions = [
        node for node in board if node.state == NodeState.PLAYER1
    ]

    if not player_1_checkers_positions:
        return  # No more checkers to remove

    # Step 1: Prioritize removing checkers that are part of a potential mill
    critical_checkers = []
    vulnerable_checkers = []

    for node in player_1_checkers_positions:
        horizontal_count = node.get_matching_neighbour_count(True)
        vertical_count = node.get_matching_neighbour_count(False)

        # Check if Player 1 is close to forming a mill
        if horizontal_count == 2 or vertical_count == 2:
            critical_checkers.append(node)
        elif horizontal_count == 1 or vertical_count == 1:
            vulnerable_checkers.append(node)

    # Step 2: If there are critical checkers, remove one of them
    if critical_checkers:
        node_to_remove = critical_checkers[
            0
        ]  # For now, pick the first one (could improve strategy here)
    elif vulnerable_checkers:
        # Step 3: If no critical checkers, remove vulnerable ones that could form mills in the future
        node_to_remove = vulnerable_checkers[0]
    else:
        # Step 4: As a last resort, remove any Player 1 checker
        node_to_remove = player_1_checkers_positions[0]

    # Remove the selected checker
    board[node_to_remove.position - 1].state = NodeState.EMPTY
    print(f"AI removed Player 1's checker from position {node_to_remove.position}")

    # Refresh the board display
    os.system("cls")
    print(get_board_representation())


def game():
    turn = 0

    print(get_board_representation())

    while player_1_checkers != 2 and player_2_checkers != 2:
        turn += 1

        if turn <= 9:
            put_checker_on_board(1)
            ai_place_checker()

        else:
            move_checker_on_board(1)
            ai_move_checker()

    if player_1_checkers == 2:
        print(
            "Player 2 wins! Player 1 is left with only 2 checkers and cannot make any more moves."
        )

    if player_2_checkers == 2:
        print(
            "Player 1 wins! Player 2 is left with only 2 checkers and cannot make any more moves."
        )


if __name__ == "__main__":
    init()
    game()
