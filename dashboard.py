import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output, dash_table
import database as db

app = Dash(__name__)
app.title = 'CRM Дашборд'

app.layout = html.Div([
    html.H1('Панель управления работой с клиентами', style={'textAlign': 'center', 'fontFamily': 'Arial'}),
    html.Div([
        html.H3('Распределение заявок по статусам'),
        dcc.Graph(id='status-chart')
    ], style={'width': '45%', 'display': 'inline-block', 'margin': '2%'}),
    html.Div([
        html.H3('Последние заявки клиентов'),
        html.Div(id='requests-table')
    ], style={'width': '45%', 'display': 'inline-block', 'verticalAlign': 'top', 'margin': '2%'}),
    dcc.Interval(id='interval', interval=15 * 1000, n_intervals=0)
])


@app.callback(
    Output('status-chart', 'figure'),
    Output('requests-table', 'children'),
    Input('interval', 'n_intervals')
)
def update_dashboard(n):
    reqs = db.get_all_requests()
    if not reqs:
        return px.bar(title="Нет данных"), html.Div("Список пуст")

    df = pd.DataFrame(reqs, columns=['ID', 'Клиент', 'Услуга', 'Статус', 'Дата'])

    # График
    status_counts = df['Статус'].value_counts().reset_index()
    status_counts.columns = ['Статус', 'Количество']
    fig = px.bar(status_counts, x='Статус', y='Количество', color='Статус', title='Статусы заявок')

    # Таблица
    table = dash_table.DataTable(
        data=df.to_dict('records'),
        columns=[{'name': i, 'id': i} for i in df.columns],
        style_header={'backgroundColor': '#2c3e50', 'color': 'white'},
        style_cell={'textAlign': 'left', 'padding': '5px'},
        page_size=10
    )
    return fig, table


if __name__ == '__main__':
    app.run(debug=True)