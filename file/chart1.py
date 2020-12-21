# 讀進檔案
import csv
with open(file = "buytogether_version2.csv", mode = "r", encoding = "utf-8") as buy:
    rows = csv.DictReader(buy)
    content = []
    for row in rows:
        content.append(row['content'])
# print(content)
# print(content[109])  # 隨便拿一筆出來看看長相

# 抓出付款方式
import re
payment = []  # list中的每個item如果有抓到付（匯）款銀行，就存入
pattern = re.compile("收款銀行：(\w+)+\s")  # 抓取收款銀行後面的字元，直到出現空白
for i in content:
    bank = pattern.findall(i)
    if len(bank) > 0:
        payment.append(bank[0])

# print(payment)
# print(len(payment))
# print(payment[10])

# 統一單一銀行的名字

# 整理付款方式
bank_rank = dict()  # 會放入以銀行名為key，出現次數為value
for i in payment:
    if i not in bank_rank:
        bank_rank[i] = 1
    else:
        bank_rank[i] += 1
print(payment, bank_rank)
