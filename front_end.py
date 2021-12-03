from data_prep.data_table import make_data_table, make_table_agg_txn_by_country_name
from data_prep.threed_prep import text_header, make_features_df
from data_prep.time_series_prep import upper_lower, anomalies_df, set_interpolated_zero
from data_prep.sentiment_prep import sentiments_redefined_polarity

import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from dash.dependencies import Input, Output
from dateutil.relativedelta import relativedelta
from datetime import datetime
from dash import Dash
import warnings
import json

# DASH == 2.0.0
from dash import html, dcc, dash_table

# DASH == 1.12.0
# import dash_core_components as dcc
# import dash_html_components as html
# import dash_table

warnings.filterwarnings('ignore')
CONFIG = json.load(open('./pfa_dash/config/config_dash.json'))

# Data
if "ts" in CONFIG["modules_to_run"]:
    data_table, agg = make_data_table(), upper_lower(make_table_agg_txn_by_country_name())
    anomalies = anomalies_df(agg)  # extract out anomalous data

if "3d" in CONFIG["modules_to_run"]:
    features_df, features = make_features_df()  # entry point to change df

if "news" in CONFIG["modules_to_run"]:
    sentiments_df = sentiments_redefined_polarity()

# agg = set_interpolated_zero(agg)

# App
app = Dash(__name__, external_stylesheets=[dbc.themes.LUX], prevent_initial_callbacks=True)

app.layout = dbc.Container([
    dcc.Location(id="url"),

    dbc.Row(
        dbc.Col(
            html.H5('MACRO MONITORING - PAYMENT FLOW',
                    style={'color': 'white',
                           'backgroundColor': '#21282b',
                           'height': '60px',
                           'align-items': 'center',
                           'display': 'flex',
                           'flex_direction': 'row',
                           'text_transform': 'uppercase',
                           'letter-spacing': '0.25em',
                           'font-weight': '300',
                           'padding': '0.8em',
                           'text-indent': '1em'}),
        ),
    ),

    html.Br(),

    dbc.Row([
        dbc.Col([
            html.Div([
                dbc.Nav(
                    [
                        dbc.NavLink("Time Series Insight", href="/", active="exact"),
                        dbc.NavLink("3D Insight", href="/page-1", active="exact"),
                        dbc.NavLink("News Insight", href="/page-2", active="exact"),
                    ],
                    vertical=True,
                    pills=True,
                ),
            ],
                style={"position": "fixed",
                       "top": "60px",
                       "left": 0,
                       "bottom": 0,
                       "width": "16rem",
                       "padding": "2rem 1rem",
                       "background-color": "#f8f9fa",
                       "color": "black",
                       'fontSize': '12',
                       'font-family': 'Arial'
                       }),
        ]),
    ]),

    dbc.Row([
        dbc.Col([
            html.Div([
                dash_table.DataTable(
                    id='datatable',
                    columns=[
                        {"name": i, "id": i, "deletable": False, "selectable": True, "hideable": False}
                        for i in data_table.columns
                    ],
                    data=data_table.to_dict("records"),  # contents of the table
                    editable=False,  # allow editing of the table
                    filter_action="native",  # allow filtering of data by user ('native') or not ('none')
                    sort_action="native",  # enables data to be sorted per-column by user or not ('none')
                    sort_mode="single",  # sort across 'multi' or 'single' columns
                    column_selectable=False,  # allow users to select 'multi' or 'single' columns
                    row_selectable="single",  # allow users to select 'multi' or 'single' rows
                    row_deletable=False,  # choose if user can delete a row (True) or not (False)
                    selected_columns=[],  # ids of columns that user selects
                    selected_rows=[0],  # indices of rows that user selects
                    page_action="native",  # all data is passed to the table up-front or not ('none')
                    page_current=0,  # page number that user is on
                    page_size=7,  # number of rows visible per page
                    persistence=True,
                    style_cell={
                        'height': 'auto',
                        'minWidth': '230px', 'width': '230px', 'maxWidth': '230px',
                        'whiteSpace': 'normal',
                        'font-family': 'Arial',
                    },
                    style_cell_conditional=[
                        {
                            'if': {'column_id': c},
                            'textAlign': 'left'
                        } for c in data_table.columns
                    ],
                    style_data={
                        'whiteSpace': 'normal',
                        'height': 'auto',
                        'minWidth': '240px', 'width': '240px', 'maxWidth': '240px',
                        'font-size': '10px'
                    },
                    style_header={
                        'fontWeight': 'bold',
                    },
                ),
            ]),
        ]),
    ], style={"margin-left": "18rem",
              "margin-right": "2rem",
              'text-indent': '1em'}, id='datatable-container'),

    html.Br(),

    dbc.Row([
        dbc.Col([
            html.Div([
                dcc.Graph(id="page-content",
                          figure={},
                          responsive='auto',
                          config={'displayModeBar': False,
                                  'showTips': True,
                                  'doubleClick': 'reset',
                                  'staticPlot': False,
                                  'scrollZoom': True,
                                  'watermark': False},)
                          #style={'height': '10vh'},)
            ], style={"margin-left": "18rem",
                      "margin-right": "2rem",
                      "margin-bottom": "0rem",
                      "height": "100%",
                      "vertical-align": "center"}),
        ]),
    ]),

    html.Div(id='sentiments-datatable-container', children=[],
             style={"margin-left": "2rem",
                    "margin-right": "2rem",
                    'text-indent': '1em'}),

    html.Div(id='selection', children=[], style={'display': 'none'}),

], fluid=True, style={'width': '100%',
                      'height': '100%',
                      'overflow-x': 'hidden',
                      'padding': '0rem',
                      'margin': '0rem',
                      'font-family': 'Arial'})


