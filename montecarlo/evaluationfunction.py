"""
評価関数を指定する関数を作る
評価は×を書く視点で書く
"""

import numpy as np
import pickle
import copy

#まずは，エージェントが起こした行動，盤面の認識ができるように設計する




def rewiew(gameboard0,action,gamestate):
    reward = 0
    reward1 = 0
    reward2 = 0
    reward3 = 0
    #まずはゲームの状態で分岐させる
    if gamestate == "win:A":#勝ったならば高報酬
        reward = 100
        print("win reward")
    elif gamestate == "win:B":#負けたならばマイナス評価
        reward = -100
        print("lose reward")

    elif gamestate == "normal":#勝敗がまだ決まってないならば，状況分析を行い評価

        #リーチ阻止できるか否かの評価を与える(ダブルリーチされたときのため，ひとつ阻止できたとして防げない選択をしたときにマイナスになるように調整)
        #すでにリーチ阻止できた場所も，評価対象とならないように，✖で埋められているか否かも確認必須
        for i in range(3):
            if (gameboard0[i][i] == "o" ) and gameboard0[np.mod(i+1,3)][np.mod(i+1,3)] == "o" and gameboard0[np.mod(i+2,3)][np.mod(i+2,3)] != "x":#右下がり斜めの判定
                if action == (np.mod(i+2,3),np.mod(i+2,3)):#ななめ阻止位置に置いたか判定
                    reward1 = 5
                    print("stop　右下がりリーチ")
                elif action != (np.mod(i+2,3),np.mod(i+2,3)):
                    reward2 = -15
                    print("pass 右下がりリーチ")
            if i == 0:
                a = 1
                b = 1
            elif i == 1:
                a = 0
                b = 2
            elif i == 2:
                a = 2
                b = 0
            if (gameboard0[np.mod(a-1,3)][np.mod(b+1,3)] == "o") and (gameboard0[np.mod(a-2,3)][np.mod(b+2,3)] == "o") and (gameboard0[a][b] != "x"):#右上がり斜め判定
                if action == (a,b):
                    reward1 = 5
                    print("stop 右上がりリーチ")
                elif action != (a,b):
                    reward2 = -15
                    print("pass 右上がりリーチ")
                    
            for j in range(3):
                if (gameboard0[i][j] == "o" ) and gameboard0[i][np.mod(j+1,3)] == "o" and gameboard0[i][np.mod(j+2,3)] != "x":#横側の判定
                    if action == (i,np.mod(j+2,3)):#横側阻止位置に置いたか判定
                        reward1 = 5
                        print("stop 横リーチ")
                    elif action != (i,np.mod(j+2,3)):
                        reward2 = -15
                        print("pass 横リーチ")

                if (gameboard0[i][j] == "o" ) and gameboard0[np.mod(i+1,3)][j] == "o" and gameboard0[np.mod(i+2,3)][j] != "x":#縦側の判定
                    if action == (np.mod(i+2,3),j):#縦側阻止位置に置いたか判定
                        reward1 = 5
                        print("stop 縦リーチ")
                    elif action != (np.mod(i+2,3),j):
                        reward2 = -15
                        print("pass 縦リーチ")

        #自分がリーチできるように選べたら報酬を与える
        for i in range(3):
            if (gameboard0[i][i] == "x" ) and gameboard0[np.mod(i+1,3)][np.mod(i+1,3)] == "x" and gameboard0[np.mod(i+2,3)][np.mod(i+2,3)] == 0:#右下がり斜めの判定
                if action == (np.mod(i+1,3) , np.mod(i+1,3)) or action == (i,i):#ななめ阻止位置に置いたか判定
                    reward3 = 3
                    print("右下がりリーチ！")

            if i == 0:
                a = 1
                b = 1
            elif i == 1:
                a = 0
                b = 2
            elif i == 2:
                a = 2
                b = 0
            if (gameboard0[np.mod(a-1,3)][np.mod(b+1,3)] == 0) and (gameboard0[np.mod(a-2,3)][np.mod(b+2,3)] == "x") and (gameboard0[a][b] == "x"):#右上がり斜め判定
                if action == (a,b) or action == (np.mod(a-2,3),np.mod(b+2,3)):
                    reward3 = 3
                    print("右上がりリーチ！")


        for i in range(3):            
            for j in range(3):
                if (gameboard0[i][j] == "x" ) and gameboard0[i][np.mod(j+1,3)] == "x" and gameboard0[i][np.mod(j+2,3)] == 0:#横側の判定
                    if action == (i,j) or action == (i,np.mod(j+1,3)):#横側阻止位置に置いたか判定
                        reward3 = 3
                        print("横リーチ！")


                if (gameboard0[i][j] == "x" ) and gameboard0[np.mod(i+1,3)][j] == "x" and gameboard0[np.mod(i+2,3)][j] == 0:#縦側の判定
                    if action == (i,j) or action == (np.mod(i+1,3),j):#縦側阻止位置に置いたか判定
                        reward3 = 3
                        print("縦リーチ！")

        reward = reward1 + reward2 + reward3

    return reward


