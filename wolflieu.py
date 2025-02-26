import sys
import random

#convert the text to move in array
def moveToIndex(str):
    if (str == "h1" or str == "r0"):
        return [-1, -1]
    col = ord(str[0]) - 97
    row = 7 - int(str[1])
    if (row != 3):
        if (col < 3):
            col = 0
        elif (col > 3):
            col = 2
        else:
            col = 1
    else:
        if col > 3:
            col -= 1
    return [row, col]

# convert the move from number in array into text
def indexToMove(row, col):
    if (row == 3):
        if (col < 3):
            return chr(col + 97) + "4"
        else:
            return chr(col + 97 + 1) + "4"
    if (col == 1):
        return "d" + str(7 - row)
    if (col < 1):
        return chr(100 - abs(3 - row)) + str(7 - row)
    else:
        return chr(100 + abs(3 - row)) + str(7 - row)

# for debugging purpose, print out the board
def printBoard(board):
    for i in range(7):
        if (abs(3 - i) == 3):
            print("\t" + str(board[i][0]) + "\t" + "\t" + "\t" + str(board[i][1]) + "\t" + "\t" + "\t" + str(board[i][2]))
        elif (abs(3 - i) == 2):
            print("\t" + "\t" + str(board[i][0]) + "\t" + "\t" + str(board[i][1]) + "\t" + "\t" + str(board[i][2]) + "\t")
        elif (abs(3 - i) == 1):
            print("\t" + "\t" + "\t" + str(board[i][0]) + "\t" + str(board[i][1]) + "\t" + str(board[i][2]) + "\t" + "\t")
        else:
            print("\t" + str(board[i][0]) + "\t" +  str(board[i][1]) + "\t" +  str(board[i][2]) + "\t" + "\t" +  str(board[i][3]) + "\t" +  str(board[i][4]) + "\t" +  str(board[i][5]))

# with a legal move used provided by the referee, change the board accordingly
def changeBoard(board, move, type):
    move = move.split(" ")
    if (move[0] != "h1" and move[0] != "h2"):
        moveUsed = moveToIndex(move[0])
        board[moveUsed[0]][moveUsed[1]] = 0
    moveUsed = moveToIndex(move[1])
    board[moveUsed[0]][moveUsed[1]] = type
    if (move[2] != "r0"):
        moveUsed = moveToIndex(move[2])
        board[moveUsed[0]][moveUsed[1]] = 0
    return board

# change a position of the board to type
def changeBoardWithIndex(board, row, col, type):
    board[row][col] = type
    return board

# Check for mill based on the row and column used
def checkForMill(board, row, col, type):
    if (row != 3):
        for i in range(3):
            if (board[row][i] != type):
                break
            if (i == 2):
                return True
        if col == 0:
            if (board[6-row][col] == type and board[3][3 - abs(3-row)] == type):
                return True
        elif col == 2:
            if (board[6-row][col] == type and board[3][2 + abs(3-row)] == type):
                return True
        else:
            if row < 3:
                if (board[0][1] == type and board[1][1] == type and board[2][1] == type):
                    return True
            else:
                if (board[4][1] == type and board[5][1] == type and board[6][1] == type):
                    return True
    else:
        if col < 3:
            for i in range(3):
                if (board[3][i] != type):
                    break
                if (i == 2):
                    return True
            if (board[col][0] == type and board[6 - col][0] == type):
                return True
        else:
            for i in range(3):
                if (board[3][i + 3] != type):
                    break
                if (i == 2):
                    return True
            if (board[col + 1][2] == type and board[6 - col - 1][2] == type):
                return True
    return False

# if the remaining pieces on the board is 2 (assuming the turn is in phase 2)
def checkWinByNumber(board, type):
    type = -type
    count = 0
    for i in range(7):
        for j in range(3):
            if (board[i][j] == type):
                count += 1
    for i in range (3):
        if (board[3][i] == type):
            count += 1
    if type == 2:
        return True
    return False

# return all the positions of the board where the position = type
def checkSpacesState(board, type):
    possibleMoves = []
    for i in range(7):
        for j in range(3):
            if (board[i][j] == type):
                possibleMoves.append([i, j])
    for i in range(3):
        if (board[3][i + 3] == type):
            possibleMoves.append([3, i + 3])
    return possibleMoves

