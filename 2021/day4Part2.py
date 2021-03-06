from os import error
import numpy as np
from  itertools import chain

from numpy.core.numeric import indices

# Counts number of lines without anything to get num of boards
with open('2021/inputs/4.txt') as f:
    f.readline()
    f.readline()
    numBoards = sum(line.isspace() for line in f)
f.close()


input = open("2021/inputs/4.txt")

# Gets list of numbers
numbers = list(map(int,input.readline().split(",")))
print(numbers)

# Gets one board from input
def read_board(input):
    input.readline()
    board = []

    for _ in range(5):
        board.append(list(map(int,filter(lambda str: str != '', input.readline().strip().split(" ")))))
    return board

# Makes board of bools from board
def makeBool(board):
    npboard = np.array(board)
    boolBoard = (npboard == -1)
    return boolBoard

# Finds index of value
def index_2d(board, n):
    for i, x in enumerate(board):
        if n in x:
            return (i, x.index(n))

# Checks if any rows or columns have only True vals
def winner(boolBoard):
    # rows
    for i in range(len(boolBoard[0])):
        if(all(boolBoard[i])):
            return True
    #transpose to check columns   
    transpose = [list(i) for i in zip(*boolBoard)]
    for i in range(len(transpose[0])):
        if(all(transpose[i])):
            return True     
    return False


def lastVals(boards, boolBoards, nums):
    for i in range(len(nums)):
        if(nums[i] in chain(*boards[0])):
            idx = index_2d(boards[0], nums[i])
            boolBoards[0][idx[0]][idx[1]] = True

        if(winner(boolBoards[0])):
            return boards, boolBoards, nums[i]


# Change bool values and return list of remaining bingo boards
def checkVals(boards, boolBoards, num):
    k=0
    for board in boards:
        if(num in chain(*board) and (len(boards)>1)):
            #print(f"{boards} and {boolBoards} with {num}")
            idx = index_2d(board, num)
            boolBoards[k][idx[0]][idx[1]] = True

        elif(num in chain(*board)):
            remBoards, remBoolBoards
        
        remBoards = [boards[i] for i in range(len(boards)) if not winner(boolBoards[i])]
        remBoolBoards =  [boolBoards[i] for i in range(len(boolBoards)) if not winner(boolBoards[i])]
        k+=1
    return remBoards, remBoolBoards

def changeVals(boards, boolBoards, numbers):
    for i in range(len(numbers)):
        if(len(boards)>1):
            boards, boolBoards = checkVals(boards, boolBoards, numbers[i])
        
        if(len(boards)==1):
            return lastVals(boards, boolBoards, numbers)

def sumUnmarked(board, boolBoard):
    res=0
    indices = [list(i) for i in zip(*np.where(boolBoard == False))]
    board = np.array(board)
    indices = np.array(indices)

    for i in range(len(indices)):
        res += board[tuple(indices[i])].sum(axis=0)
    #sum = board[tuple(indices.T) + (slice(None),)].sum(0)

    return res

# Create board of boards and corresponding bool board
i=0
boards = []
boolBoards = []
while True:
    board = read_board(input)
    boolBoard = makeBool(board)

    boards.append(board)
    boolBoards.append(boolBoard)
    if(i==numBoards):
        break

    i+=1

#print(changeVals(boards, boolBoards, numbers))
boards, boolBoards, num = changeVals(boards, boolBoards, numbers)
print(f"\nboard\n{np.array(boards[0])}\n\nboolboard\n{boolBoards[0]}\n\nnum: {num}")

res = sumUnmarked(boards[0], boolBoards[0])
print(f"sum of unmarked: {res} \nmultiplied by last num: {res*num}")