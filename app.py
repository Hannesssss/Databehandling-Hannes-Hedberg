from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd
import seaborn as sns
import numpy as np

app = Dash(__name__)

app.layout = html.Div([
    html.H6("Change the value in the text box to see callbacks in action!"),
    html.Div([
        "Input: ",
        dcc.Input(id='my-input', value='initial value', type='text')
    ]),
    html.Br(),
    html.Div(id='my-output'),

])


@app.callback(
    Output(component_id='my-output', component_property='children'),
    Input(component_id='my-input', component_property='value')
)
def update_output_div(input_value):
    return f'Output: {input_value}'

# see https://plotly.com/python/px-arguments/ for more options

df_c19_vaccine = pd.read_excel(
    "Folkhalsomyndigheten_Covid19_Vaccine.xlsx",            # read the 2nd excel file, coiv19 vaccine data
    sheet_name = "Vaccinerade kommun och ålder"                     # open the sheet in the excel file named "Vaccinerade kommun och ålder"
)

counties = df_c19_vaccine.groupby(["Län_namn"])

df_vaccine_rollout = pd.DataFrame()                                                                                 # create a DataFrame for vaccine rollout
df_vaccine_rollout["Antal minst 1 dos"] = counties["Antal minst 1 dos"].sum() / counties["Befolkning"].sum()        # simple formula for dosage 1-3 summed, then divided by the population "befolkning"
df_vaccine_rollout["Antal minst 2 doser"] = counties["Antal minst 2 doser"].sum() / counties["Befolkning"].sum()
df_vaccine_rollout["Antal 3 doser"] = counties["Antal 3 doser"].sum() / counties["Befolkning"].sum()

fig1 = px.bar(                                                                                   # using a bar chart from ploty express, as suggested by Jonas Bergström
    df_vaccine_rollout,                                                                         # loading the data from above
    title="Vaccination Rollout, 1-3 doses",                                                     # title of the bar chart, will appear top left corner
    labels= {"value": "andel vaccinerade", "Län_namn": "Län", "variable": "Doser"}              # labels from län, setting value and variables. Grabbed from above
)

fig2 = px.pie(                               # Using ploty express
    data_frame=df_c19_vaccine,              # grabbing the dataframe
    values='Befolkning',                    # uses population 
    names='Ålder',                          # uses age
    title='Sveriges åldersfördelning',      # title, displayed top left
    hole=.1                                 # dount hole
)

colors = ['gold', 'mediumturquoise', 'darkorange', 'lightgreen', 'red', 'blue', 'green', 'cyan', 'purple', 'violet', ] # colors

fig2.update_traces(                         # updates the pie chart with new settings
    hoverinfo='label+percent',             # hover with mouse for age & population
    textinfo='value', textfont_size=15,    # size of the text within the pie chart
    marker=dict(colors=colors,             # calls for colors above
    line=dict(color='#000000',             # sets the lines color, using hex numbers ex white would be "#FFFFFF"
    width=1),
    
))

app.layout = html.Div(children=[
    html.H1(children='Covid-19 Dashboard'),

    html.Div(children='''
        Dashboard over some covid-19 information
    '''),

   # dcc.Dropdown(
   #     id="c19-dropdown",
   #     value="",
   #),

   dcc.Dropdown(
        id="c19-dropdown",
        options=[
            {"label": "Stockholm", "value": "Stockholms län"},
            {"label": "Göteborg", "value": "Göteborg"},
            {"label": "Skåne", "value": "Skåne län"},
        ],
        placeholder="Select a County",
        value = "Län_namn",
        multi = False,
        clearable=False,
        style={"width": "50%"}


   ),

    dcc.Graph(
        id='bar_chart',
        figure=fig1
    ),
    
    dcc.Graph(
        id='pie_chart',
        figure=fig2
   )
   

#@app.callback(
#    Output(component_id="bar_chart", component_property="figure"),
#    [Input(component_id = "c19-dropdown", component_property="value")]
#)

])

@app.callback(
    Output('dropdown', 'value'),
    Input('dropdown', 'value'),
)
def update_ticker_options(value):
    if 'All' in value:
        value = ['a', 'b', 'c']
    return value


if __name__ == '__main__':
    app.run_server(debug=True)