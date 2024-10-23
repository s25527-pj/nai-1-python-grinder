from enum import Enum
import os
from colorama import init
from termcolor import colored


class NodeState(Enum):
    EMPTY = 0
    PLAYER1 = 1
    PLAYER2 = 2


class Node:
    state = NodeState.EMPTY

    def __init__(
        self,
        position: int,
        horizontal_neighbours_positions: list[int],
        vertical_neighbours_positions: list[int],
    ):
        self.position = position
        self.horizontal_neighbours_positions = horizontal_neighbours_positions
        self.vertical_neighbours_positions = vertical_neighbours_positions

    def __str__(self):
        if self.state == NodeState.EMPTY:
            return str(self.position)
        else:
            color = "red" if self.state == NodeState.PLAYER1 else "green"

            return colored(str(self.position), color)

    def get_matching_neighbour_count(
        self, horizontal: bool, excluded_neighbour_position: int = None
    ):
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


def game():
    turn = 0

    print(get_board_representation())

    while player_1_checkers != 2 and player_2_checkers != 2:
        turn += 1

        if turn <= 9:
            put_checker_on_board(1)
            put_checker_on_board(2)

        else:
            move_checker_on_board(1)
            move_checker_on_board(2)

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
