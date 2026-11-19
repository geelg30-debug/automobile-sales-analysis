
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

df = pd.read_csv('historical_automobile_sales 2.csv')

app = dash.Dash(__name__)
app.title = "Automobile Sales Dashboard"

app.layout = html.Div([
    html.H1("Automobile Sales Statistics Dashboard", style={'textAlign': 'center'}),
    html.Div([
        html.Label("Select Statistics:"),
        dcc.Dropdown(
            id='dropdown-statistics',
            options=[
                {'label': 'Yearly Statistics', 'value': 'Yearly'},
                {'label': 'Recession Period Statistics', 'value': 'Recession'}
            ],
            value='Yearly',
            placeholder='Select a report type',
            style={'width': '50%'}
        )
    ], className='dropdown-container'),
    html.Div(id='output-container', className='chart-grid', style={'display': 'flex', 'flex-direction': 'column'})
])

@app.callback(
    Output(component_id='output-container', component_property='children'),
    [Input(component_id='dropdown-statistics', component_property='value')]
)
def update_output(selected_statistics):
    if selected_statistics == 'Yearly':
        yearly_data = df.groupby('Year')['Automobile_Sales'].mean().reset_index()
        fig1 = px.line(yearly_data, x='Year', y='Automobile_Sales', title='Yearly Statistics')
        return html.Div([dcc.Graph(figure=fig1)])
    elif selected_statistics == 'Recession':
        recession_data = df[df['Recession'] == 1]
        fig2 = px.bar(recession_data, x='Vehicle_Type', y='Automobile_Sales', title='Recession Statistics')
        return html.Div([dcc.Graph(figure=fig2)])

if __name__ == '__main__':
    app.run_server(debug=True)
