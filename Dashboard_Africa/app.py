import dash
from dash import dcc, html, dash_table
import dash_bootstrap_components as dbc
from Datasets import dataset_agriculture
from Datasets import agri_value_col
from Dashboard_Africa.Callbacks import callbacks

app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1"}
    ]
)

# CSS Style

CARD_STYLE = {
    'backgroundColor': 'white',
    'borderRadius': '5px',
    'padding': '15px',
    'marginBottom': '15px',
    'boxShadow': '0 4px 6px rgba(0, 0, 0, 0.1)'
}

CHART_STYLE = {
    'height': '400px'
}
table_style = {
    'overflowX': 'auto',
    'backgroundColor': 'white',
    'border': '1px solid #ddd',
    'borderRadius': '5px'
}

table_header_style = {
    'backgroundColor': '#f4f4f4',
    'color': '#333',
    'fontWeight': 'bold',
    'border': '1px solid #ddd',
    'padding': '8px'
}

table_cell_style = {
    'textAlign': 'left',
    'border': '1px solid #ddd',
    'padding': '8px'
}

# Create table columns
agriculture_table = dash_table.DataTable(
    id="agriculture-table",
    columns=[
        {"id": "Entity", "name": "Entity", "type": "text"},
        {"id": "Code", "name": "Code", "type": "text"},
        {"id": "Year", "name": "Year", "type": "numeric"},
        {
            "id": agri_value_col,
            "name": "Gross Production Value (thousand US$)",
            "type": "numeric",
            "format": {"specifier": "$,.0f"},
        },
    ],
    style_table=table_style,
    style_header=table_header_style,
    style_cell=table_cell_style,
    page_size=10
)

conflict_table = dash_table.DataTable(
    id="conflict-table",
    columns=[
        {"id": "Entity", "name": "Entity", "type": "text"},
        {"id": "Code", "name": "Code", "type": "text"},
        {"id": "Year", "name": "Year", "type": "numeric"},
        {
            "id": "Number of ongoing conflicts - Conflict type: one-sided violence",
            "name": "One-sided Violence",
            "type": "numeric",
        },
        {
            "id": "Number of ongoing conflicts - Conflict type: extrasystemic",
            "name": "Extrasystemic",
            "type": "numeric",
        },
        {
            "id": "Number of ongoing conflicts - Conflict type: non-state conflict",
            "name": "Non-state Conflict",
            "type": "numeric",
        },
        {
            "id": "Number of ongoing conflicts - Conflict type: intrastate",
            "name": "Intrastate",
            "type": "numeric",
        },
        {
            "id": "Number of ongoing conflicts - Conflict type: interstate",
            "name": "Interstate",
            "type": "numeric",
        },
    ],
    style_table=table_style,
    style_header=table_header_style,
    style_cell=table_cell_style,
    page_size=10
)



# Conflicts Dropdowns
conflict_dropdown = dcc.Dropdown(
    id='conflict-dropdown',
    options=[{'label': 'One-sided violence', 'value': 'one_sided_violence'},
             {'label': 'Extrasystemic', 'value': 'extra_systemic'},
             {'label': 'Non-state conflict', 'value': 'non_state_conflict'},
             {'label': 'Intrastate', 'value': 'intrastate'}
             ],
    value='one_sided_violence',
    clearable=False,
    style={'width': '100%'}

)

comparison_conflict_dropdown = dcc.Dropdown(
    id='comparison-conflict-dropdown',
    options=[{'label': 'One-sided violence', 'value': 'one_sided_violence'},
             {'label': 'Extrasystemic', 'value': 'extra_systemic'},
             {'label': 'Non-state conflict', 'value': 'non_state_conflict'},
             {'label': 'Intrastate', 'value': 'intrastate'}
             ],
    value='one_sided_violence',
    clearable=False,
    style={'width': '100%'}

)

# Year range slider

year_range_slider = dcc.RangeSlider(
    id='year-range-slider',
    min=dataset_agriculture['Year'].min(),
    max=dataset_agriculture['Year'].max(),
    step=1,
    value=[dataset_agriculture['Year'].min(), dataset_agriculture['Year'].max()],
    marks={str(year): str(year) for year in
           range(int(dataset_agriculture['Year'].min()),
                 int(dataset_agriculture['Year'].max()) + 1,
                 5)},
    tooltip={"placement": "bottom", "always_visible": True}
)

# App layout
app.layout = ([
    dbc.Row([
        dbc.Col(html.H4('Wars and Agriculture Industry in the Africa',
                        className="bg-primary p-2 mb-2 text-center text-white")

                )
    ]),
    dbc.Row([
        dbc.Col(html.H5("Nice Teta Hirwa — CS150 — Professor Mike Ryu",
                        className="bg-primary p-2 mb-2 text-center text-white"))
    ], style={'marginBottom': '10px'}),

    dcc.Tabs(id="tabs", value='tab-individual', children=[
        dcc.Tab(label='Individual Charts', value='tab-individual', children=[
            # Contents of first tab - individual charts
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader(html.H5('Wars Dropdown')),
                        dbc.CardBody([
                            html.Label('Select Conflict Type:', className='fw-bold'),
                            conflict_dropdown,
                            html.Div(style={'height': '20px'})
                        ])
                    ])
                ])
            ], className='mt-2'),

            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader(html.H5('Conflict Data Over Time')),
                        dbc.CardBody([
                            dcc.Graph(id='conflict-bar-chart', style={"height": "400px"})
                        ])
                    ])
                ], width=6),
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader(html.H5('Agricultural Production Over Time')),
                        dbc.CardBody([
                            dcc.Graph(id='agriculture-line-chart', style={"height": "400px"})
                        ])
                    ])
                ], width=6)
            ], className='mt-2'),
        ]),

        dcc.Tab(label='Comparison Chart', value='tab-comparison', children=[
            # Contents of second tab - comparison chart
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader(html.H5("Dashboard Controls")),
                        dbc.CardBody([
                            html.Label("Select Conflict Type:", className="fw-bold mb-2"),
                            comparison_conflict_dropdown,
                            html.Div(style={"height": "20px"}),  # Spacer
                            html.Label("Select Year Range:", className="fw-bold mb-2"),
                            year_range_slider
                        ])
                    ])
                ])
            ], className="mt-2"),

            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader(html.H5("Comparison: Selected Conflict vs Agricultural Production")),
                        dbc.CardBody([
                            dcc.Graph(
                                id='comparison-line-chart',
                                style={"height": "450px", "width": "100%", "margin": "auto"},
                                config={
                                    'responsive': True,
                                    'displayModeBar': True,
                                    'scrollZoom': True
                                }
                            )
                        ])
                    ])
                ])
            ], className="mt-2"),
        ]),

        dcc.Tab(label='Data Tables', value='tab-tables', children=[
            # Contents of third tab - data tables
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader(html.H5("Conflict Data")),
                        dbc.CardBody([
                            conflict_table
                        ])
                    ]),
                    html.Div(style={"height": "20px"}),  # Spacer
                    dbc.Card([
                        dbc.CardHeader(html.H5("Agriculture Data")),
                        dbc.CardBody([
                            agriculture_table
                        ])
                    ])
                ])
            ])
        ]),
    ]),
])

callbacks(app)

if __name__ == '__main__':
    app.run(debug=True)
