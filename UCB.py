from func import pro
import numpy as np
import random

from modules import initial_infomation_gathering
from modules import cal_expected_value
from modules import update_expected_value
from modules import extra_try



pro_num = 1#取り扱うベンチマーク問題の種類を指定
slot_num_max = 4#スロットの種類が何種あるか指定


trial_num = 5

end_time = 100

def cal_CI(totalN0,n0):
    """
    CIはConfidence Intervalの略称，意味は信頼区間
    この関数は信頼区間を求める関数
    totalNは（全スロットの）総プレイ回数
    nは１つスロットのプレイ回数 
    """
    UI0 = 2*np.sqrt(totalN0)/n0

    return UI0

def cal_Upside_expected_value(record0,expected_value0,totalN0):
    """
    スロット記録より，信頼区間上，最も上振れた場合の(1つのスロットの)期待値を計算する
    record0:1スロット分の記録
    """
    Confidence_Interval = cal_CI(totalN0,len(record0))
    upside_expected0 = expected_value0 + Confidence_Interval#信頼区間の上限値を算出

    return upside_expected0 , Confidence_Interval


def check_best_upslot(up_expected_values0):
    #信頼区間上限値が最も高いスロットを探索する
    best_slot = 0
    best_upexpected = 0#1番良い信頼区間上限値のスロット
    best2_upexpected = 0#2番目に良い信頼区間上限値のスロット
    first_changed = False
    #2番目に良い期待値を見つけるため(1回目に現在の最良値を見つけたとき，一旦bestに，2回目より2番目となったものをbest2に入れる)
    for i in range(len(up_expected_values0)):
        if best_upexpected < up_expected_values0[i]:
            best_slot = i
            if first_changed == True:
                best2_upexpected = best_upexpected
                best_upexpected = up_expected_values0[i]
            elif first_changed == False:
                best_upexpected = up_expected_values0[i]
                first_changed = True

        elif best2_upexpected < up_expected_values0[i]:
            best2_upexpected = up_expected_values0[i]
    #print(best_slot)
    return best_slot , best_upexpected , best2_upexpected


def UCB():
    total_reward = 0
    records , total_reward , expected_values , total_values = initial_infomation_gathering(total_reward,trial_num)
    #全てのスロットを１回ずつ回し，各スロットの報酬値をrecordsに記録
    totalN = slot_num_max * trial_num#各スロットの回した合計回数を記録

    up_expected_values = []#信頼区間の上限値を記録する空リストを作成
    CIs = []
    for i in range(slot_num_max):#㊟スロット１の信頼区間の上限値はup_expected_values[0]に記憶，２は[1]に...
        upside_expected , CI = cal_Upside_expected_value(records[i],expected_values[i],totalN)
        up_expected_values.append(upside_expected)
        CIs.append(CI)
    #信頼区間上限値リスト作成完了
    
    checked = False

    for i in range(end_time - slot_num_max * trial_num):#試行回数上限値までスロットを回す
        
        if checked == False:#調査フラグが立っている場合は，1番，2番の期待値，１番目のスロット番号を抽出
            bestupslot , best_upexpected , best2_upexpected = check_best_upslot(up_expected_values)
            checked = True
            #print(bestupslot)
        #現時点で最適なスロットを選ぶ

        records , total_values , total_reward = extra_try(records,total_values,total_reward,bestupslot)
        totalN += 1

        expected_values  = update_expected_value(records,expected_values, total_values, bestupslot)
        #更新した記録より，期待値を更新
        for i in range(slot_num_max):
            up_expected_values[i] , CIs[i] =  cal_Upside_expected_value(records[i],expected_values[i],totalN)
            if i == bestupslot:
                best_upexpected = up_expected_values[bestupslot]

                
        #print(total_reward)
        #print(expected_values)
        #print(best_upexpected)
        #print(best2_upexpected)
        print(CIs)

        if best_upexpected < best2_upexpected:#2番目を下回った場合は，調査フラグを立てる
            checked = False
            #print("False")
    #print(len(records[0]), len(records[1]) , len(records[2]) , len(records[3]))

    return total_reward