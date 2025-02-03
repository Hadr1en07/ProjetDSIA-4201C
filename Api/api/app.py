import dash
from dash import dcc, html, dash_table
import pandas as pd
from pymongo import MongoClient

# Connexion à MongoDB
client = MongoClient("mongodb://db:27017/")
db = client["nintendo_db"]
collection = db["games"]

# Chargement des données
data = list(collection.find({}, {"_id": 0}))
df = pd.DataFrame(data)

# Initialisation de Dash
app = dash.Dash(__name__, external_stylesheets=["https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css"])

app.layout = html.Div([
    html.H1("Nintendo Games", style={'textAlign': 'center'}),
    
    dash_table.DataTable(
        id='games-table',
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict('records'),
        page_size=10,
        style_table={'overflowX': 'auto'}
    ),
    
    dcc.Graph(
        id='games-by-platform',
        figure={
            'data': [
                {'x': df['platform'].value_counts().index, 'y': df['platform'].value_counts().values, 'type': 'bar'}
            ],
            'layout': {'title': 'Number of Games by Platform'}
        }
    )
])

if __name__ == "__main__":
    app.run_server(debug=True, host="0.0.0.0", port=8050)