# check for opponent pieces that is not in mill. If all pieces are in a mill, return all opponents pieces
def checkRemovableSpaces(board, type):
    possibleMoves = checkSpacesState(board, type)
    i = 0
    while i < len(possibleMoves):
        if (checkForMill(board, possibleMoves[i][0], possibleMoves[i][1], type)):
            possibleMoves.pop(i)
            i -= 1
        i += 1
    if (len(possibleMoves) == 0):
        possibleMoves = checkSpacesState(board, type)
    return possibleMoves

# with a piece ar row,col, determine the positions that the piece can move to
def checkPossibleMoves(board, row, col):
    possibleMoves = []
    if row != 3:
        if col == 0:
            if (board[3][3 - abs(3-row)] == 0):
                possibleMoves.append([3, 3 - abs(3-row)])
            if (board[row][1] == 0):
                possibleMoves.append([row, 1])
        elif col == 2:
            if (board[3][2 + abs(3-row)] == 0):
                possibleMoves.append([3, 2 + abs(3-row)])
            if (board[row][1] == 0):
                possibleMoves.append([row, 1])
        else:
            if (board[row][0] == 0):
                possibleMoves.append([row, 0])
            if (board[row][2] == 0):
                possibleMoves.append([row, 2])
            if row < 3:
                if row < 2:
                    if (board[row+1][1] == 0):
                        possibleMoves.append([row+1, 1])
                if row > 0:
                    if (board[row-1][1] == 0):
                        possibleMoves.append([row-1, 1])
            if row > 3:
                if row < 6:
                    if (board[row+1][1] == 0):
                        possibleMoves.append([row+1, 1])
                if row > 4:
                    if (board[row-1][1] == 0):
                        possibleMoves.append([row-1, 1])
    else:
        if col < 3:
            if (board[col][0] == 0):
                possibleMoves.append([col, 0])
            if (board[6-col][0] == 0):
                possibleMoves.append([6-col, 0])
            if col < 2:
                if (board[3][col + 1] == 0):
                    possibleMoves.append([3, col + 1])
            elif col > 0:
                if (board[3][col - 1] == 0):
                    possibleMoves.append([3, col - 1])
        else:
            if (board[col + 1][2] == 0):
                possibleMoves.append([col+1, 2])
            if (board[6 - col - 1][2] == 0):
                possibleMoves.append([6-col-1, 2])
            if col > 3:
                if (board[3][col - 1] == 0):
                    possibleMoves.append([3, col - 1])
            elif col < 6:
                if (board[3][col + 1] == 0):
                    possibleMoves.append([3, col + 1])
    return possibleMoves

# evaluation function for heuristic
def evaluate(board, turn):
    score = 0
    blue_moves = checkSpacesState(board, 1)
    orange_moves = checkSpacesState(board, -1)

    center_positions = [[0,1],[1,1],[2,1],[4,1],[5,1],[6,1],[3,0],[3,1],[3,2],[3,3],[3,4],[3,5]]
    if (turn <= 20):
        return (len(blue_moves) - len(orange_moves)) * 100
    
    score += (len(blue_moves) - len(orange_moves)) * 50

    for i in range(len(blue_moves)):
        if blue_moves[i] in center_positions:
            score += 10
    for i in range(len(orange_moves)):
        if orange_moves[i] in center_positions:
            score -= 10

    for i in range(len(blue_moves)):
        score += len(checkPossibleMoves(board, blue_moves[i][0], blue_moves[i][1]))*5
    for i in range(len(orange_moves)):
        score -= len(checkPossibleMoves(board, orange_moves[i][0], orange_moves[i][1]))*5
    return score


