from operator import imod
from func import pro
import numpy as np
import random

from modules import initial_infomation_gathering
from modules import cal_expected_value
from modules import update_expected_value
from modules import extra_try

#from UCB import proposal

pro_num = 1#取り扱うベンチマーク問題の種類を指定,1は教科書通りの期待値設定の問題であることを表す。
slot_num_max = 4#スロットの種類が何種あるか指定
end_time = 100#greedy法

eps = 0.1#εgreedy法にて選択方法をランダムにする確率を設定

records = []
expected_values = []#期待値記録用のリストを作成
total_values = []
for i in range(slot_num_max):
    expected_values.append(0)
    total_values.append(0)

trial_num = 5#初期試行回数を設定

def check_best_slot(expected_values0):
    #期待値が最も高いスロットを探索する，2番目に期待値が高いスロットも確認し，最高期待値のスロットが変わっていないのかもチェック
    best_slot = 0
    best_expected = 0#1番良い期待値
    best2_expected = 0#2番目に良い期待値
    first_changed = False
    #2番目に良い期待値を見つけるため
    for i in range(len(expected_values0)):
        if best_expected < expected_values0[i]:
            best_slot = i
            if first_changed == False:
                best_expected = expected_values0[i]
                first_changed = True
            elif first_changed == True:
                best2_expected = best_expected
                best_expected = expected_values0[i]
        elif best2_expected < expected_values0[i]:
            best2_expected = expected_values0[i]
    #print(best_slot)
    return best_slot , best_expected , best2_expected


def greedy():#greedy法の実行プログラム本体
    total_reward = 0
    records , total_reward , expected_values , total_values = initial_infomation_gathering(total_reward,trial_num)
    #初期の情報収集を行う。総報酬も情報収集中に得られたものは更新
    #recordsは各スロットの全試行報酬情報が入ってる
    #初期情報より各スロットの期待値と総価値のリストを作成

    checked = False

    for i in range(end_time - trial_num * slot_num_max):

        if checked == False:#調査フラグが立っている場合は，1番，2番目に良い期待値を見てどちらが最高値を取っているのかチェックする
            best_slot , best_expected , best2_expected = check_best_slot(expected_values)
            checked = True
            #print(best_slot)
        #現時点で最適なスロットを選ぶ

        records , total_values , total_reward = extra_try(records,total_values,total_reward,best_slot)
        #最適なスロットを回し,記録を更新

        expected_values  = update_expected_value(records,expected_values, total_values, best_slot)
        #更新した記録より，期待値を再計算

        best_expected = expected_values[best_slot]
        #最良値の更新

        #print(expected_values)
        #print(total_reward)

        if best_expected < best2_expected:#2番目を下回った場合は，調査フラグを立てる
            checked = False
    #print(len(records[0]), len(records[1]) , len(records[2]) , len(records[3]))

    return total_reward

def eps_greedy():
    """
    初期試行を何度かやることは同じ，その後確率εでランダム選択
    """

    total_reward = 0
    records , total_reward , expected_values , total_values = initial_infomation_gathering(total_reward,trial_num)
    #初期情報収集

    #初期情報より各スロットの期待値と総価値のリストを作成

    checked = False

    for i in range(end_time):
        randnum = random.random()
        if checked == False:#調査フラグが立っている場合は，1番，2番の期待値，１番目のスロット番号を抽出
            best_slot , best_expected , best2_expected = check_best_slot(expected_values)
            checked = True
            #print(best_slot)
        #現時点で最適なスロットを選ぶ
        if randnum < eps:#確率εでランダム選択を行う
            rand_slotnum = random.randint(0,3)
            records , total_values , total_reward = extra_try(records,total_values,total_reward,rand_slotnum)
            #最適なスロットを回し,記録を更新
        else:#確率εに引っかからなければ最も期待値の良いスロットを引く
            records , total_values , total_reward = extra_try(records,total_values,total_reward,best_slot)
            #最適なスロットを回し,記録を更新

        expected_values  = update_expected_value(records,expected_values, total_values, best_slot)
        #更新した記録より，期待値を再計算

        best_expected = expected_values[best_slot]

        #print(expected_values)
        #print(total_reward)

        if best_expected < best2_expected:#2番目を下回った場合は，調査フラグを立てる
            checked = False
    #print(len(records[0]), len(records[1]) , len(records[2]) , len(records[3]))

    return total_reward

def numexp():
    #複数回試行して，総報酬値の平均，標準偏差を算出するプログラム
    exnum = 50#数値実験の回数
    rewardex = 0
    minmam = 0
    rewarddata = []
    for i in range(exnum):
        rewarddata.append(eps_greedy())#総報酬値算出するのにどのような手法を用いるのか選択している
        if i == 0:
            minmam = rewarddata[i]
        rewardex += rewarddata[i]
        if minmam > rewarddata[i]:
            minmam = rewarddata[i]
        

    exaverage = rewardex / exnum#総報酬値の平均を算出
    btotal = 0
    for i in range(exnum):
        b = rewarddata[i] - exaverage
        btotal += b
    bave = btotal / exnum

    print("総報酬の最低値（最も下振れたときの報酬値）",minmam)
    print("総報酬の平均",exaverage)
    print("標準偏差(総報酬値のばらつき)",bave)


#greedy()
#eps_greedy()
numexp()