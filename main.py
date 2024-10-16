from enum import Enum


class NodeState(Enum):
    EMPTY = 0
    PLAYER1 = 1
    PLAYER2 = 2

first = [
    [NodeState.EMPTY, NodeState.EMPTY, NodeState.EMPTY],
    [NodeState.EMPTY, NodeState.EMPTY, NodeState.EMPTY],
    [NodeState.EMPTY, NodeState.PLAYER1, NodeState.EMPTY]
]

second = [
    [NodeState.EMPTY, NodeState.EMPTY, NodeState.EMPTY],
    [NodeState.EMPTY, NodeState.EMPTY, NodeState.EMPTY],
    [NodeState.EMPTY, NodeState.PLAYER1, NodeState.EMPTY]
]

third = [
    [NodeState.EMPTY, NodeState.EMPTY, NodeState.EMPTY],
    [NodeState.EMPTY, NodeState.EMPTY, NodeState.EMPTY],
    [NodeState.EMPTY, NodeState.PLAYER1, NodeState.EMPTY]
]


def check_line_alignment(player: int, matrice: list[list[NodeState]], direction: str):
    sum = 0

    for h in range(0, 3):
        for v in range(0, 3):
            if matrice[h if direction == "horizontal" else v][v if direction == "horizontal" else h] is NodeState(player):
                sum+=1
        if sum == 3:
            return True
        else:
            sum = 0

def check_matrix_alignment(player: int, matrice: list[list[NodeState]]):
    return check_line_alignment(player, matrice, "horizontal") or check_line_alignment(player, matrice, "vertical")


        
def check_inter_matrix_alignment(player: int, direction: str):
    i = 1 if direction == "horizontal" else 0
    j = 0 if direction == "horizontal" else 1
    
    for k in range(2):
        if first[i][j] is NodeState(player) and second[i][j] is NodeState(player) and third[i][j] is NodeState(player):
            return True
        if direction == "horizontal":
            # check on right
            j+=2
        else:
            # check on bottom
            i+=2




if __name__ == "__main__":
    print(check_matrix_alignment(1, first))
    print(check_inter_matrix_alignment(1, "vertical"))