# max pruning function
def maxPruning(board, depth, alpha, beta, turn, lastChanged):
    # check if the position is at a loss
    if turn > 20:
        if (checkWinByNumber(board, -1)):
            return -1000
    # check if the position is in a stalemate
    if turn - lastChanged == 20:
        return 0
    # if depth = 0, then return the evaluation function
    if (depth == 0):
        return evaluate(board, turn)
    # if turn <= 20, this means that there are still pieces on hand.
    if (turn <= 20):
        # check for empty spaces that the player can put down
        possibleMoves = checkSpacesState(board, 0)
        for i in range(len(possibleMoves)):
            # change the board accordingly
            board = changeBoardWithIndex(board, possibleMoves[i][0], possibleMoves[i][1], 1)
            # if the move create a mill, move into this function
            if (checkForMill(board, possibleMoves[i][0], possibleMoves[i][1], 1)):
                # check for opponents' removable pieces
                possibleRemoves = checkRemovableSpaces(board, -1)
                for k in range(len(possibleRemoves)):
                    board = changeBoardWithIndex(board, possibleRemoves[k][0], possibleRemoves[k][1], 0)
                    # minimax
                    value = minPruning(board, depth - 1, alpha, beta, turn + 1, turn + 1)
                    if (value > beta):
                        beta = value
                    board = changeBoardWithIndex(board, possibleRemoves[k][0], possibleRemoves[k][1], -1)
            else:
                # minimax
                value = minPruning(board, depth - 1, alpha, beta, turn + 1, turn + 1)
                if (value > beta):
                    beta = value
            board = changeBoardWithIndex(board, possibleMoves[i][0], possibleMoves[i][1], 0)
            # alpha beta pruning
            if alpha <= beta:
                return alpha
    # phase 2 and 3 where the player has to move the pieces on the table
    elif (turn > 20):
        # check all position of the player's pieces
        ChoosablePieces = checkSpacesState(board, 1)
        possibleMoves = []
        for l in range(len(ChoosablePieces)):
            # Check if the player can fly
            if len(ChoosablePieces) == 3:
                possibleMoves = checkSpacesState(board, 0)
            else:
                possibleMoves = checkPossibleMoves(board, ChoosablePieces[l][0], ChoosablePieces[l][1])
            # everything else follow the same thing
            board = changeBoardWithIndex(board, ChoosablePieces[l][0], ChoosablePieces[l][1], 0)
            for i in range(len(possibleMoves)):
                board = changeBoardWithIndex(board, possibleMoves[i][0], possibleMoves[i][1], 1)
                if (checkForMill(board, possibleMoves[i][0], possibleMoves[i][1], 1)):
                    possibleRemoves = checkRemovableSpaces(board, -1)
                    for k in range(len(possibleRemoves)):
                        board = changeBoardWithIndex(board, possibleRemoves[k][0], possibleRemoves[k][1], 0)
                        value = minPruning(board, depth - 1, alpha, beta, turn + 1, turn + 1)
                        if (value > beta):
                            beta = value
                        board = changeBoardWithIndex(board, possibleRemoves[k][0], possibleRemoves[k][1], -1)
                else:
                    value = minPruning(board, depth - 1, alpha, beta, turn + 1, lastChanged)
                    if (value > beta):
                        beta = value
                board = changeBoardWithIndex(board, possibleMoves[i][0], possibleMoves[i][1], 0)
                if alpha <= beta:
                    board = changeBoardWithIndex(board, ChoosablePieces[l][0], ChoosablePieces[l][1], 1)
                    return alpha
            board = changeBoardWithIndex(board, ChoosablePieces[l][0], ChoosablePieces[l][1], 1)
    return beta

def minPruning(board, depth, alpha, beta, turn, lastChanged):
    if turn > 20:
        if (checkWinByNumber(board, 1)):
            return 1000
    if turn - lastChanged == 20:
        return 0
    if (depth == 0):
        return evaluate(board, turn)
    if (turn <= 20):
        possibleMoves = checkSpacesState(board, 0)
        for i in range(len(possibleMoves)):
            board = changeBoardWithIndex(board, possibleMoves[i][0], possibleMoves[i][1], -1)
            if (checkForMill(board, possibleMoves[i][0], possibleMoves[i][1], -1)):
                possibleRemoves = checkRemovableSpaces(board, 1)
                for k in range(len(possibleRemoves)):
                    board = changeBoardWithIndex(board, possibleRemoves[k][0], possibleRemoves[k][1], 0)
                    value = minPruning(board, depth - 1, alpha, beta, turn + 1, turn + 1)
                    if (value < alpha):
                        alpha = value
                    board = changeBoardWithIndex(board, possibleRemoves[k][0], possibleRemoves[k][1], 1)
            else:
                value = maxPruning(board, depth - 1, alpha, beta, turn + 1, turn + 1)
                if (value < alpha):
                    alpha = value
            board = changeBoardWithIndex(board, possibleMoves[i][0], possibleMoves[i][1], 0)
            if alpha <= beta:
                return alpha
            
    elif (turn > 20):
        ChoosablePieces = checkSpacesState(board, -1)
        possibleMoves = []
        for l in range(len(ChoosablePieces)):
            if len(ChoosablePieces) == 3:
                possibleMoves = checkSpacesState(board, 0)
            else:
                possibleMoves = checkPossibleMoves(board, ChoosablePieces[l][0], ChoosablePieces[l][1])
            board = changeBoardWithIndex(board, ChoosablePieces[l][0], ChoosablePieces[l][1], 0)
            for i in range(len(possibleMoves)):
                board = changeBoardWithIndex(board, possibleMoves[i][0], possibleMoves[i][1], -1)
                if (checkForMill(board, possibleMoves[i][0], possibleMoves[i][1], -1)):
                    possibleRemoves = checkRemovableSpaces(board, 1)
                    for k in range(len(possibleRemoves)):
                        board = changeBoardWithIndex(board, possibleRemoves[k][0], possibleRemoves[k][1], 0)
                        value = minPruning(board, depth - 1, alpha, beta, turn + 1, turn + 1)
                        if (value < alpha):
                            alpha = value
                        board = changeBoardWithIndex(board, possibleRemoves[k][0], possibleRemoves[k][1], 1)
                else:
                    value = maxPruning(board, depth - 1, alpha, beta, turn + 1, lastChanged)
                    if (value < alpha):
                        alpha = value
                board = changeBoardWithIndex(board, possibleMoves[i][0], possibleMoves[i][1], 0)
                if alpha <= beta:
                    board = changeBoardWithIndex(board, ChoosablePieces[l][0], ChoosablePieces[l][1], -1)
                    return alpha
            board = changeBoardWithIndex(board, ChoosablePieces[l][0], ChoosablePieces[l][1], -1)
    return alpha


