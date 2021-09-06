import pandas as pd
import random

# 棋士情報
kishi_no = [131, 175, 182, 183, 235, 264, 276, 307]
kishi_name = ["谷川", "羽生", "佐藤", "森内", "渡辺", "豊島", "永瀬", "藤井"]
kishi_rank = [9] * len(kishi_name)

# タイトル情報
title_name = ["竜王", "名人", "叡王", "王位", "王座", "棋王", "王将", "棋聖"]
holder = ["豊島", "渡辺", "豊島", "藤井", "永瀬", "渡辺", "渡辺", "藤井"]
prize = [4320, 2250, 2000, 1200, 1200, 900, 800, 700]

# 永世称号情報
title_ = ["竜王", "竜王", "名人", "名人", "名人", "叡王", "王位", "王座", "棋王", "棋王", "王将", "棋聖", "棋聖"]
holder_ = ["羽生", "渡辺", "羽生", "谷川", "森内", "", "羽生", "羽生", "羽生", "渡辺", "羽生", "羽生", "佐藤"]
year_ = [2017, 2008, 2008, 1997, 2007, "", 1997, 1996, 1995, 2017, 2006, 1995, 2006]

# 棋戦情報
kisen_list = ["竜王", "順位", "叡王", "王位", "王座", "棋王", "王将", "棋聖"]
kisen_dc = {}
for i, k in enumerate(kisen_list):
    kisen_dc[k] = i
    
# 各データDataFrame作成
df_kishi = pd.DataFrame(
    [x for x in zip(kishi_no, kishi_name, kishi_rank)],
    columns=["棋士番号", "棋士名", "段位"],
)

df_title = pd.DataFrame(
    [x for x in zip(title_name, holder, prize)],
    columns=["タイトル", "保持者","賞金"],
)

df_eternal_title = pd.DataFrame(
    [x for x in zip(title_, holder_, year_)],
    columns=["タイトル", "保持者", "取得年"],
)


players = random.sample(kishi_name, 2)
kisen = random.sample(kisen_list, 1)[0]

p1 = players[0]
p2 = players[1]


#p1 = input('対局者1:')
#p2 = input('対局者1:')
#kisen = input('棋戦：')

# 対局者のタイトル保持数
df_1 = df_title[df_title["保持者"] == p1]
df_2 = df_title[df_title["保持者"] == p2]
c1 = df_1.タイトル.count()
c2 = df_2.タイトル.count()

# 当該棋戦のタイトル保持者
t = title_name[kisen_dc[kisen]]
kisen_title1 = df_1[df_1["タイトル"] == t].タイトル.count()
kisen_title2 = df_2[df_2["タイトル"] == t].タイトル.count()

honor = ""

# 八大タイトルの防衛戦ルール(最優先)
if kisen_title1 == 1:
    honor = p1
elif kisen_title2 == 1:
    honor = p2
else:

    if c1 > 0 and c2 > 0:
        # 両者タイトル保持者の場合
        strong_title_1 = df_1.query('タイトル in ["名人", "竜王"]').タイトル.count()
        strong_title_2 = df_2.query('タイトル in ["名人", "竜王"]').タイトル.count()

        if strong_title_1 > strong_title_2:
            honor = p1
        elif strong_title_1 < strong_title_2:
            honor = p2
        elif strong_title_1 > 0 and strong_title_2 > 0:
            # 両者保持の名人、竜王をそれぞれ保持している場合
            # タイトル数の多いほうが上座
            if c1 > c2:
                honor = p1
            elif c1 < c2:
                honor = p2
            else:
                # タイトル数が同じ場合
                if not (c1 == 1 and c2 == 1):
                    # 名人、竜王以外のタイトルを持っている場合    
                    # 賞金の多いほうが上座
                    sum1 = df_1.賞金.sum()
                    sum2 = df_2.賞金.sum()
                    if sum1 > sum2:
                        honor = p1
                    elif sum1 < sum2:
                        honor = p2
                else:
                    # 名人、竜王以外のタイトルを持っていない場合
                    # 棋士番号の少ないほうが上座
                    kishi_no_1 = int(df_kishi[df_kishi["棋士名"] == p1].棋士番号)
                    kishi_no_2 = int(df_kishi[df_kishi["棋士名"] == p2].棋士番号)
                    if kishi_no_1 < kishi_no_2:
                        honor = p1
                    else:
                        honor = p2
        else:
            # 両者竜王、名人を保持していない場合
            # タイトル数の多いほうが上座
            if c1 > c2:
                honor = p1
            elif c1 < c2:
                honor = p2
            else:
                # 賞金の多いほうが上座
                sum1 = df_1.賞金.sum()
                sum2 = df_2.賞金.sum()
                if sum1 > sum2:
                    honor = p1
                elif sum1 < sum2:
                    honor = p2

    elif (c1 > 0 and c2 == 0) or (c2 > 0 and c1 == 0):
        # 片方のみタイトルを持つ場合
        if c1 > c2:
            honor = p1
        elif c1 < c2:
            honor = p2

    else:
        # 両者タイトルを持たない場合
        # 永世称号を持つほうが上座
        e1 = df_eternal_title[df_eternal_title["保持者"] == p1].タイトル.count()
        e2 = df_eternal_title[df_eternal_title["保持者"] == p2].タイトル.count()
        if e1 > 0 and e2 == 0:
            honor = p1
        elif e1 == 0 and e2 > 0:
            honor = p2
        elif e1 > 0 and e2 > 0:
            
            # 両者永世称号を保持している場合、先に資格を得たほうが上座
            get_year1 = min(df_eternal_title[df_eternal_title["保持者"] == p1].取得年)
            get_year2 = min(df_eternal_title[df_eternal_title["保持者"] == p2].取得年)
            
            if get_year1 > get_year2:
                honor = p2
            elif get_year1 < get_year2:
                honor = p1
            else:
                # 棋士番号の少ないほうが上座
                kishi_no_1 = int(df_kishi[df_kishi["棋士名"] == p1].棋士番号)
                kishi_no_2 = int(df_kishi[df_kishi["棋士名"] == p2].棋士番号)
                if kishi_no_1 < kishi_no_2:
                    honor = p1
                else:
                    honor = p2
            
        else:
            # 両者資格を持たない場合
            # 段位が上のほうが上座
            rank_1 = int(df_kishi[df_kishi["保持者"] == p1].段位)
            rank_2 = int(df_kishi[df_kishi["保持者"] == p2].段位)
        
            if rank_1 > rank_2:
                honor = p1
            elif rank_1 < rank_2:
                honor = p2
            else:
                # 段位が同じ場合、棋士番号の少ないほうが上座
                kishi_no_1 = int(df_kishi[df_kishi["棋士名"] == p1].棋士番号)
                kishi_no_2 = int(df_kishi[df_kishi["棋士名"] == p2].棋士番号)
                if kishi_no_1 < kishi_no_2:
                    honor = p1
                else:
                    honor = p2
if honor == p1:
    other = p2
else:
    other = p1

print(f'対局者1：{p1} 対局者2：{p2} 棋戦：{kisen}戦')
print(f'上座：{honor} 下座：{other}')