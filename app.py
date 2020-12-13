# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
from sklearn.datasets import load_iris
import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html

iris = load_iris() ## It returns simple dictionary like object with all data.

## Creating dataframe of total data
iris_df = pd.DataFrame(data=np.concatenate((iris.data,iris.target.reshape(-1,1)), axis=1), columns=(iris.feature_names+['Flower Type']))
iris_df["Flower Name"] = [iris.target_names[int(i)] for i in iris_df["Flower Type"]]

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# 標題
header = html.H1(children="解析合購版")

# 時間軸
year_slider = dcc.RangeSlider(id='year_slider',
                marks={
                    2015: '2015',
                    2016: '2016',
                    2017: '2017',
                    2018: '2018',
                    2019: '2019',
                    2020: '2020'},
                step=1,
                min=2015,
                max=2020,
                value=[2017,2020])

# 以px繪製月份圖，並丟入dcc.Graph
chart1 = px.scatter(data_frame=iris_df,
           x="sepal length (cm)",
           y="petal length (cm)",
           color="Flower Name",
           size=[1.0]*150,
           title="Month Percentage(%)")


graph1 = dcc.Graph(
        id='graph1',
        figure=chart1,
        className="six columns"
    )

# 以px繪製星期圖，並丟入dcc.Graph
chart2 = px.scatter(data_frame=iris_df,
           x="sepal width (cm)",
           y="petal width (cm)",
           color="Flower Name",
           size=[1.0]*150,
           title="Week Percentage(%)")


graph2 = dcc.Graph(
        id='graph2',
        figure=chart2,
        className="six columns"
    )

# 以px繪製??圖，並丟入dcc.Graph
chart3 = px.histogram(data_frame=iris_df,
             x="sepal length (cm)",
             color="Flower Name",
             title="Producst Types")

graph3 = dcc.Graph(
        id='graph3',
        figure=chart3,
        className="six columns"
    )

# 以px繪製??圖，並丟入dcc.Graph
chart4 = px.box(data_frame=iris_df,
           x="Flower Name",
           y="sepal width (cm)",
           color="Flower Name",
           title="Payment Types")


graph4 = dcc.Graph(
        id='graph4',
        figure=chart4,
        className="six columns"
    )

# 版面配置
row0 = html.Div(children=[year_slider])
row1 = html.Div(children=[graph1, graph2])
row2 = html.Div(children=[graph3, graph4])

# 以html.Div建立layout物件
layout = html.Div(children=[header, row0, row1, row2], style={"text-align": "center"})

# 將layout丟到app.layout才能在網頁輸出
app.layout = layout

# 執行
if __name__ == "__main__":
    app.run_server(debug=True)