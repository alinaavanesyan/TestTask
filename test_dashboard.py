import dash
from dash import dcc
from dash import html
import pandas as pd
import plotly.express as px
import json
from glob import glob
import json
from multiprocessing import Pool
import pandas as pd
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import dash_bootstrap_components as dbc

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server


hits = glob("data/**/*.json", recursive=True)

#1 процесс
count = {}
all_categories = {}

def graph1(paths, all_categories): 
    for file_name in paths: 
        file = open(file_name)
        data_file = json.loads(file.read())
        if data_file["params"]["task_category"] not in all_categories.keys():
                all_categories[data_file["params"]["task_category"]] = {"f1": {}, "accuracy": {}}
                name = "count" + str(data_file["params"][ "task_category"])
                count[name] = 1
                for b in range(0,24):
                    all_categories[data_file["params"]["task_category"]]["f1"][b] = data_file["results"]["test_score"]["f1"][str(b)][0]
                    all_categories[data_file["params"]["task_category"]]["accuracy"][b] = data_file["results"]["test_score"]["f1"][str(b)][0]
        else:
            count[name] += 1
            for b in range(0,24):
                all_categories[data_file["params"]["task_category"]]["f1"][b] += data_file["results"]["test_score"]["f1"][str(b)][0]
                all_categories[data_file["params"]["task_category"]]["accuracy"][b] += data_file["results"]["test_score"]["f1"][str(b)][0]
                name = "count" + str(data_file["params"][ "task_category"])
    
    for k in all_categories.keys():
        name = "count" + str(k)
        for el in all_categories[k]["f1"].keys():
            all_categories[k]["f1"][el] = all_categories[k]["f1"][el]/count[name]
        for el in all_categories[k]["accuracy"].keys():
            all_categories[k]["accuracy"][el] = all_categories[k]["accuracy"][el]/count[name]


    average_all_categories = {}
    for k in all_categories.keys():
        average = 0
        for n in all_categories[k]["f1"].keys():
            average += float(all_categories[k]["f1"][n])
        average_all_categories[k] = float(average/len(all_categories[k]["f1"].keys()))
    average_all_categories = dict(sorted(average_all_categories.items(), key=lambda x: x[1]))
    
    fig1 = go.Figure(data=[
        go.Bar(
            name="f1",
            x = list(range(24)),
            y = list(all_categories["Number"]["f1"].values()),
            offsetgroup = 0,
            marker=dict(color="#393F84")
        ),
            
        go.Bar(
            name="accuracy",
            x = list(range(24)),
            y = list(all_categories["Number"]["accuracy"].values()),
            offsetgroup = 1,
            marker=dict(color="#8B94FF")
        ),
        ],
        layout=go.Layout(
            title="Metrics",
            height=350,
        )
    )
    fig2 = px.bar(y=list(average_all_categories.keys()), x=list(average_all_categories.values()),orientation="h", height=750)
    fig2.update_layout(showlegend=False)
    
    return fig1,fig2
    


#2 процесс
all_lang = {}
def graph2(hits,all_lang):
    for file_name in hits:
        file = open(file_name)
        data_file = json.loads(file.read())
        if data_file["params"]["task_language"] not in all_lang.keys():
                all_lang[data_file["params"]["task_language"]] = {}
                all_lang[data_file["params"]["task_language"]][data_file["params"]["task_category"]] = []
                for b in range(0,24):
                    all_lang[data_file["params"]["task_language"]][data_file["params"]["task_category"]].append(data_file["results"]["test_score"]["f1"][str(b)][0])
    
        else:
            all_lang[data_file["params"]["task_language"]][data_file["params"]["task_category"]] = []
            for b in range(0,24):
                    all_lang[data_file["params"]["task_language"]][data_file["params"]["task_category"]].append(data_file["results"]["test_score"]["f1"][str(b)][0])

    all_lang = dict(sorted(all_lang.items(), key=lambda x: x[0]))
    average_all_lang = {}
    for k in all_lang.keys():
        average = 0
        for n in all_lang[k].keys():
            average += sum(all_lang[k][n])/23
        average_all_lang[k] = average/len(all_lang[k].keys())
    average_all_lang = dict(sorted(average_all_lang.items(), key=lambda x: x[1]))

    fig3 = px.scatter(x=average_all_lang.keys(), y=average_all_lang.values(), labels=dict(x="Languages", y="Result"))
    def graph_choice(name):
        graph = {}
        for b in all_lang.keys():
            if name in all_lang[b].keys():
                graph[b] = all_lang[b][name]
        return graph

    fig4 = go.Figure(
        layout=go.Layout(
            height=900,
        )
    )

    fig4.add_trace(
        go.Heatmap(
        name="Number",
        z = np.array(list(graph_choice("Number").values())),
        y = list(graph_choice("Number").keys()),
        x = list(range(24)),
        xgap = 2,
        ygap = 2,
        colorscale="Magma"
        ))
    
    fig4.add_trace(
        go.Heatmap(
        name="Mood",
        z = np.array(list(graph_choice("Mood").values())),
        y = list(graph_choice("Mood").keys()),
        x = list(range(24)),
        xgap = 2,
        ygap = 2,
        colorscale="Magma",
        visible=False
    ))
    
    fig4.update_layout(
        updatemenus=[
            dict(
                buttons=list([
                    dict(label="Number",
                        method="update",
                        args=[{"visible": [True, False]},
                            ]),
                    dict(label="Mood",
                        method="update",
                        args=[{"visible": [False, True]},
                            ]),
                ]),
            )
        ])
    
    
    return fig3, fig4



if __name__ == "__main__":   
    with Pool(processes=2) as pool:
        result1 = pool.apply_async(graph1, (hits, all_categories))
        result1 = result1.get()
        result2 = pool.apply_async(graph2, (hits, all_lang))
        result2 = result2.get()

    app.layout = html.Div([
        dbc.Card(
            dbc.CardBody([
                dbc.Row([
                    dbc.Col([
                        dbc.Card(
                            dbc.CardBody([
                            html.H5("Probing score"),
                            ]), style={"margin-bottom": "1rem"}
                        ),
                        dbc.Card(
                            dbc.CardBody([
                            dcc.Graph(figure=result1[1]),
                            html.A("(graph.1) Categories: average values for all layers and languages"),
                        ]),
                        ),
                    ], width=4),

                    dbc.Col([
                        dbc.Card(
                            dbc.CardBody([
                                dcc.Graph(figure=result1[0]),
                                html.A("(graph.2) Comparison of the results of different metrics (average values for all categories in each layer, category Number)"),
                                dcc.Graph(figure=result2[0]),
                                html.A("(graph.3) Languages: average feature probing score on all layers and all categories"),
                            ]), 
                        ),
                    ], width=8),

                    dbc.Card(
                        dbc.CardBody([
                            dcc.Graph(figure=result2[1]),
                            html.A("(graph.4) Languages: average feature probing score on all layers (in two categories: Number and Mood)"),
                            html.P("P.S.: for the most effective use of the graph, use the zoom to better see the statistics for each layer"),
                        ]), style={"margin": "1rem"}
                        ),
                ]), 

            ]), style={"background-color": "#1B1A20", "text-align": "center"}
        )
        ])


    app.run_server(debug=True)
    
