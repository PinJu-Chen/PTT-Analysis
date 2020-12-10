import json
import pandas as pd
import re

# 讀取json檔
with open('D:\\PCB\\buytogether_version2.json', 'r', encoding="utf-8") as f:
    data = json.loads(f.read())

# 建立list用以儲存json所需欄位
all_list = []
for i in range(len(data)):
    all_list.append([data[i]['a_ID'], data[i]['b_作者'],
                     data[i]['c_標題'], data[i]['d_日期'],
                     data[i]['e_ip'], data[i]['h_推文總數']['all'],
                     data[i]['f_內文']])

# 以list建立datafram，以方便後續繪圖
buy2df = pd.DataFrame(all_list, columns=['id','author','title','date','ip','likes','content'])


# 建立年月週資料
buy2df['year'] = buy2df['date'].apply(lambda x: x[20:24])
buy2df['month'] = buy2df['date'].apply(lambda x: x[4:7])
buy2df['week'] = buy2df['date'].apply(lambda x: x[0:4])

# 排除無法使用資料(星期正常，就不再處理)
yearlist = ['2020','2019','2018','2017','2016',
            '2015','2014','2013','2012','2011','2010']
buy2df = buy2df[buy2df['year'].isin(yearlist)]
                
monlist = ['Jan','Feb','Mar','Apr','May',
           'Jun','Jul','Aug','Sep','Oct',
           'Nov','Dec']
buy2df = buy2df[buy2df['month'].isin(monlist)]


# 排除無法使用資料
df = buy2df[(buy2df.author!='no author')|
            (buy2df.content!='main_content error')]

# 去除作者欄位暱稱
df['author'] = df.author.str.split(" ", n=1, expand=True)

df.to_csv(r'D:\PCB\rawdata.csv', index=False)

# 排除非團購文章
''''''
df1 = df[~(df.title.str.contains('公告')|
      df.title.str.contains('黑人')|
      df.title.str.contains('灰人')|
      df.title.str.contains('黑名單')|
      df.title.str.contains('判決'))]

# 非團購文章(用以做黑名單)
blackdf = df[(df.title.str.contains('黑人')|
          df.title.str.contains('灰人')|
          df.title.str.contains('黑名單')|
          df.title.str.contains('判決'))&
          (df.year.str.contains('2020')|
          df.year.str.contains('2019')|
          df.year.str.contains('2018')|
          df.year.str.contains('2017'))&
          (~df.title.str.contains('RE:'))&
          (~df.title.str.contains('Re:'))]

blackdf['ID_test'] = blackdf.title.str.replace('^.+?([a-zA-Z0-9]+).+$', r'\1')
'''
# 2020年各月次數
df1[(~df1.title.str.contains('無主'))&
    (df.year == '2019')].groupby('month').size()

df1[(df1.title.str.contains('無主'))&
    (df.year == '2020')].groupby('month').size()

# 2020年主揪top3
df1[(df1.year=='2020')&
    (~df.title.str.contains('無主'))].groupby('author').size().nlargest(5)
'''
         