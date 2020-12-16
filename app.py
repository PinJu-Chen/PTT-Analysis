# -*- coding: utf-8 -*-
import pandas as pd
import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_table


'''-------------------data-------------------'''
<<<<<<< HEAD
# test data
iris = load_iris() ## It returns simple dictionary like object with all data.
iris_df = pd.DataFrame(data=np.concatenate((iris.data,iris.target.reshape(-1,1)), axis=1), columns=(iris.feature_names+['Flower Type']))
iris_df["Flower Name"] = [iris.target_names[int(i)] for i in iris_df["Flower Type"]]

dfc = pd.read_csv(r'gapminder2007.csv')

=======
>>>>>>> 6d15e97e12e1dc440080b2de057913a330c72f1a
# buytogether data
df = pd.read_csv(r'rawdata.csv')
# >>>>>>> Stashed changes


'''-------------------資料處理-------------------'''
# 排除不需要的文章
dff = df[~(df.title.str.contains('公告')|
      df.title.str.contains('黑人')|
      df.title.str.contains('灰人')|
      df.title.str.contains('黑名單')|
      df.title.str.contains('判決')|
      df.title.str.contains('無主'))]

# top3
dft = pd.DataFrame(dff.groupby('author').count().nlargest(5, columns='id'))
dft['author'] = dft.index
print(dft)
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
                columns=[{"name": 'Black IDs', "id": 'black_ID'}],
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
                              value=[2018,2020],
                              className='ten columns')

# 以dcc.Graph建立instance，存放月份圖
month_bar = dcc.Graph(id='month_bar',
                   selectedData=None,
                   className="five columns")

# 以dcc.Graph建立instance，存放星期圖
week_bar = dcc.Graph(id='week_bar', className="five columns")

# 以dcc.Graph建立instance，存放???
graph3 = dcc.Graph(
        id='graph3',
        # figure=,
        className="five columns"
    )

# 以dcc.Graph建立instance，存放???
graph4 = dcc.Graph(
        id='graph4',
        # figure=,
        className="five columns"
    )

# 版面配置
# row0 = html.Div(children=[year_slider])
table_col = html.Div(children=[top3,blacklist], className="two columns")
graph_col = html.Div(children=[year_slider,month_bar, week_bar, graph3, graph4],
                     className='offset-by-three.column')
first_row = html.Div(children=[table_col, graph_col])
second_row = html.Div(id='select')


# 以html.Div建立layout物件
layout = html.Div(children=[header, first_row, second_row],
                  style={"text-align": "center"})


# 將layout丟到app.layout才能在網頁輸出
app.title = '解析合購版'
app.layout = layout


'''-------------------Month callback------------------'''
@app.callback(
    Output('month_bar', 'figure'),
    Output('month_bar', 'selectedData'),
    Input('year_slider', 'value'))

def update_month_bar(selected_year):
    # 年度
    dfm = dff[dff['year'].isin(selected_year)]

    # 更新 month_bar 月份圖
    chartm = px.bar(x=dfm.groupby('month').size().index,
                y=dfm.groupby('month').size(),
                title="Posts by Month",
                labels={"x":"Month",
                        "y":"Posts"},
                category_orders={"x": 
                                 ['Jan','Feb','Mar','Apr','May', 'Jun',
                                  'Jul','Aug','Sep','Oct','Nov','Dec']}
                )
    # 設定clickmode，作為後續的input
    chartm.update_layout(clickmode='event+select')
    return chartm, None


'''-------------------Week callback------------------'''
@app.callback(
    Output('week_bar', 'figure'),
    Input('year_slider', 'value'),
    Input('month_bar', 'selectedData'))

def upgrade_week_bar(selected_year, selectedData):
    # 年度
    dfw = dff[dff['year'].isin(selected_year)]
    
    # 月份 (Shift + leftclick)
    if selectedData is not None:
        filterm = []
        for i in range(len(selectedData['points'])):
            filterm.append(selectedData['points'][i].get('x'))
        dfw = dfw[dfw['month'].isin(filterm)]

    # 更新 week_bar 星期圖            
    chartw = px.bar(x=dfw.groupby('week').size().index,
                y=dfw.groupby('week').size(),
                title="Posts by Week",
                labels={"x":"Week",
                        "y":"Posts"},
                category_orders={"x": 
                                 ['Mon','Thu','Wed','Tue','Fri', 'Sat',
                                  'Sun']}
                )
    return  chartw


'''-------------------top3 callback------------------'''
@app.callback(
    Output('top3', 'data'),
    Input('year_slider', 'value'),
    Input('month_bar', 'selectedData'))

def upgrade_top3(selected_year, selectedData):
    # 年度
    dft = dff[dff['year'].isin(selected_year)]
    
    # 月份 (Shift + leftclick)
    if selectedData is not None:
        filterm = []
        for i in range(len(selectedData['points'])):
            filterm.append(selectedData['points'][i].get('x'))
        dft = dft[dft['month'].isin(filterm)]

    # 更新top3的data
    dft = pd.DataFrame(dft.groupby('author').count().nlargest(5, columns='id'))
    dft['author'] = dft.index    
    data = dft.head(3).to_dict('records')
    return  data


# 執行
if __name__ == "__main__":
    app.run_server(debug=True)