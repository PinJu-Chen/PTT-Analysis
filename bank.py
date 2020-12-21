import pandas as pd
import numpy as np

raw = pd.read_csv("buytogether_version2.csv")
# print(raw.info())

# 針對content欄& date欄: df
import re
df = raw[["content" , "date"]]

# 從date中取出year
df_year = pd.DataFrame(df["date"].str.split(" ").str.get(-1).str.title())  # 是一個object
df_content = pd.DataFrame(df["content"])
df_all = pd.concat([df_year, df_content], axis = 1)

# mutate一欄銀行（Pandas DataFrame columns are Pandas Series when you pull them out）
content = df_all['content'].tolist()  # content is now a list
# convert every item in content into string
content_str = []
for i in content:
    if type(i) == list:
        tostr = ''.join(i)
        content_str.append(tostr)
    elif type(i) == str:
        content_str.append(i)
    else:
        content_str.append("NA")

payment = []  # list中的每個item如果有抓到付（匯）款銀行，就存入
pattern = re.compile("收款銀行：(\w+)+\s")  # 抓取收款銀行後面的字元，直到出現空白
for i in content_str:
    bank = pattern.findall(i)
    if len(bank) > 0:
        payment.append(bank[0])
    else:
        payment.append("NA")
# 處理payment這個list，再轉為column：統一銀行名稱
# 郵局 國泰 玉山 台新 中信 土地 永豐 第一 王道 兆豐 台灣 彰化 星展 上海 富邦 台灣企銀 新光商銀 花旗 元大 華南
# 遠東 渣打 凱基 大眾 合作 安泰
# Line 街口 面交 貨到付款 PC
# detect到 就新增以上統一名至另一欄
bank = []
for i in payment:
    if '郵局' in i:
        bank.append('郵局')
    elif '國泰' in i:
        bank.append('國泰')
    elif '玉山' in i:
        bank.append('玉山')
    elif '台新' in i:
        bank.append('台新')
    elif '中信' in i:
        bank.append('中信')
    elif '土地' in i:
        bank.append('土地')
    elif '永豐' in i:
        bank.append('永豐')
    elif '第一' in i:
        bank.append('第一')
    elif '王道' in i:
        bank.append('王道')
    elif '兆豐' in i:
        bank.append('兆豐')
    elif '台灣' in i:
        bank.append('台灣')
    elif '臺灣' in i:
        bank.append('台灣')
    elif '彰化' in i:
        bank.append('彰化')
    elif '星展' in i:
        bank.append('星展')
    elif '上海' in i:
        bank.append('上海')
    elif '富邦' in i:
        bank.append('富邦')
    elif '台灣企銀' in i:
        bank.append('台灣企銀')
    elif '新光商銀' in i:
        bank.append('新光商銀')
    elif '花旗' in i:
        bank.append('花旗')
    elif '元大' in i:
        bank.append('元大')
    elif '華南' in i:
        bank.append('華南')
    elif '遠東' in i:
        bank.append('遠東')
    elif '渣打' in i:
        bank.append('渣打')
    elif '凱基' in i:
        bank.append('凱基')
    elif '大眾' in i:
        bank.append('大眾')
    elif '合作' in i:
        bank.append('合作')
    elif '安泰' in i:
        bank.append('安泰')
    elif 'line' in i:
        bank.append('line')
    elif '街口' in i:
        bank.append('街口')
    elif '面交' in i:
        bank.append('面交')
    elif '貨到付款' in i:
        bank.append('貨到付款')
    elif 'PC' in i:
        bank.append('PC')
    else:
        bank.append(i)
print(bank)

'''
df_all['payment'] = payment
df_final = df_all[["date", "payment"]]  # 可以拿來畫圖的兩欄
print(df_final)
'''



