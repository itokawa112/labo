from func import pro
import numpy as np
import random

slot_num_max = 4


def ini_search(records0):#入力された報酬記録から期待値を計算する（全スロット分）
    """現在の最も期待値が高いスロット㊟スロット１ならば0，スロット２ならば1，スロット３ならば2..."""
    expected_values0 = [0] * slot_num_max
    total_values0 = [0] * slot_num_max
    for i in range(slot_num_max):#初期期待値計算
        expected_values0[i] , total_values0[i] = cal_expected_value(records0[i])
       
    return expected_values0 , total_values0

def initial_infomation_gathering(total_reward0,trial_num,pro_num = 1,slot_num_max = 4):
    """
    初期操作で指定回数のスロットマシーンを引き，その結果をrecordsというリストに記録する
    """

    record_slot1 = []
    record_slot2 = []
    record_slot3 = []
    record_slot4 = []

    records0 = []
    #0行目にはスロット１の情報，1行目にはスロット２の情報，2行目にはスロット３の情報...

    for i in range(slot_num_max):#全スロットマシーンを初期試行回数分だけ回してみる
        for j in range(trial_num):#指定の試行回数trial_numだけ，各スロットマシーンを回す
            if i == 0:
                #iは何番目のスロットであるのかを表す
                #pro_numはスロット１：20％，２：30％…という設定の問題を取り扱っていることを表す
                reward = pro(pro_num , i)
                record_slot1.append(reward)
                
            elif i == 1:
                reward = pro(pro_num , i)
                record_slot2.append(reward)

            elif i == 2:
                reward = pro(pro_num , i)
                record_slot3.append(reward)

            elif i == 3:
                reward = pro(pro_num , i)
                record_slot4.append(reward)


            #print(reward)

            total_reward0 = total_reward0 + reward

    #recordsというリストに情報をまとめる，recordというリストにrecord_slot（スロット番号）というリストが入れられていることに注意
    records0.append(record_slot1)
    records0.append(record_slot2)
    records0.append(record_slot3)
    records0.append(record_slot4)

    expected_values0 , total_values0 = ini_search(records0)

    return records0 , total_reward0 , expected_values0 , total_values0


def cal_expected_value(list1):#入力された報酬記録から期待値を計算する（１スロット分）
    total_value = 0
    for i in range(len(list1)):#入力されたリストの総和を算出
        total_value += list1[i]
    expected_value = total_value / len(list1)#リストの要素数（そのスロット試行回数）で割って，期待値を求める
    return expected_value , total_value

def update_expected_value(records0,expected_values0,total_values0,slotnum0):#追加分の期待値更新

    expected_values0[slotnum0] = total_values0[slotnum0] / len(records0[slotnum0])#期待値更新

    return expected_values0 



def extra_try(records0 , total_values0 , total_reward0 , slotnum0 , pro_num = 1):
    reward = pro(pro_num , slotnum0)#追加分のスロット実行

    records0[slotnum0].append(reward)#リストを更新
    total_reward0 = total_reward0 + reward#総価値を更新
    total_values0[slotnum0] += reward#各スロットの総価値更新
    
    return records0 , total_values0 , total_reward0