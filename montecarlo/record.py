import pickle
import numpy as np
import random
import copy

win_reward = 100
lose_reward = -70
learning_rate = 0.4
Rate_of_decrease = 0.9#Rate_of_decrease割引率を表している


def reverselist(list0):
    print(list0)
    returnlist = []
    for i in range(len(list0)):
        returnlist.append(list0[-i-1])
    return returnlist


def convert_record(record,data0):
    #現在のプログラム動作：入れられた盤面・報酬値のデータから各盤面に対して報酬期待値をつけた記録に変換する
    #盤面報酬値を記録すべき数値へ変更するプログラム
    #turn_numは1~9ターン目のどれを算出対象としているのかを示す数値だが格納されている数値は0~8である点に注意 
    tbr_senko = 0#total_behind_reward以降の報酬合計値を割引率を適用した形で保持(先攻用)
    tbr_koko = 0#total_behind_reward以降の報酬合計値を割引率を適用した形で保持(後攻用)
    turn_length = len(record)
    #最終行動をどちらが行ったのか判断する
    recordforlearning = []

    data = copy.deepcopy(data0)

    #最終行動にてどちらかが勝利していた場合，一つ前の行動（敵の最終行動）に対して-100の報酬を与える
    if record[-1][1] == win_reward:#最終行動にて報酬値が勝利報酬を得ているならば…
        record[-2][1] += lose_reward

    boardvalue0 = 0

    #書き込み記録と過去の学習データのターン長を
    
    if len(data) < len(record):
        #recordを記録したいが，記録するためのturn_unitの数が足りないため，そのままではエラーが出る。これを防ぐためturn_unitの数を増やす
        lack_num = len(record) - len(data)#turnunitの不足数を取得
        for i in range(lack_num):
            data.append([])#不足しているターン数の分だけturnunitとして空リストを追加
    

    if np.mod(turn_length,2) == 0:#最後の選択エージェントが先攻であるのか判断,先攻が行動するのは奇数ターンで，turnnumは１ならば０偶数になることに注意が必要
        selectplayer = "senko"
        print("最後は先攻")
    else:#そうでなければ，選択エージェントは後攻
        selectplayer = "koko" 
        print("最後は後攻")
    for i in range(turn_length):
        board_unit = []
        #すでに学習されたことのある盤面であれば，その盤面報酬期待値を取得する
        boardfound = False
        if len(data) > 0:#dataが空のリストでなければ
            for board_num in range(len(data[turn_length-1-i])):#同ターンの学習データに，記録されている数だけ，繰り返す
                if record[turn_length-1-i][0] == data[turn_length-1-i][board_num][0]:#データの格納turnunitの方が大きい可能性があるので注意
                    boardaddress = board_num
                    boardvalue0 = data[turn_length-1-i][board_num][1]#該当盤面の報酬期待値を取得
                    boardfound = True
                    break
        if selectplayer == "senko":
            tbr_senko = tbr_senko * Rate_of_decrease + record[turn_length-1-i][1]#今までの合計後方報酬値に割引率を掛けて，現在の報酬を加算して，合計後方報酬値を更新
            boardvalue0 = (1 - learning_rate) * boardvalue0 + learning_rate * tbr_senko
            board_unit.append(record[turn_length-1-i][0])
            board_unit.append(boardvalue0)
            #board_unit.append(calperfection(record[turn_length - i][0],turn_length - i,learningdata))
            """            
            if boardfound == True:
                data[-i-1][boardaddress][1] = boardvalue0
            """
        else:
            tbr_koko = tbr_koko * Rate_of_decrease + record[turn_length-1-i][1]
            boardvalue0 = (1 - learning_rate) * boardvalue0 + learning_rate * tbr_koko
            board_unit.append(record[turn_length-1-i][0])
            board_unit.append(boardvalue0)
            #board_unit.append(calperfection(record[turn_length - i][0],turn_length - i,learningdata))
        recordforlearning.append(board_unit)
        
        #記録対象を先攻・後攻の入れ替えを行う
        if selectplayer == "senko":
            nextselectplayer = "koko"
        elif selectplayer == "koko":
            nextselectplayer = "senko"
        selectplayer = nextselectplayer

    recordforlearning = reverselist(recordforlearning)#エピソードを後ろから記録しているため，前後逆転させる

    for i in range(len(record)):
        recordforlearning[i].append(record[i][2])#入れ忘れていたので急遽行動本体のデータが必要になったため格納

    return recordforlearning


