data = pd.read_excel("../Data/Folkhalsomyndigheten_Covid19.xlsx", sheet_name="Veckodata Riket")
data = data.query("type == 'conventional' and region == 'Albany'")
data.sort_values("Date", inplace=True)
 
app = Dash(__name__)

app.layout = html.Div(
    children=[
        html.H1(children="Covid-19",),
        html.P(
            children="Data about covid-19",
        ),
        dcc.Graph(
            figure={
                "data": [
                    {
                        "x": data["Date"],
                        "y": data["AveragePrice"],
                        "type": "lines",
                    },
                ],
                "layout": {"title": "Avrage covid-19"},
            },
        ),
        dcc.Graph(
            figure={
                "data": [
                    {
                        "x": data["Date"],
                        "y": data["Total Volume"],
                        "type": "lines",
                    },
                ],
                "layout": {"title": "Coivd 19"}
            },
        ),
    ]
)

if __name__ == "__main__":
    app.run_server()