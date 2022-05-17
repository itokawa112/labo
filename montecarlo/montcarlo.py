from asyncio import gather
from datetime import date
from operator import imod
import re
import numpy as np
import pickle
import copy
import random

import matplotlib.pyplot as plt

from gamecontrols import printboard, update_board, updete_gamestate , turn_change

from evaluationfunction import changeboard_for_record ,rewiew

from selectmethods import randomselect , rewardselect

from record import convert_record , add_record_to_data

win_reward = 100
lose_reward = -70
learning_rate = 0.4
Rate_of_decrease = 0.9#Rate_of_decrease割引率を表している

try:#該当ファイルがなければここでエラーが起きて，exceptへ移行する
    readmontedatafile = open("montedata.textfile","rb")
    print("ファイル発見")
    readmontedata = pickle.load(readmontedatafile)
except:
    print("該当ファイルなし。空のリストを新規作成します")
    readmontedata = []

def AgentA(gameboardA, selected , data , turn_num , gather , fight):
    if gather == True:#情報収集がしたいなら
        selectrow , selectcolumn = randomselect(gameboardA,selected)
    else:
        selectrow , selectcolumn = rewardselect(gameboardA,data,turn_num,selected,fight)

    return selectrow , selectcolumn

def AgentB(gameboardB,selected):

    selectrow , selectcolumn = randomselect(gameboardB,selected)

    return selectrow , selectcolumn

def monte(gather,fight):
    #モンテカルロ法
    gameboard = [[0,0,0],[0,0,0],[0,0,0]] 
    #gameboard_rec = copy.deepcopy(gameboard)
    gamestate = "normal"
    #shadowverse = random.randint(0,1)#先攻後攻を決める。１のときAgentAが先行，０で後攻(じゃんけん) 
    shadowverse = 1#先攻はA（x）固定
    selected = 0
    recording_record = []

    selectplayer = "null"
    #print(shadowverse)
    if shadowverse == 1:
        selectplayer = "A"
    elif shadowverse == 0:
        selectplayer = "B"

    for i in range(9):
        #print("更新前",gameboard_rec)
        gameboard_rec = copy.deepcopy(gameboard)
        #print("更新後",gameboard_rec)
        if selectplayer == "A":
            #selectrowA , selectcolumnA = AgentA(gameboard,selected)
            selectrowA , selectcolumnA = AgentA(gameboard,selected,readmontedata,i,gather,fight)
            gameboard = update_board(gameboard,selectrowA,selectcolumnA,selectplayer)
            selected += 1
        elif selectplayer == "B":
            selectrowB , selectcolumnB = AgentB(gameboard,selected)
            gameboard = update_board(gameboard,selectrowB,selectcolumnB,selectplayer)
            selected += 1
        #print(gameboard)

        gamestate = updete_gamestate(gamestate,gameboard,selected)

        if selectplayer == "A":#エージェントAに選択権があるなら..
            #recording_data = pickle.load(readfile)
            Action = (selectrowA,selectcolumnA)#選んだマス目を記録
            reward = rewiew(gameboard,Action,gamestate)
            """
            if gamestate == "win:A":
                reward = win_reward
            else:
                reward = 0
            """    
            #print(gameboard_rec)
            recording1 = [gameboard_rec,reward,Action]
            #recording1 = [gameboard_rec,reward]
            #print(recording1)
            recording_record.append(recording1)


        if selectplayer == "B":#エージェントBに選択権があるなら..
            Action = (selectrowB,selectcolumnB)
            #reward = rewiew_o(gameboard,Action,gamestate)

            if gamestate == "win:B":
                reward = win_reward
            else:
                reward = 0
                
            #gameboard_rec2 = changeboard_for_record(gameboard_rec)#マル，バツを逆にしてバツ主観の情報に統一し，記録種類は半分に減らす
            #recording1 = [gameboard_rec2,reward,Action]
            recording1 = [gameboard_rec,reward,Action]
            #recording1 = [gameboard_rec2,reward]
            #print(recording1)
            recording_record.append(recording1)



        if gamestate != "normal":
            #print(gameboard)
            #printboard(gameboard)
            #print(gamestate)
            #print(recording_record)


            writerecord = convert_record(recording_record,readmontedata)#一連の記録を取り終わったら，データ保存形式に変換


            try:#通常であれば，ファイル呼び出し，データ書き込み，保存
                montedatafile = open("montedata.textfile","rb")#該当ファイルがなければここでエラーが起きて，exceptへ移行する
                #print("ファイル発見")
                writemontedata = pickle.load(montedatafile)
                #print("発見データ内容",learningData)
                writemontedata = add_record_to_data(writerecord,readmontedata)#今までの学習記録に追加書き込み記録writerecordを追加する
                #montedata = adding_actionValueData(writedata,montedata)

                montedatafile = open("montedata.textfile","wb")
                #print("上書き内容",writerecord)
                pickle.dump(writemontedata,montedatafile)
                montedatafile.close
            except:#該当ファイルがなければ，初期動作
                print("該当ファイルが見つかりません。新規ファイルを作成します")
                montedatafile = open("montedata.textfile","wb")

                #iniwritedata = inishape(recording1)
                writemontedata = add_record_to_data(writerecord,readmontedata)#今までの学習記録に追加書き込み記録writerecordを追加する
                print("新規作成ファイルへの書き込み内容",writemontedata)
                pickle.dump(writemontedata,montedatafile)
                montedatafile.close
            break
        
        #print(selectplayer)
        selectplayer = turn_change(selectplayer)

    return gamestate

