from google import genai
from google.genai import types
import os
from dotenv import load_dotenv
import time


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

def makeMove(board, turns, blue, isSecond=0):
    if isSecond==1:
        instruction = "You just answered incorrectly, please try again." 
    else: instruction = ""
    
    instruction += "Please return the answer in 4.5 seconds"
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
    
    content += "The board is as follows: (1 is your man, 0 is empty, -1 is the opponent's man)\n"
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
    
    move = response.text[0:8]
    
    parts = move.strip().split()
    if len(parts) != 3:
        return False

    source, target, remove = parts
    
    if (is_valid_move(board=board, source=source, target=target, remove=remove, blue=blue)):
        return makeMove(board, turns, blue, 1)
        
    return (response.text[0:8])

def is_valid_move(board, source: str, target: str, remove: str, blue: bool) -> (bool, str):
    """Validate move according to game rules.

    Args:
        board: The current state of the board (7x3 with a special row).
        source: Starting position of stone ('h1' or 'h2' if from hand).
        target: Target position for stone placement/movement.
        remove: Position of opponent's stone to remove ('r0' if none).
        blue: Boolean indicating if the player is blue.

    Returns:
        (bool, str): True if move is valid, False with reason if not.
    """
    invalid_fields = {
        "a2", "a3", "a5", "a6", "b1", "b3", "b5", "b7",
        "c1", "c2", "c6", "c7", "d4", "e1", "e2", "e6", "e7",
        "f1", "f3", "f5", "f7", "g2", "g3", "g5", "g6",
    }

    # Convert positions to board indices
    source_idx = moveToIndex(source)
    target_idx = moveToIndex(target)
    remove_idx = moveToIndex(remove)

    # Validate target position
    if target in invalid_fields or not (0 <= target_idx[0] < 7 and 0 <= target_idx[1] < 3):
        return False, f"Invalid move: Target position {target} does not exist on the board."

    if board[target_idx[0]][target_idx[1]] != 0:
        return False, f"Invalid move: Target position {target} is already occupied."

    # Validate source position
    if source in ["h1", "h2"]:  
        # Hand move validation
        correct_hand = "h1" if blue else "h2"
        if source != correct_hand:
            return False, f"Invalid move: Player tried to use opponent's hand ({source})."
    else:
        if source in invalid_fields or not (0 <= source_idx[0] < 7 and 0 <= source_idx[1] < 3):
            return False, f"Invalid move: Source position {source} does not exist on the board."

        if board[source_idx[0]][source_idx[1]] != (1 if blue else -1):
            return False, f"Invalid move: Player tried to move opponent's stone from {source}."

        # Check adjacency rule unless in phase 3
        if checkSpacesState(board, 1 if blue else -1) > 3:
            if abs(source_idx[0] - target_idx[0]) > 1 or abs(source_idx[1] - target_idx[1]) > 1:
                return False, f"Invalid move: Must move to adjacent position when you have more than 3 pieces."

    # Validate remove position
    if remove != "r0":
        if remove in invalid_fields or not (0 <= remove_idx[0] < 7 and 0 <= remove_idx[1] < 3):
            return False, f"Invalid move: Cannot remove stone - position {remove} does not exist."

        if board[remove_idx[0]][remove_idx[1]] == 0:
            return False, f"Invalid move: Cannot remove stone - position {remove} is empty."

        if board[remove_idx[0]][remove_idx[1]] == (1 if blue else -1):
            return False, f"Invalid move: Player tried to remove their own stone at {remove}."

    return True, "Valid move"


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