@app.callback(
    Output('selection', 'children'),
    [Input("url", "pathname")]
)
def render_page_content(pathname):
    """ Callback function to identify pages
    :param pathname: web application URL
    :type pathname: String
    ...
    :return: html text to identify existing pages
    :rtype: String
    """
    if pathname == "/":
        return 'dummy1'

    elif pathname == "/page-1":
        return 'dummy2'

    elif pathname == "/page-2":
        return 'dummy3'


@app.callback(
    Output(component_id='page-content', component_property='style'),
    [Input(component_id='selection', component_property='children')]
)
def show_hide_element(visibility_state):
    """ Callback function to adjust CSS for graph component
    :param visibility_state: html text to identify existing page
    :type visibility_state: String
    ...
    :return: CSS overwrite
    :rtype: Dictionary
    """
    if visibility_state == 'dummy1':
        return {}

    elif visibility_state == 'dummy2':
        return {}

    elif visibility_state == 'dummy3':
        return {"display": "none"}


@app.callback(
    Output(component_id='datatable-container', component_property='style'),
    [Input(component_id='selection', component_property='children')]
)
def show_hide_element(visibility_state):
    """ Callback function to adjust CSS for dash datatable
    :param visibility_state: html text to identify existing page
    :type visibility_state: String
    ...
    :return: CSS overwrite
    :rtype: Dictionary
    """
    if visibility_state == 'dummy1':
        return {"margin-left": "18rem", "margin-right": "2rem", 'text-indent': '1em'}

    elif visibility_state == 'dummy2':
        return {"margin-left": "18rem", "margin-right": "2rem", 'text-indent': '1em'}

    elif visibility_state == 'dummy3':
        return {"margin-left": "18rem", "margin-right": "2rem", 'text-indent': '1em'}


@app.callback(
    Output(component_id='sentiments-datatable-container', component_property='style'),
    [Input(component_id='selection', component_property='children')]
)
def show_hide_element(visibility_state):
    """ Callback function to adjust CSS for sentiments datatable
    :param visibility_state: html text to identify existing page
    :type visibility_state: String
    ...
    :return: CSS overwrite
    :rtype: Dictionary
    """
    if visibility_state == 'dummy1':
        return {"margin-left": "18rem", "margin-right": "2rem", 'text-indent': '1em', 'display': 'none'}

    elif visibility_state == 'dummy2':
        return {"margin-left": "18rem", "margin-right": "2rem", 'text-indent': '1em', 'display': 'none'}

    elif visibility_state == 'dummy3':
        return {"margin-left": "18rem", "margin-right": "2rem", 'text-indent': '1em'}


