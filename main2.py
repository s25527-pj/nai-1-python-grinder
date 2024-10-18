from enum import Enum
import math


#FieldTypes define field status, either which player occupies the field or if it's available
class FieldType(Enum):
    EMPTY = 0
    PLAYER1 = 1
    PLAYER2 = 2


#TODO:setter for FieldType?
#Field holds the information about it's position, status and name which is typical combination of column and row position
class Field:
    def __init__(self, col, row):
        self.col = col
        self.row = row
        self.FieldType = FieldType.EMPTY
        self.name = str(col) + str(row)


#TODO: move, check millis, remove
class Board:
    def __init__(self):
        self.board = createNineMensBoard()


#utilizes column-based filled creation to prepare board for 9 mens variation
def createNineMensBoard():
        boardFields = []
        for i in range(7):
            jump = 0
            startRow = 0
            end = 6
            match i:
                case 0 | 6:
                    jump = 3
                case 1 | 5:
                    jump = 2
                    startRow = 1
                    end = 5
                case 2 | 4:
                    jump = 1
                    startRow = 2
                    end = 4
                case 3:
                    jump = 1

            boardFields.extend(createColumnFields(i, startRow, end, jump))

        #clear middle
        boardFields.pop(math.floor(len(boardFields) / 2))

        return boardFields

#needs to double-check
#the field is only adjacent to another if it has either the same row or col
#exception to cover are middle column and row, which are connected but have gap in the middle
def isAdjacent(field1, field2):
    if field1.col == 3:
        return field1.col == field2.col and (field1.row - field2.row >= -1 or field1.row - field2.row <= 1)

    if field1.row == 3:
        return field1.row == field2.row and (field1.col - field2.col >= -1 or field1.col - field2.col <= 1)

    return field1.col == field2.col or field1.row == field2.row


# utility used to simplify field creation depending on size/variation of the board
# creates fields in one column
# col indicates column number, startRow indicates first row to be filled,
# jump depends on rows that need to be filled in column, end is the last row
def createColumnFields(col, startRow, end, jump):
    fields = []
    for i in range(startRow, end + jump, jump):
        fields.append(Field(col, i))

    return fields


#TODO:gameflow logic
def game():
    board = Board()

    #WIP check if fields are correct
    for field in board.board:
        print(field.name)



if __name__ == "__main__":
    game()
