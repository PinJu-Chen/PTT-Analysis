# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
from sklearn.datasets import load_iris
import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table


'''-------------------data-------------------'''
# test data
iris = load_iris() ## It returns simple dictionary like object with all data.
iris_df = pd.DataFrame(data=np.concatenate((iris.data,iris.target.reshape(-1,1)), axis=1), columns=(iris.feature_names+['Flower Type']))
iris_df["Flower Name"] = [iris.target_names[int(i)] for i in iris_df["Flower Type"]]

dfc = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder2007.csv')

# buytogether data
df = pd.read_csv(r'D:\PCB\rawdata.csv')


'''-------------------資料處理-------------------'''
# 主揪top3
dft = df[~(df.title.str.contains('公告')|
      df.title.str.contains('黑人')|
      df.title.str.contains('灰人')|
      df.title.str.contains('黑名單')|
      df.title.str.contains('判決')|
      df.title.str.contains('無主'))]
dft = pd.DataFrame(dft.groupby('author').count().nlargest(5, columns='id'))
dft['author'] = dft.index

# 黑名單
blackdf = df[(df.title.str.contains('黑人')|
          df.title.str.contains('灰人')|
          df.title.str.contains('黑名單')|
          df.title.str.contains('判決'))&
          ((df.year == 2020)|
          (df.year == 2019)|
          (df.year == 2018)|
          (df.year == 2017))&
          (~df.title.str.contains('RE:'))&
          (~df.title.str.contains('Re:'))]

blackdf['black_ID'] = blackdf.title.str.replace('^.+?([a-zA-Z0-9]+).+$', r'\1')


'''-------------------main------------------'''
# css
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# 建立app
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# 主標
header = html.H1(children="解析合購版",style={'font-weight': 'bold'})

# Top 3 table
top3 = dash_table.DataTable(
            id='top3',
            columns=[{"name": 'Top 3 Shopaholics', "id": 'author'}],
            data=dft.head(3).to_dict('records'),
            editable=False,
            style_header={
                'backgroundColor': 'rgb(230, 230, 230)',
                'fontWeight': 'bold'
                }
        )

# Blacklist table
blacklist = dash_table.DataTable(
                id='blacklist',
                columns=[{"name": 'Black_id', "id": 'black_ID'}],
                data=blackdf.to_dict('records'),
                filter_action="native",
                editable=False,
                page_size= 20,
                style_cell={'minWidth': 95, 'maxWidth': 95, 'width': 95},
                style_header={
                    'backgroundColor': 'rgb(230, 230, 230)',
                    'fontWeight': 'bold'
                    }
                )

# 時間軸
year_slider = dcc.RangeSlider(id='year_slider',
                              marks={
                                  2015: '2015',
                                  2016: '2016',
                                  2017: '2017',
                                  2018: '2018',
                                  2019: '2019',
                                  2020: '2020'},
                              min=2015,
                              max=2020,
                              value=[2017,2020],
                              className='ten columns')

# 以px繪製月份圖，並丟入dcc.Graph
chart1 = px.bar(x=df.groupby('month').size().index,
                y=df.groupby('month').size()/df.groupby('month').size().sum()*100,
                title="Month Percentage(%)",
                labels={"x":"Month",
                        "y":"Percentage(%)"},
                category_orders={"x": 
                                 ['Jan','Feb','Mar','Apr','May', 'Jun',
                                  'Jul','Aug','Sep','Oct','Nov','Dec']}
                )


graph1 = dcc.Graph(
        id='graph1',
        figure=chart1,
        className="five columns"
    )

# 以px繪製星期圖，並丟入dcc.Graph
chart2 = px.bar(x=df.groupby('week').size().index,
                y=df.groupby('week').size()/df.groupby('week').size().sum()*100,
                title="Week Percentage(%)",
                labels={"x":"Week",
                        "y":"Percentage(%)"},
                category_orders={"x": 
                                 ['Mon','Tue','Wed','Thu',
                                  'Fri', 'Sat', 'Sun']}
                )


graph2 = dcc.Graph(
        id='graph2',
        figure=chart2,
        className="five columns"
    )

# 以px繪製??圖，並丟入dcc.Graph
chart3 = px.histogram(data_frame=iris_df,
                      x="sepal length (cm)",
                      title="Producst Types")

graph3 = dcc.Graph(
        id='graph3',
        figure=chart3,
        className="five columns"
    )

# 以px繪製??圖，並丟入dcc.Graph
chart4 = px.box(data_frame=iris_df,
                x="Flower Name",
                y="sepal width (cm)",
                title="Payment Types")


graph4 = dcc.Graph(
        id='graph4',
        figure=chart4,
        className="five columns"
    )

# 版面配置
row0 = html.Div(children=[year_slider])
row_table = html.Div(children=[top3,blacklist], className="two columns")
row_graph = html.Div(children=[year_slider,graph1, graph2, graph3, graph4],
                     className='offset-by-three.column')
row1 = html.Div(children=[row_table, row_graph])


# 以html.Div建立layout物件
layout = html.Div(children=[header, row1],
                  style={"text-align": "center"})

# 將layout丟到app.layout才能在網頁輸出
app.title = '解析合購版'
app.layout = layout

# 執行
if __name__ == "__main__":
    app.run_server(debug=True)