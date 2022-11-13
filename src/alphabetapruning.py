from math import inf
import random

HUMAN_MARK = 'X'
COMPUTER_MARK = 'O'

HUMAN = -1
COMPUTER = 1

GRIDSIDELEN = 3


def createEmptyBoard():
    return [[0 for _ in range(GRIDSIDELEN)] for _ in range(GRIDSIDELEN)]


def grid_index_to_row_and_col(index):
    return index // GRIDSIDELEN, index % GRIDSIDELEN


def print_board(board):
    boardStr = ""

    for row in board:
        for cell in row:
            if cell == HUMAN:
                boardStr += HUMAN_MARK
            elif cell == COMPUTER:
                boardStr += COMPUTER_MARK
            else:
                boardStr += " "

            boardStr += " | "

        boardStr = boardStr[:-3] + "\n"

    print(boardStr + "\n")


def get_winning_space_values(board):
    # column space
    columnValues = [0 for _ in range(GRIDSIDELEN)]

    for y in range(GRIDSIDELEN):
        for x in range(GRIDSIDELEN):
            columnValues[x] += board[y][x]

    # row space
    rowValues = [0 for _ in range(GRIDSIDELEN)]

    for y in range(GRIDSIDELEN):
        for x in range(GRIDSIDELEN):
            rowValues[y] += board[y][x]

    # diagonals
    diagonalValues = [0 for _ in range(2)]
    maxIndex = GRIDSIDELEN - 1

    for y in range(GRIDSIDELEN):
        positiveSlopeDiagonal = maxIndex - y

        for x in range(GRIDSIDELEN):
            if x == y: # negative slope diagonal
                diagonalValues[0] += board[y][x]

            if positiveSlopeDiagonal == x: # positive slope diagonal
                diagonalValues[1] += board[y][x]

    return columnValues, rowValues, diagonalValues


def isBoardFull(board):
    for row in board:
        for cell in row:
            if cell == 0:
                return False

    return True


def AI_win(board):
    valueSpaces = get_winning_space_values(board)

    for currentSpace in valueSpaces:
        for score in currentSpace:
            if score == 3: # positive 3 bc the ai is positive 1
                return True

    return False


def AI_lose(board): 
    valueSpaces = get_winning_space_values(board)

    for currentSpace in valueSpaces:
        for score in currentSpace:
            if score == -3: # negative 3 bc the human is negative 1
                return True

    return False


def is_draw(board):
    return isBoardFull(board) and not AI_win(board) and not AI_lose(board)


def game_over(board):
    return AI_win(board) or AI_lose(board) or is_draw(board)


def human_turn(board):
    while True:
        move = int(input('Which cell do you want to place an "X" in? (Type a number 1 through 9): '))

        if move >= 1 and move <= 9:
            coord = grid_index_to_row_and_col(move - 1)

            if board[coord[0]][coord[1]] == 0: # cant choose occupied cell
                board[coord[0]][coord[1]] = HUMAN
                break


def isBoardEmpty(board):
    for row in board:
        for cell in row:
            if cell != 0:
                return False

    return True


def countEmptyCells(board):
    cells = 0

    for row in board:
        for cell in row:
            if cell == 0:
                cells += 1

    return cells


def ai_turn(board):
    if isBoardEmpty(board):
        x = random.choice(range(GRIDSIDELEN))
        y = random.choice(range(GRIDSIDELEN))
    else:
        move = alphabetapruning(board, countEmptyCells(board), COMPUTER, -inf, inf)
        x = move[0]
        y = move[1]

    board[y][x] = COMPUTER


def alphabetapruning(board, depth, player, alpha, beta):
    """
    returns x, y, score
    """

    # evaluate
    if AI_win(board):
        return [-1, -1, depth]
    if AI_lose(board):
        return [-1, -1, -depth]
    if is_draw(board):
        return [-1, -1, 0]

    bestScore = None

    if player == COMPUTER: # when it is AI, it is maximizer
        bestScore = [-1, -1, -inf]
    else: # when is is human player, it is minimizer
        bestScore = [-1, -1, inf]

    for y in range(GRIDSIDELEN):
        for x in range(GRIDSIDELEN):
            if board[y][x] == 0:
                board[y][x] = player
                score = alphabetapruning(board, depth - 1, -player, alpha, beta)
                board[y][x] = 0

                # set the cell location
                score[0] = x
                score[1] = y

                # compare the score
                if player == COMPUTER:
                    if score[2] > bestScore[2]:
                        bestScore = score

                    if alpha < bestScore[2]:
                        alpha = bestScore[2]
                else:
                    if score[2] < bestScore[2]:
                        bestScore = score

                    if beta > bestScore[2]:
                        beta = bestScore[2]

                if beta <= alpha:
                    return bestScore

    return bestScore


def main():
    print("You are X\nThe AI is O\nThe cells of the tic tac toe grid are labeled 1 through 9 starting from the top left corner\n")

    firstTurn = random.randint(0, 1)
    board = createEmptyBoard()

    if firstTurn == 0:
        print("You go first")
    else:
        print("The AI went first")
        ai_turn(board)

    print_board(board)

    while not game_over(board):
        human_turn(board)
        print_board(board)

        if not game_over(board):
            ai_turn(board)

            print_board(board)
        else:
            break

if __name__ == "__main__":
    main()