def episode_append(record,data):
    action_addresses = []
    board_addresses = []
    actionfound = False
    next_num_found = True

    #盤面報酬期待値record[turnn_num][1]が格納されていない

    #まずは，同じ盤面があるかの確認をおこなう
    for turn_num in range(len(record)):
        boarddatalength = len(data[turn_num])#データ内にあるボードの種類数を取得
        boardfound = False#同一盤面が見つからない場合はFalse，見つかったらTrue
        for i in range(boarddatalength):
            if record[turn_num][0] == data[turn_num][i][0]:#格納されている盤面データと一致しているとき
                if next_num_found == False:
                    data[turn_num-1][board_addresses[turn_num-1]][2][action_addresses[turn_num-1]].append(i)
                    next_num_found = True
                data[turn_num][i][1] = record[turn_num][1]#報酬値更新
                board_addresses.append(i)
                actionfound = False
                for j in range(len(data[turn_num][i][2])):
                    if record[turn_num][2] == data[turn_num][i][2][j][0]:
                        #行動自体と次番号については更新する必要はない，更新する必要があるものは行動期待値のみ
                        action_addresses.append(j)
                        actionfound = True
                if actionfound == False:
                    next_num_found = False
                    action_unit = []
                    action_unit.append(record[turn_num][2])
                    action_addresses.append(len(data[turn_num][i][2]))
                    data[turn_num][i][2].append(action_unit)#該当ターンのaction_unitsに新規action_unitを追加する

                boardfound = True
                #actionについて次盤面の盤面アドレスを追加して格納
                break
        if boardfound == False:#全てを検索しても同一盤面が見つからないとき
            if next_num_found == False:
                data[turn_num-1][board_addresses[turn_num-1]][2][action_addresses[turn_num-1]].append(boarddatalength)
                next_num_found = True
            board_unit = []
            next_num_found = False
            board_unit.append(record[turn_num][0])#盤面の状態を格納
            board_unit.append(record[turn_num][1])#盤面の報酬期待値を格納
            action_units = []
            action_unit = []
            action_unit.append(record[turn_num][2])
            action_units.append(action_unit)
            action_addresses.append(0)
            board_unit.append(action_units)
            data[turn_num].append(board_unit)#新規盤面の各種情報を入れる
            board_addresses.append(boarddatalength)

    return data , board_addresses , action_addresses


