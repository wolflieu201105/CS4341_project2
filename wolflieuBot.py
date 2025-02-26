from google import genai
from google.genai import types
import os
from dotenv import load_dotenv
import time
import random


load_dotenv()
api_key = os.getenv("API_KEY")
client = genai.Client(api_key = api_key)

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

def printBoard(board):
    content = ""
    for i in range(7):
        if (abs(3 - i) == 3):
            content += (str(board[i][0]) + "\t" + "\t" + "\t" + str(board[i][1]) + "\t" + "\t" + "\t" + str(board[i][2]))
        elif (abs(3 - i) == 2):
            content += ("\t" + str(board[i][0]) + "\t" + "\t" + str(board[i][1]) + "\t" + "\t" + str(board[i][2]) + "\t")
        elif (abs(3 - i) == 1):
            content += ("\t" + "\t" + str(board[i][0]) + "\t" + str(board[i][1]) + "\t" + str(board[i][2]) + "\t" + "\t")
        else:
            content += (str(board[i][0]) + "\t" +  str(board[i][1]) + "\t" +  str(board[i][2]) + "\t" + "\t" +  str(board[i][3]) + "\t" +  str(board[i][4]) + "\t" +  str(board[i][5]))
        content += "\n"
    return content

# change a position of the board to type
def changeBoardWithIndex(board, row, col, type):
    board[row][col] = type
    return board

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

# make random move as a fallback option
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

def makeMove(board, turns, blue):
    instruction = "Please return the asnswer in 4.5 seconds"
    instruction += "This is a game called larsker morris, I want you to provide the best move possible. Here is how I symbolize the positions: The board has the following format:\n"
    instruction += "a7\t\t\td7\t\t\tg7\n"
    instruction += "\tb6\t\td6\t\tf6\t\n"
    instruction += "\t\tc5\td5\te5\t\t\n"
    instruction += "a4\tb4\tc4\t\te4\tf4\tg4\n"
    instruction += "\t\tc3\td3\te3\t\t\n"
    instruction += "\tb2\t\td2\t\tf2\t\n"
    instruction += "a1\t\t\td1\t\t\tg1\n"
    instruction += "you will win the game when you make the opponent doesn't have any move left or the total number of mills on hand and on board equals to 2.\n"
    instruction += "you will have a mill when the move you just made create a 3 consecutive positions of your man vertically or horizontally. For example, a4 b4 c4, b2 b4 b6 are valid mills while a7 b6 c5 and b4 c4 e4 are not valid mills. When a mill is created, you MUST remove the opponent's man that is not in mill unless all of the opponent's man are in mill"
    instruction += "try to create as much mill as possible, you can break a mill and make it back in order to create a mill again."
    instruction += "In phase 1 (when you still have pieces on hand, if you are blue, decode the first part as h1, if you are orange, decode the first part as h2.) The second part would be the position of the man you want to put in, and the third part would be the position of the opponent that you want to remove if you have a mill. If you don't have a mill, the third part would be r0\n"
    instruction += "In phase 2 (when you don't have any pieces on hand and you have more than 3 man), the first part would be the man that you want to move, the second part is the postion than you want your man to move to (in this phase, you can only move your man to a position next to the previous position), and again, the third part would be the position of the opponent that you want to remove if you have a mill. If you don't have a mill, the third part would be r0\n"
    instruction += "In phase 3 (when you only have 3 man left), the first part would be the man that you want to move, the second part is the postion than you want your man to move to (in this phase, you can move your man to any empty spaces), and again, the third part would be the position of the opponent that you want to remove if you have a mill. If you don't have a mill, the third part would be r0\n"
    instruction += "Some examples are h1 d3 r0 (the blue player takes the man on hand and put in position d3. Since it didn't create a mill, the third part is r0), a7 a4 d3 (the player move it's man from position a7 to a4 and since it create a mill, the player must remove a mam from the opponent and the choice is d3."
    
    content = "In this game, you are "
    content += "blue. " if blue else "orange. "
    content += "What is the best possible move for you?\n"
    if turns <= 20:
        content += "You have "
        if blue:
            num = (20 - turns)/2
            content += str(num)
        else:
            num = (20 - turns + 1)/2
            content += str(num)
        content += " pieces on hand\n"
    else:
        content += "You don't have any pieces on hand\n"
    
    content += "The board is as follows: (1 is your man, 0 is empty, -1 is the opponent's man\n"
    content += printBoard(board)
    content += "You just need to give out the move, nothing else"

    sys_instruct = instruction
    client = genai.Client(api_key=api_key)

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        config=types.GenerateContentConfig(
            system_instruction=sys_instruct),
        contents=[content]
    )
    # return (response.text[0:8])
    return makeRandomMove(board, turns, blue)

def main():
    board = [[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0, 0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0]]
    blue = True
    myTurn = False
    turns = 0
    game_input = input().strip()
    if game_input == "blue":
        myTurn = True
    else:
        blue = False
    while True:
        try:
            if (myTurn):
                start = time.time()
                move = makeMove(board, turns, blue)
                end = time.time()
                if (end - start < 4):
                    time.sleep(4 - end + start)
                turns += 1
                print(move, flush = True)
                board = changeBoard(board, move, 1)
                myTurn = False
            
            else:
                move = input().strip()
                board = changeBoard(board, move, -1)
                myTurn = True
                turns += 1
        except EOFError:
            break

if __name__ == "__main__":
    main()