def makeMove(board, turn, lastChanged, isBlue):
    # initialize depth, alpha and beta 
    depth = 5
    alpha = 2000
    beta = -2000
    if turn > 20:
        if (checkWinByNumber(board, 1)):
            return "I won"
        if (checkWinByNumber(board, -1)):
            return "I lost"
    if turn - lastChanged == 20:
        return "draw"
    firstMove = ""
    secondMove = ""
    thirdMove = "r0"
    # everything also follows max pruning function except when the value is larger than beta, update the move
    if (turn <= 20):
        firstMove = "h2"
        if (isBlue):
            firstMove = "h1"
        possibleMoves = checkSpacesState(board, 0)
        for i in range(len(possibleMoves)):
            board = changeBoardWithIndex(board, possibleMoves[i][0], possibleMoves[i][1], 1)
            if (checkForMill(board, possibleMoves[i][0], possibleMoves[i][1], 1)):
                possibleRemoves = checkRemovableSpaces(board, -1)
                for k in range(len(possibleRemoves)):
                    board = changeBoardWithIndex(board, possibleRemoves[k][0], possibleRemoves[k][1], 0)
                    value = minPruning(board, depth, alpha, beta, turn + 1, turn + 1)
                    if (value > beta):
                        beta = value
                        secondMove = indexToMove(possibleMoves[i][0], possibleMoves[i][1])
                        thirdMove = indexToMove(possibleRemoves[k][0], possibleRemoves[k][1])
                    board = changeBoardWithIndex(board, possibleRemoves[k][0], possibleRemoves[k][1], -1)
            else:
                value = minPruning(board, depth, alpha, beta, turn + 1, turn + 1)
                if (value > beta):
                    beta = value
                    secondMove = indexToMove(possibleMoves[i][0], possibleMoves[i][1])
                    thirdMove = "r0"
            board = changeBoardWithIndex(board, possibleMoves[i][0], possibleMoves[i][1], 0)
    elif (turn > 20):
        ChoosablePieces = checkSpacesState(board, 1)
        possibleMoves = []
        for l in range(len(ChoosablePieces)):
            if len(ChoosablePieces) == 3:
                possibleMoves = checkSpacesState(board, 0)
            else:
                possibleMoves = checkPossibleMoves(board, ChoosablePieces[l][0], ChoosablePieces[l][1])
            if (len(possibleMoves) == 0):
                continue
            board = changeBoardWithIndex(board, ChoosablePieces[l][0], ChoosablePieces[l][1], 0)
            for i in range(len(possibleMoves)):
                board = changeBoardWithIndex(board, possibleMoves[i][0], possibleMoves[i][1], 1)
                if (checkForMill(board, possibleMoves[i][0], possibleMoves[i][1], 1)):
                    possibleRemoves = checkRemovableSpaces(board, -1)
                    for k in range(len(possibleRemoves)):
                        board = changeBoardWithIndex(board, possibleRemoves[k][0], possibleRemoves[k][1], 0)
                        value = minPruning(board, depth, alpha, beta, turn + 1, turn + 1)
                        if (value > beta):
                            beta = value
                            firstMove = indexToMove(ChoosablePieces[l][0], ChoosablePieces[l][1])
                            secondMove = indexToMove(possibleMoves[i][0], possibleMoves[i][1])
                            thirdMove = indexToMove(possibleRemoves[k][0], possibleRemoves[k][1])
                        board = changeBoardWithIndex(board, possibleRemoves[k][0], possibleRemoves[k][1], -1)
                else:
                    value = minPruning(board, depth, alpha, beta, turn + 1, lastChanged)
                    if (value > beta):
                        beta = value
                        firstMove = indexToMove(ChoosablePieces[l][0], ChoosablePieces[l][1])
                        secondMove = indexToMove(possibleMoves[i][0], possibleMoves[i][1])
                        thirdMove = "r0"
                board = changeBoardWithIndex(board, possibleMoves[i][0], possibleMoves[i][1], 0)
            board = changeBoardWithIndex(board, ChoosablePieces[l][0], ChoosablePieces[l][1], 1)
    return firstMove + " " + secondMove + " " + thirdMove