def add_record_to_data(record,data):
    #データ保存形式に変換された記録を学習データの中に加える
    #dataが⑴リストの場合，⑵既存のリスト長がrecordのリスト長より小さい場合，⑶大きい場合の3通りで書き分ける
    board_addresses = []
    action_addresses = []
    #print("record=",record)
    #print("data=",data)

    if len(data) == 0:
        #空のリストに初めての学習記録を加える
        #データ完成度を加えないならばそのまま入れてやればよい
        turn_length = len(record)
        for i in range(turn_length):
            turn_unit = []
            board_unit = []
            board_addresses.append(0)#1個も保存されてなければ，格納数は0で保存されるとき番号0に格納される

            board_unit.append(record[i][0])#盤面を格納

            board_unit.append(record[i][1])#盤面報酬期待値を格納

            action_units = []
            action_addresses.append(0)#新規保存する行動に対して，割り当てされているアドレスを格納,初期動作では利用しない
            action_unit = []
            action_unit.append(record[i][2])#行動を格納
            action_units.append(action_unit)
            board_unit.append(action_units)
            turn_unit.append(board_unit)
            #print("turnunit=",turn_unit)
            data.append(turn_unit)
            if i > 0:#（次番号格納のため）2ターン目以降のデータであれば
                #まだ，上書きされていない1ターン前の盤面アドレスを利用して，1ターン前のboardunitの新規保存された行動に対して次番号を格納する
                #print(i)
                #print(data)
                data[i-1][board_addresses[i-1]][2][action_addresses[i-1]].append(0)#新規保存される盤面のアドレスを格納,0のところは本来data[i]
                
                #data[ターン数][盤面アドレス][記録種別(0:gameboard,1:boardvalue,2:actionunit)][（actionunitであれば必要）0:行動,1:boardの次番号,2:行動報酬期待値]

    elif len(data) < len(record):
        #recordを記録したいが，記録するためのturn_unitの数が足りないため，そのままではエラーが出る。これを防ぐためturn_unitの数を増やす
        lack_num = len(record) - len(data)#turnunitの不足数を取得
        for i in range(lack_num):
            data.append([])#不足しているターン数の分だけturnunitとして空リストを追加
        #以降，turn_unitの数が足りている場合と同じ動作をすればよい
        data , board_addresses , action_addresses = episode_append(record,data)#１エピソードの情報をデータに加える

    else:#dataのturn_unitの数は足りているため単純に加えていけばよい
        data , board_addresses , action_addresses = episode_append(record,data)#１エピソードの情報をデータに加える
    #逆に言うとrecordのターン数が短い可能性がある点に注意したい
    #あらかじめ各行動に対して，報酬期待値を算出しておく
    #print("data=",data)
    for i in range(len(record)-2):
        if np.mod(i,2) == 0:#先攻の手版を学習対象としているため，限定を行う(1（奇数）ターン目がturn_num=0偶数であることに注意)
            #print(i,"ターン目を処理中")
            totalvalue = 0
            #勝敗が決まり，行動選択後に勝利報酬が得られていた場合，違う動作をしなければ，ならない可能性があるため，分岐させなければならない
            #print("boardaddress=",board_addresses)
            #この時点で，新規盤面がdataに追加されておらず，読み込めない
            #print(data[i+1][board_addresses[i+1]][2])
            for j in range(len(data[i+1][board_addresses[i+1]][2])):#1ターン後，遷移先の盤面にて選択されたことのある行動数だけ動作
                #選択行動にて動作が終了しているのか否かで分岐させる必要がある
                if len(data[i+1][board_addresses[i+1]][2][j]) < 2:#格納されているデータが行動本体のみで，次番号や行動報酬期待値が格納されていなければ
                    #その行動によって勝敗が決し，なおかつ，相手の行動で勝敗が決していることより，先攻は敗北していることより，負の期待値が与えられるべき
                    totalvalue += lose_reward
                else:
                    next_boardaddress = data[i+1][board_addresses[i+1]][2][j][1]#j番目の行動による次盤面の割り当てアドレスを取得
                    #print("next_boardaddress=",next_boardaddress)
                    #print("盤面報酬期待値data[i+2][next_boardaddress][1]=",data[i+2][next_boardaddress][1])
                    #2つ目のboardunitに行動報酬が入ってない
                    #print(data[i+2][next_boardaddress][1])
                    totalvalue += data[i+2][next_boardaddress][1]#盤面の報酬期待値を加算
                    #行動期待値を求める
            expected_value = totalvalue / len(data[i+1][board_addresses[i+1]][2])#平均にするため行動数で割る
            if len(data[i][board_addresses[i]][2][action_addresses[i]]) == 3:#行動期待値がすでに追加されており，appendで追加しなくてもよいならば，上書きによって更新
                data[i][board_addresses[i]][2][action_addresses[i]][2] = expected_value    
            else:#行動に対して，期待値が追加されておらず，行動・次番号のみならばappendで期待値を追加
                data[i][board_addresses[i]][2][action_addresses[i]].append(expected_value)
    return data