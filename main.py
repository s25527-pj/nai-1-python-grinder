from enum import Enum


class NodeState(Enum):
    EMPTY = 0
    PLAYER1 = 1
    PLAYER2 = 2

class Node:
    state = NodeState.PLAYER1

    def __init__(self, position: int, horizontal_neighbours_positions: list[int], vertical_neighbours_positions: list[int]):
        self.position = position
        self.horizontal_neighbours_positions = horizontal_neighbours_positions
        self.vertical_neighbours_positions = vertical_neighbours_positions

    def check_neighbouring_nodes_state(self, horizontal: bool, excluded_neighbour_position: int = None):
        # zeby w pelni zrozumiec dzialanie tej funkcji ponumeruj kazdy z node'ow od 1 do 24 od lewej do prawej
        # jesli suma jest rowna 2, oznacza to ze w linii znajduja sie 3 node'y o tym samym stanie, czyli naliczony zostanie punkt
        # takie podejscie pozwala nam rowniez wyeliminowac koniecznosc wykonania petli na calej planszy w celu sprawdzenia, czy powinien zostac naliczony punkt
        # po kazdym ruchu sprawdzany jest tylko stan node'ow bedacych w relacji trojkowej z nodem, ktorego stan zostal zmieniony.
        sum = 0
        neighbours_positions = self.horizontal_neighbours_positions if horizontal else self.vertical_neighbours_positions

        for position in neighbours_positions:
            if position is excluded_neighbour_position:
                continue

            neighbouring_node = board[position - 1]

            if self.state == neighbouring_node.state:
                sum += 1
                if sum == 2: return sum
                sum += neighbouring_node.check_neighbouring_nodes_state(horizontal, self.position)
        
        return sum

# taka struktura planszy pozwala nam pozbyc sie logiki zmiany wspolrzednych, dla kazdego z obiektow. jedyne czym musimy manipulowac to stan naszych node'ow.
board = [
    Node(1, [2], [10]),
    Node(2, [1, 3], [5]),
    Node(3, [2], [15])
]

if __name__ == "__main__":
    print(board[0].check_neighbouring_nodes_state(True))


# first = [
#     [NodeState.EMPTY, NodeState.EMPTY, NodeState.EMPTY],
#     [NodeState.EMPTY, NodeState.EMPTY, NodeState.EMPTY],
#     [NodeState.EMPTY, NodeState.PLAYER1, NodeState.EMPTY]
# ]

# second = [
#     [NodeState.EMPTY, NodeState.EMPTY, NodeState.EMPTY],
#     [NodeState.EMPTY, NodeState.EMPTY, NodeState.EMPTY],
#     [NodeState.EMPTY, NodeState.PLAYER1, NodeState.EMPTY]
# ]

# third = [
#     [NodeState.EMPTY, NodeState.EMPTY, NodeState.EMPTY],
#     [NodeState.EMPTY, NodeState.EMPTY, NodeState.EMPTY],
#     [NodeState.EMPTY, NodeState.PLAYER1, NodeState.EMPTY]
# ]


# def check_line_alignment(player: int, matrice: list[list[NodeState]], direction: str):
#     sum = 0

#     for h in range(0, 3):
#         for v in range(0, 3):
#             if matrice[h if direction == "horizontal" else v][v if direction == "horizontal" else h] is NodeState(player):
#                 sum+=1
#         if sum == 3:
#             return True
#         else:
#             sum = 0

# def check_matrix_alignment(player: int, matrice: list[list[NodeState]]):
#     return check_line_alignment(player, matrice, "horizontal") or check_line_alignment(player, matrice, "vertical")


        
# def check_inter_matrix_alignment(player: int, direction: str):
#     i = 1 if direction == "horizontal" else 0
#     j = 0 if direction == "horizontal" else 1
    
#     for k in range(2):
#         if first[i][j] is NodeState(player) and second[i][j] is NodeState(player) and third[i][j] is NodeState(player):
#             return True
#         if direction == "horizontal":
#             # check on right
#             j+=2
#         else:
#             # check on bottom
#             i+=2




# if __name__ == "__main__":
#     print(check_matrix_alignment(1, first))
#     print(check_inter_matrix_alignment(1, "vertical"))