def makeRandomMove(board, turn, isBlue):
    firstMove = ""
    secondMove = ""
    thirdMove = "r0"
    
    if turn <= 20:
        firstMove = "h1" if isBlue else "h2"
        possibleMoves = checkSpacesState(board, 0)
        moveIndex = random.randint(0, len(possibleMoves) - 1)
        movePos = possibleMoves[moveIndex]
        secondMove = indexToMove(movePos[0], movePos[1])
        
        # check for mills
        board = changeBoardWithIndex(board, movePos[0], movePos[1], 1)
        if checkForMill(board, movePos[0], movePos[1], 1):
            possibleRemoves = checkRemovableSpaces(board, -1)
            if possibleRemoves:
                removeIndex = random.randint(0, len(possibleRemoves) - 1)
                removePos = possibleRemoves[removeIndex]
                thirdMove = indexToMove(removePos[0], removePos[1])

        board = changeBoardWithIndex(board, movePos[0], movePos[1], 0)
    
    else:
        myPieces = checkSpacesState(board, 1)
        # flying
        canFly = len(myPieces) == 3
        validPiecesToMove = []

        for piece in myPieces:
            if canFly:
                possibleDestinations = checkSpacesState(board, 0)
                if possibleDestinations:
                    validPiecesToMove.append(piece)
            else:
                possibleDestinations = checkPossibleMoves(board, piece[0], piece[1])
                if possibleDestinations:
                    validPiecesToMove.append(piece)
        
        pieceIndex = random.randint(0, len(validPiecesToMove) - 1)
        piecePos = validPiecesToMove[pieceIndex]
        firstMove = indexToMove(piecePos[0], piecePos[1])

        if canFly:
            possibleDestinations = checkSpacesState(board, 0)
        else:
            possibleDestinations = checkPossibleMoves(board, piecePos[0], piecePos[1])
        
        destIndex = random.randint(0, len(possibleDestinations) - 1)
        destPos = possibleDestinations[destIndex]
        secondMove = indexToMove(destPos[0], destPos[1])

        board = changeBoardWithIndex(board, piecePos[0], piecePos[1], 0)
        board = changeBoardWithIndex(board, destPos[0], destPos[1], 1)
        
        if checkForMill(board, destPos[0], destPos[1], 1):
            possibleRemoves = checkRemovableSpaces(board, -1)
            if possibleRemoves:
                removeIndex = random.randint(0, len(possibleRemoves) - 1)
                removePos = possibleRemoves[removeIndex]
                thirdMove = indexToMove(removePos[0], removePos[1])
        
        board = changeBoardWithIndex(board, destPos[0], destPos[1], 0)
        board = changeBoardWithIndex(board, piecePos[0], piecePos[1], 1)
    
    return firstMove + " " + secondMove + " " + thirdMove

def main():
    board = [[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0, 0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0]]
    blue = True
    myTurn = False
    turns = 0
    lastChanged = 21
    game_input = input().strip()
    if game_input == "blue":
        myTurn = True
    else:
        blue = False
    while True:
        try:
            if (myTurn):
                turns += 1
                # move = makeMove(board, turns, lastChanged, blue)
                move = makeRandomMove(board, turns, blue)
                print(move, flush = True)
                board = changeBoard(board, move, 1)
                myTurn = False
                if turns > 20:
                    if move[7] != "0":
                        lastChanged = turns
            
            else:
                move = input().strip()
                board = changeBoard(board, move, -1)
                myTurn = True
                turns += 1
                if turns > 20:
                    if move[7] != "0":
                        lastChanged = turns
        except EOFError:
            break

if __name__ == "__main__":
    main()