def playgamewinrate(fight):

    finalgenaration = 1000
    win = []
    winrate = []
    #当時，勝率を出すことに意味を見出していたが，最終的に最適解の選択を行いつづけると必ず引き分けになるため，敗北率が０になることを目指すべき
    gather = True
    #情報収集したければTrue，実戦時として情報収集をしなくていいならばFalse
    win_near100times = 0#直近の100回で何度勝利しているのかを格納する

    for generation in range(finalgenaration):
        state = monte(gather,fight)
        #勝敗をゲームを行って決める
        if state == "win:A":#先攻が勝利した場合
            win.append(1)
            win_near100times += 1
        elif state == "win:B":#後攻が勝利した場合
            win.append(0)
        else:#引き分けの場合
            win.append(0)
        if generation < 20:
            gather = False
        if generation < 100:
            winrate.append(win_near100 / (generation+1))
        else:
            win_near100 = win_near100 - win[generation - 100]

            winrate.append(win_near100 / 100)
    print(winrate)

def playgameloserate(fight):

    finalgenaration = 100


    #当時，勝率を出すことに意味を見出していたが，最終的に最適解の選択を行いつづけると必ず引き分けになるため，敗北率が０になることを目指すべき
    lose = []
    loserate = []

    gather = True
    #情報収集したければTrue，実戦時として情報収集をしなくていいならばFalse
    lose_near100 = 0#直近の100回で何度敗北しているのかを格納する

    for generation in range(finalgenaration):
        
        state = monte(gather,fight)
        #勝敗をゲームを行って決める

        if state == "win:B":#後攻が勝利した場合
            lose.append(1)
            lose_near100 += 1
        else:#引き分けの場合
            lose.append(0)
        if generation < 20:
            gather = False
        if generation < 100:
            loserate.append(lose_near100 / (generation+1))
        else:
            lose_near100 = lose_near100 - lose[generation - 100]
            #学習するため直近の100世代での敗北率を見たい

            loserate.append(lose_near100 / 100)
    if fight == True:
        print(loserate)

def main():
    fight = False#実戦モードの管理Falseは情報収集する，Trueは実戦モード
    gather_time = 4#何ユニット分のデータを集めるか？
    for i in range(gather_time):
        playgameloserate(fight)
    fight = True
    playgameloserate(fight)

main()