@app.callback(
    Output(component_id='page-content', component_property='figure'),
    [Input(component_id='datatable', component_property='selected_rows'),
     Input(component_id='selection', component_property='children'), ]
)
def update_graph(slctd_rows, dummy_value):
    """ Callback function to update time series and 3D clustering graphs
    :param slctd_rows: user selection on the main datatable
    :type slctd_rows: String
    :param dummy_value: html text to identify existing page
    :type dummy_value: String
    ...
    :return: plotly graph (if applicable)
    :rtype: plotly graph object
    """
    if dummy_value == 'dummy1':
        if "ts" not in CONFIG["modules_to_run"]:
            return {}
        country = data_table.iloc[slctd_rows[0]][0]
        df_ref = agg.loc[agg['country_name'] == country]

        anomalies_ref = anomalies.loc[anomalies['country_name'] == country]
        anomalies_ref = anomalies_ref.loc[anomalies_ref['begin_date'] >= df_ref['begin_date'].iloc[0]]

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=df_ref.begin_date, y=df_ref.agg_amount, mode='lines+markers',
            marker_symbol='circle-open',
            line_color='royalblue',
            name='Actual Transaction'
        ))

        fig.add_trace(go.Scatter(
            x=df_ref.begin_date, y=df_ref.lower, mode='lines',
            line_color='rgba(46, 139, 87, 0.1)',
            name='Lower Bound'
        ))

        fig.add_trace(go.Scatter(
            x=df_ref.begin_date, y=df_ref.upper, mode='lines',
            fill='tonexty',
            fillcolor='rgba(46, 139, 87, 0.15)',
            line_color='rgba(46, 139, 87, 0.1)',
            name='Upper Bound'
        ))

        fig.add_trace(go.Scatter(
            x=df_ref.begin_date, y=df_ref.mv_mean,
            line=dict(color='rgba(46, 139, 87, 0.5)', width=4, dash='dash'),
            name='Moving Average'
        ))

        fig.add_trace(go.Scatter(
            x=anomalies_ref.begin_date, y=anomalies_ref.agg_amount, mode='markers',
            line=dict(color='rgb(255,0,0)', width=10),
            name='Outlier'
        ))

        fig.update_yaxes(rangemode="nonnegative")
        fig.update_layout(
            xaxis_title="Period",
            yaxis_title="Debit Transaction Amount",
            legend_title="Legend",
            font=dict(
                family="Arial",
                size=14,
            )
        )

        max_date_str = df_ref.begin_date.max()
        max_date = datetime.strptime(max_date_str, '%Y-%m-%d')
        min_date = max_date - relativedelta(years=2)
        fig.update_layout(xaxis_range=[min_date, max_date])
        fig.update_layout(margin=dict(l=0, r=0, b=0, t=0))
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        fig.update_layout(height=2000)
        fig.update_xaxes(showline=True, linewidth=1, linecolor='black')
        fig.update_yaxes(showline=True, linewidth=1, linecolor='black')
        return fig

    elif dummy_value == 'dummy2':
        if "3d" not in CONFIG["modules_to_run"]:
            return {}
        country = data_table.iloc[slctd_rows[0]][0]
        if country not in features_df['country_name'].tolist():
            return {}
        comp_normalized = text_header(country, features_df)
        comp_normalized.loc[comp_normalized.result == 0.0, 'Colour'] = 'rgb(23, 190, 207)'
        comp_normalized.loc[comp_normalized.result == 1.0, 'Colour'] = 'red'

        positive = comp_normalized.loc[comp_normalized.result == 1.0]
        negative = comp_normalized.loc[comp_normalized.result == 0.0]
        point_df = comp_normalized.loc[comp_normalized.country == country]

        if country in negative['country'].values:
            point_df['header'] = country
        else:
            point_df['header'] = ''

        x = comp_normalized.columns[0]
        y = comp_normalized.columns[1]
        z = comp_normalized.columns[2]

        scatter1 = dict(
            mode="markers+text",
            name="Anomaly",
            type="scatter3d",
            x=positive[x], y=positive[y], z=positive[z],
            text=list(positive['header'].values),
            textfont=dict(family="Arial", size=10),
            opacity=0.8,
            marker=dict(size=10, color=positive.Colour)
        )

        scatter2 = dict(
            mode="markers",
            name="Non-Anomaly",
            type="scatter3d",
            x=negative[x], y=negative[y], z=negative[z],
            opacity=0.8,
            marker=dict(size=6, color=negative.Colour)
        )

        scatter3 = dict(
            mode="markers+text",
            name="Current Point",
            type="scatter3d",
            x=point_df[x], y=point_df[y], z=point_df[z],
            text=list(point_df['header'].values),
            textfont=dict(family="Arial", size=10),
            opacity=0.8,
            marker=dict(size=15, color='#FDDA0D')
        )

        clusters = dict(
            alphahull=7,
            name="Clusters",
            opacity=0.1,
            type="mesh3d",
            x=comp_normalized[x], y=comp_normalized[y], z=comp_normalized[z],
        )

        fig = go.Figure(dict(data=[scatter1, scatter2, scatter3, clusters]))

        fig.update_layout(
            autosize=True, scene=dict(
                xaxis=dict(
                    backgroundcolor="white",
                    gridcolor="rgb(200, 200, 200)",
                    showbackground=True,
                    showgrid=True, ),

                yaxis=dict(
                    backgroundcolor="white",
                    gridcolor="rgb(200, 200, 200)",
                    showbackground=True,
                    showgrid=True),

                zaxis=dict(
                    backgroundcolor="white",
                    gridcolor="rgb(200, 200, 200)",
                    showbackground=True,
                    showgrid=True, ),

                xaxis_title=dict(
                    text=x, font=dict(size=12)
                ),

                yaxis_title=dict(
                    text=y, font=dict(size=12)
                ),

                zaxis_title=dict(
                    text=z, font=dict(size=12)
                ),

                xaxis_showspikes=False,
                yaxis_showspikes=False,
                zaxis_showspikes=False, ),
        )

        fig.update_layout(margin=dict(l=0, r=0, b=0, t=0))
        fig.update_layout(legend_title_text='Legend')
        return fig

    elif dummy_value == 'dummy3':
        return {}


