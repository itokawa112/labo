def printboard(gameboard0):
    print(gameboard0[0])
    print(gameboard0[1])
    print(gameboard0[2])


def update_board(gameboard0,row,column,player):
    if player == "A":
        if gameboard0[row][column] == 0:
            gameboard0[row][column] = "x"
        elif gameboard0[row][column] != 0:
            print("error:gameboard[",row,"][",column,"] is selected")
    elif player == "B":
        if gameboard0[row][column] == 0:
            gameboard0[row][column] = "o"
        elif gameboard0[row][column] != 0:
            print("error:gameboard[",row,"][",column,"] is selected")
    
    return gameboard0

def updete_gamestate(gamestate,gameboard0,selected):
    
    if gameboard0[0][0] == "x" and gameboard0[1][1] == "x" and gameboard0[2][2] == "x":#右下がり斜めの判定
        gamestate = "win:A"
    if gameboard0[2][0] == "x" and gameboard0[1][1] == "x" and gameboard0[0][2] == "x":#右上がり斜めの判定
        gamestate = "win:A"

    for i in range(3):
        if gameboard0[i][0] == "x" and gameboard0[i][1] == "x" and gameboard0[i][2] == "x":#横判定
            gamestate = "win:A"
        if gameboard0[0][i] == "x" and gameboard0[1][i] == "x" and gameboard0[2][i] == "x":#縦判定
            gamestate = "win:A"

    if gameboard0[0][0] == "o" and gameboard0[1][1] == "o" and gameboard0[2][2] == "o":#右下がり斜めの判定
        gamestate = "win:B"
    if gameboard0[2][0] == "o" and gameboard0[1][1] == "o" and gameboard0[0][2] == "o":#右上がり斜めの判定
        gamestate = "win:B"

    for i in range(3):
        if gameboard0[i][0] == "o" and gameboard0[i][1] == "o" and gameboard0[i][2] == "o":#横判定
            gamestate = "win:B"
        if gameboard0[0][i] == "o" and gameboard0[1][i] == "o" and gameboard0[2][i] == "o":#縦判定
            gamestate = "win:B"


    if selected == 9 and gamestate == "normal":
        gamestate = "draw"

    return gamestate


def turn_change(selectplayer0):
    if selectplayer0 == "A":
        nextselectplayer = "B"
    elif selectplayer0 == "B":
        nextselectplayer = "A"

    return nextselectplayer