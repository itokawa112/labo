import random

"""
    ベンチマーク問題として，いくつかの仮想スロットマシーンを用意する
    各スロットマシーンは一回の試行で得られる報酬が決まっている
    報酬の詳細としては，払い戻し率
"""

def pro1(slot_num):#払い戻し率のみ違うベンチマーク問題
    """
    報酬は統一して当たれば１，外れれば０
    スロットマシーンを回して当たりが出る確率は
    スロット１：20％
    スロット２：30％
    スロット３：40％
    スロット４：50％
    """
    randnum = random.random()#不動小数点ありで０～１の区間でランダムな値を取る
    reward = 0 #当たらない時の基本報酬である０を設定しておく

    if slot_num == 0:#１つ目のスロットマシーンならば払い戻し率は0.2
        if randnum <= 0.2:
            reward = 1
    
    elif slot_num == 1:#２つ目のスロットマシーンならば払い戻し率は0.3
        if randnum <= 0.3:
            reward = 1

    elif slot_num == 2:#３つ目のスロットマシーンならば払い戻し率は0.4
        if randnum <= 0.4:
            reward = 1

    elif slot_num == 3:#４つ目のスロットマシーンならば払い戻し率は0.5
        if randnum <= 0.5:
            reward = 1
        
    return reward


def pro(pro_num,slot_num):
    if pro_num == 1:
        reward = pro1(slot_num)

    return reward