@app.callback(
    Output(component_id='sentiments-datatable-container', component_property='children'),
    [Input(component_id='datatable', component_property='selected_rows'),
     Input(component_id='selection', component_property='children'), ]
)
def update_sentiment(slctd_rows, dummy_value):
    """ Callback function to update news sentiment datatable
     :param slctd_rows: user selection on the main datatable
     :type slctd_rows: String
     :param dummy_value: html text to identify existing page
     :type dummy_value: String
     ...
     :return: news datatable (if applicable)
     :rtype: dash datatable component
     """
    if dummy_value == 'dummy1':
        return
    elif dummy_value == 'dummy2':
        return
    elif dummy_value == 'dummy3':
        if "news" not in CONFIG["modules_to_run"]:
            return []
        country = data_table.iloc[slctd_rows[0]][0]
        sentiments_country_df = sentiments_df.loc[sentiments_df['Country'] == country]
        sentiments_country_df.drop('Country', axis=1, inplace=True)
        sentiments_country_df = sentiments_country_df.sort_values(by='Polarity', ascending=True)
        return dbc.Row([
            dbc.Col([
                dash_table.DataTable(
                    id='sentiment-datatable',
                    columns=[
                        {"name": i, "id": i, "deletable": False, "selectable": False, "hideable": False}
                        for i in sentiments_country_df.columns
                    ],
                    data=sentiments_country_df.to_dict("records"),  # contents of the table
                    editable=False,  # allow editing of the table
                    filter_action='none',  # allow filtering of data by user ('native') or not ('none')
                    sort_action="native",  # enables data to be sorted per-column by user or not ('none')
                    sort_mode="multi",  # sort across 'multi' or 'single' columns
                    column_selectable=False,  # allow users to select 'multi' or 'single' columns
                    row_selectable=False,  # allow users to select 'multi' or 'single' rows
                    row_deletable=False,  # choose if user can delete a row (True) or not (False)
                    selected_columns=[],  # ids of columns that user selects
                    selected_rows=[0],  # indices of rows that user selects
                    page_action="native",  # all data is passed to the table up-front or not ('none')
                    page_current=0,  # page number that user is on
                    page_size=15,  # number of rows visible per page
                    style_cell={
                        'height': 'auto',
                        'whiteSpace': 'normal',
                        'font-family': 'Arial',
                        'textAlign': 'center',
                        'maxWidth': '500px',
                        'overflow': 'hidden',
                        'textOverflow': 'ellipsis',
                    },
                    style_cell_conditional=[
                        {
                            'if': {'column_id': 'Headline'},
                            'textAlign': 'left'
                        }

                    ],
                    style_data_conditional=(
                        [
                            {
                                'if': {
                                    'column_id': 'Polarity',
                                    'filter_query': '{Polarity} < -0.5',
                                },
                                'backgroundColor': '#F9CDC4',
                                'color': 'black',
                            },

                            {
                                'if': {
                                    'column_id': 'Polarity',
                                    'filter_query': '{Polarity} > 0.5',
                                },
                                'backgroundColor': '#BEE5B0',
                                'color': 'black',
                            },

                            {
                                'if': {
                                    'column_id': 'Polarity',
                                    'filter_query': '{Polarity} >= -0.5 && {Polarity} <= 0.5',
                                },
                                'backgroundColor': '#FFFCB4',
                                'color': 'black',
                            },

                            {
                                'if': {
                                    'column_id': 'Headline'
                                },
                                'fontWeight': 'bold'
                            },

                        ]
                    ),
                    style_as_list_view=True,
                    style_data={
                        'whiteSpace': 'normal',
                        'height': 'auto',
                        'lineHeight': '15px',
                        'font-size': '10px'

                    },
                    style_header={
                        'fontWeight': 'bold',
                    },
                ),
            ]),
        ]),


if __name__ == '__main__':
    app.run_server(debug=False, port=8888)
