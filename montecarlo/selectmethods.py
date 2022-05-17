from email import policy
import random

#エージェントの行動方針を決めるプログラムを記載したスクリプト

def randomselect(gameboard0,selected):
    print("selected=",selected)
    selectnum = random.randint(1 , 9-selected)#１～（９引く選択されたマス数）で割り振られる選択候補をランダムに選ぶ
    count = 1
    flag = False
    for i in range(3):#0になっている場所をカウントアップしていき，指定値selectnumになったら，そのマスの行数・列数を記録して返す
        for j in range(3):
            if gameboard0[i][j] == 0:
                if count == selectnum:
                    pointrow = i
                    pointcolumn = j
                    flag = True
                    break
                else:
                    count += 1
        if flag == True:
            break

    return pointrow , pointcolumn

def rewardselect(gameboard0,data,turn_num,selected,fight):
    #見積もり報酬値が最も高いマス目を見つけてそのマスを選択する
    
    boardfound = False#同一盤面が見つからない場合はFalse，見つかったらTrue
    #記録されている同一盤面がないなら，期待値もないためランダム探索
    firstcontact = True
    total_expected = 0
    #確率epsでランダム探索，そうでなければ，報酬期待値が高い選択肢ほど選びやすくする
    eps = 0.2
    policy_num = random.random()#一定確率でランダム探索
    if fight == True:
        policy_num = 0#greedyにしたい場合はこちらを採用
    if policy_num < eps:
        pointrow , pointcolumn = randomselect(gameboard0,selected)
    else:#行動報酬期待値が高いものを選ぶ
        if turn_num > len(data):
            pointrow , pointcolumn = randomselect(gameboard0,selected)
        else:
            boarddatalength = len(data[turn_num])#データ内にあるボードの種類数を取得
            for board_num in range(boarddatalength):
                if gameboard0 == data[turn_num][board_num][0]:#格納されている盤面データと一致しているとき
                    #必ずアクセスする行動データに行動報酬値があるのかチェックをしなければならない
                    boardfound = True

                    #boardunit内のaction_units，この内の各action_unitに格納されている行動報酬期待値を総和を求める
                    for action_num in range(len(data[turn_num][board_num][2])):
                        if len(data[turn_num][board_num][2][action_num]) > 2:#actionunitに２つより多くの種別データが存在すればアクセスする
                            if firstcontact == True:#まだなにもbestactionへのアクセスがない場合，無条件で格納する
                                firstcontact = False
                                bestaction = data[turn_num][board_num][2][action_num][0]
                                best_act_expected = data[turn_num][board_num][2][action_num][2]

                            if best_act_expected < data[turn_num][board_num][2][action_num][2]:#現在格納されている行動より期待値が高いならば
                                bestaction = data[turn_num][board_num][2][action_num][0]
                    if firstcontact == False:#bestactionへのアクセスがあったのならば
                        pointrow , pointcolumn = bestaction
                    else:
                        pointrow , pointcolumn = randomselect(gameboard0,selected)
            if boardfound == False:
                pointrow , pointcolumn = randomselect(gameboard0,selected)
            
    return pointrow , pointcolumn




def epsgreedyselect(gameboard0,data,turn_num,selected):
    #まずは学習データに同じ盤面があるのかを検索
    eps = 0.10#ランダム探索をする確率
    policy_num = random.random()#どの方針で行うのか決定を行うために用いる確率変動値
    if policy_num < eps:#
        pointrow , pointcolumn = randomselect(gameboard0,selected)#ランダム探索を行う
    else:
        pointrow , pointcolumn = rewardselect(gameboard0,selected)
    
    return pointrow , pointcolumn



            