def rewiew_o(gameboard0,action,gamestate):
    reward = 0
    reward1 = 0
    reward2 = 0
    reward3 = 0
    #まずはゲームの状態で分岐させる
    if gamestate == "win:B":#勝ったならば高報酬
        reward = 100
        print("なんで負けたのか明日まで考えといてください")
    elif gamestate == "win:A":#負けたならばマイナス評価
        reward = -100
        print("おめでとう")

    elif gamestate == "normal":#勝敗がまだ決まってないならば，状況分析を行い評価

        #リーチ阻止できるか否かの評価を与える(ダブルリーチされたときのため，ひとつ阻止できたとして防げない選択をしたときにマイナスになるように調整)
        #すでにリーチ阻止できた場所も，評価対象とならないように，✖で埋められているか否かも確認必須
        for i in range(3):
            if (gameboard0[i][i] == "x" ) and gameboard0[np.mod(i+1,3)][np.mod(i+1,3)] == "x" and gameboard0[np.mod(i+2,3)][np.mod(i+2,3)] != "o":#右下がり斜めの判定
                if action == (np.mod(i+2,3),np.mod(i+2,3)):#ななめ阻止位置に置いたか判定
                    reward1 = 5
                    print("O：stop　右下がりリーチ")
                elif action != (np.mod(i+2,3),np.mod(i+2,3)):
                    reward2 = -15
                    print("O:pass 右下がりリーチ")
            if i == 0:
                a = 1
                b = 1
            elif i == 1:
                a = 0
                b = 2
            elif i == 2:
                a = 2
                b = 0
            if (gameboard0[np.mod(a-1,3)][np.mod(b+1,3)] == "x") and (gameboard0[np.mod(a-2,3)][np.mod(b+2,3)] == "x") and (gameboard0[a][b] != "o"):#右上がり斜め判定
                if action == (a,b):
                    reward1 = 5
                    print("O:stop 右上がりリーチ")
                elif action != (a,b):
                    reward2 = -15
                    print("O:pass 右上がりリーチ")
                    
            for j in range(3):
                if (gameboard0[i][j] == "x" ) and gameboard0[i][np.mod(j+1,3)] == "x" and gameboard0[i][np.mod(j+2,3)] != "o":#横側の判定
                    if action == (i,np.mod(j+2,3)):#横側阻止位置に置いたか判定
                        reward1 = 5
                        print("O:stop 横リーチ")
                    elif action != (i,np.mod(j+2,3)):
                        reward2 = -15
                        print("O:pass 横リーチ")

                if (gameboard0[i][j] == "x" ) and gameboard0[np.mod(i+1,3)][j] == "x" and gameboard0[np.mod(i+2,3)][j] != "o":#縦側の判定
                    if action == (np.mod(i+2,3),j):#縦側阻止位置に置いたか判定
                        reward1 = 5
                        print("O:stop 縦リーチ")
                    elif action != (np.mod(i+2,3),j):
                        reward2 = -15
                        print("O:pass 縦リーチ")

        #自分がリーチできるように選べたら報酬を与える
        for i in range(3):
            if (gameboard0[i][i] == "o" ) and gameboard0[np.mod(i+1,3)][np.mod(i+1,3)] == "o" and gameboard0[np.mod(i+2,3)][np.mod(i+2,3)] == 0:#右下がり斜めの判定
                if action == (np.mod(i+1,3) , np.mod(i+1,3)) or action == (i,i):#ななめ阻止位置に置いたか判定
                    reward3 = 3
                    print("O:右下がりリーチ！")

            if i == 0:
                a = 1
                b = 1
            elif i == 1:
                a = 0
                b = 2
            elif i == 2:
                a = 2
                b = 0
            if (gameboard0[np.mod(a-1,3)][np.mod(b+1,3)] == 0) and (gameboard0[np.mod(a-2,3)][np.mod(b+2,3)] == "o") and (gameboard0[a][b] == "o"):#右上がり斜め判定
                if action == (a,b) or action == (np.mod(a-2,3),np.mod(b+2,3)):
                    reward3 = 3
                    print("O:右上がりリーチ！")


        for i in range(3):            
            for j in range(3):
                if (gameboard0[i][j] == "o" ) and gameboard0[i][np.mod(j+1,3)] == "o" and gameboard0[i][np.mod(j+2,3)] == 0:#横側の判定
                    if action == (i,j) or action == (i,np.mod(j+1,3)):#横側阻止位置に置いたか判定
                        reward3 = 3
                        print("O:横リーチ！")


                if (gameboard0[i][j] == "o" ) and gameboard0[np.mod(i+1,3)][j] == "o" and gameboard0[np.mod(i+2,3)][j] == 0:#縦側の判定
                    if action == (i,j) or action == (np.mod(i+1,3),j):#縦側阻止位置に置いたか判定
                        reward3 = 3
                        print("O:縦リーチ！")

        reward = reward1 + reward2 + reward3
    return reward



def inishape(record):
    data = []
    turn_length = len(record)
    turn_num = 0
    #まずはターンごとのユニット作成を行う
    for i in range(turn_length):
        if i == turn_num:
            turn_unit = []
            board_unit = []

            other_unit = [record[i][1:]]#行動，報酬格納箱生成

            board_unit.append(record[i][0])#盤面記録
            board_unit.append(other_unit)#行動，報酬記録

            turn_unit.append(board_unit)
        
        data.append(turn_unit)
        turn_num += 1

    return data


def adding_actionValueData(record,data):
    sus_data = copy.deepcopy(data)
    print(sus_data)
    #recordは1ゲームで取れた情報
    #record[ターン数][情報種別][(情報種によって変わる)]
    #例:record[2][1]は3ターン目の行動（選択行，列）を示している
    #例:record[4][0]は5ターン目のgameboard_rec(ターン開始時盤面)を示している
    #例:record[0][2]は1ターン目のreward(報酬値)を示している

    #dataは今までの蓄積情報
    #data[ターン数][0:ボード情報 or 1:他][情報種: 0:行動　1:報酬][(情報種によって変わる)]
    #ターン数の直後が盤面状態となり，情報種の上に繰り上げされていることに注意したい
    
    turn_length = len(record)
    turn_num = 0
    for i in range(turn_length):
        #ターン数によって分岐
        
        if i == turn_num:#0ターン（1ターン目）目から順に記録していく
            #まずはそのターンにおいて記録内容がこれまでのボード情報と同一であるのか判定させる
            board_nummax = len(sus_data[turn_num])#今までいくつの種類の盤面が観測されているのかチェック
            print(i,"ターン目の情報",sus_data[turn_num])
            print("盤面数",board_nummax)
            searched = False#一致するものが発見されたときにTrue
            recorded = False
            for j in range(board_nummax):#発見されている盤面と重複していないのか判別させる
                if j == 0:
                    print("recordの盤面",record[turn_num][0])
                print("データの盤面",sus_data[turn_num][j][0])

                if sus_data[turn_num][j][0] == record[turn_num][0]:#盤面重複判断
                    action_num = len(sus_data[turn_num][j][1])#その盤面において,かつて行動された選択肢の数だけ読み込む
                    for l in range(action_num):
                        action = record[turn_num][1]#iターン目の行動の読み込み
                        if action == sus_data[turn_num][j][1][l][0]:#行動が一致しているのか読み込む
                            sus_data[turn_num][j][1][l][1] = record[turn_num][2]#報酬値
                            searched = True
                            recorded = True
                    if searched == False:#同じ行動が見つからなかった場合，そのｊ盤面での行動，報酬値を記録
                        data[turn_num][j][1].append(record[turn_num][1:])#情報種別，行動以降を記録
                        recorded = True
            if recorded == False:#同じ盤面が見つからなかった場合，そのターンにおける，盤面，行動，報酬値を記録
                board_unit = []
                board_unit.append(record[turn_num][0])#まずは，盤面格納
                other_unit = [record[turn_num][1:]]#行動,報酬格納
                board_unit.append(other_unit)
                data[turn_num].append(board_unit)

        turn_num += 1
    return data


def changeboard_for_record(board):
    """
    マルのターンのとき，マルとバツを逆にして，記録内容を統一させる
    """
    rec_board = [[0,0,0],[0,0,0],[0,0,0]]
    #print("〇×逆転前",board)
    for i in range(3):
        for j in range(3):
            if board[i][j] == "o":
                rec_board[i][j] = "x"
            if board[i][j] == "x":
                rec_board[i][j] = "o"

    #print("〇×逆転後",rec_board)
    return rec_board 