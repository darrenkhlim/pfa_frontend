from synthetic_data.agg_txn_by_country_name import agg_txn_by_country_names
from synthetic_data.agg_by_features import make_features_df

from data_prep.shapley_prep import iforest_shap
from data_prep.threed_prep import features_pca
from data_prep.data_table import make_data_table
from data_prep.time_series_prep import upper_lower, anomalies_df, set_interpolated_zero

import dash_bootstrap_components as dbc
from dash import Dash, html, dcc, dash_table
from dash.dependencies import Input, Output
from collections import OrderedDict
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

# Synthetic Data
data_table, agg = make_data_table(), upper_lower(agg_txn_by_country_names())
# agg = set_interpolated_zero(agg)
anomalies = anomalies_df(agg)

features_df, features = make_features_df()

# Data Prep
comp_normalized = features_pca(features_df, features)
df_with_shap, shap_cols = iforest_shap(features_df, features)

# App
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], prevent_initial_callbacks=True)

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
                           'padding': '0.8em 0'}),
        ),
    ),

    html.Br(),

    dbc.Row([
        dbc.Col([
            html.Div([
                html.P(
                    "Selection Visualization", className="lead"
                ),
                dbc.Nav(
                    [
                        dbc.NavLink("Time Series Inisght", href="/", active="exact"),
                        dbc.NavLink("3D Insight", href="/page-1", active="exact"),
                        dbc.NavLink("Anomaly Interpretation", href="/page-2", active="exact"),
                    ],
                    vertical=True,
                    pills=True,
                ),
            ],
                style={"position": "fixed",
                       "top": "60px",
                       "left": 0,
                       "bottom": 0,
                       "width": "16rem",  # total width of the side bar
                       "padding": "2rem 1rem",  # top and side gaps
                       "background-color": "#f8f9fa",
                       }),
        ]),
    ]),

    html.Div([
        dbc.Row([
            dbc.Col([
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
                    page_size=6,  # number of rows visible per page
                    style_cell={
                        'height': 'auto',
                        'minWidth': '230px', 'width': '230px', 'maxWidth': '230px',
                        'whiteSpace': 'normal'
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
                    },
                    style_header={
                        'fontWeight': 'bold',
                    },
                ),
            ]),
        ]),
    ], style={"margin-left": "18rem",
              "margin-right": "2rem"}),

    html.Div([
        dcc.Graph(id="page-content", figure={}, responsive=True)
    ], style={"margin-left": "18rem", "margin-right": "0rem"},
    ),
    html.Div(id='selection', children=[], style={'display': 'none'}),

], fluid=True, style={'width': '100%',
                      'height': '100%',
                      'overflow-x': 'hidden',
                      'padding': '0rem',
                      'margin': '0rem',
                      'font-family': 'Arial'}
)


@app.callback(
    Output('selection', 'children'),
    [Input("url", "pathname")]
)
def render_page_content(pathname):
    if pathname == "/":
        return 'dummy1'

    elif pathname == "/page-1":
        return 'dummy2'

    elif pathname == "/page-2":
        return 'dummy3'


@app.callback(
    Output(component_id='page-content', component_property='figure'),
    [Input(component_id='datatable', component_property='selected_rows'),
     Input('selection', 'children'), ]
)
def update_graph(slctd_rows, dummy_value):
    if dummy_value == 'dummy1':
        country = data_table.iloc[slctd_rows[0]][0]
        df_ref = agg.loc[agg['country_name'] == country]
        # df_ref = df_ref.tail(40) ## last 13 months

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
            xaxis_title="Period (Weeks)",
            yaxis_title="Transaction Amount",
            legend_title="Legend",
            font=dict(
                family="Courier New, monospace",
                size=14,
            )
        )

        fig.update_layout(xaxis_range=[df_ref.tail(56).begin_date.min(), df_ref.begin_date.max()])
        fig.update_layout(margin=dict(l=0, r=0, b=0, t=0))
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        fig.update_xaxes(showline=True, linewidth=1, linecolor='black')
        fig.update_yaxes(showline=True, linewidth=1, linecolor='black')

        return fig

    elif dummy_value == 'dummy2':
        country = data_table.iloc[slctd_rows[0]][0]
        comp_normalized.loc[comp_normalized.result == 0.0, 'Colour'] = 'blue'
        comp_normalized.loc[comp_normalized.result == 1.0, 'Colour'] = 'red'
        positive = comp_normalized.loc[comp_normalized.result == 1.0]
        negative = comp_normalized.loc[comp_normalized.result == 0.0]
        point_df = comp_normalized.loc[comp_normalized.country == country]

        data = [go.Scatter3d(x=positive['PC_1'], y=positive['PC_2'], z=positive['PC_3'],
                             mode='markers+text', marker=dict(size=10, color=positive.Colour), opacity=0.8,
                             text=list(positive['header'].values),
                             name='Anomaly'),

                go.Scatter3d(x=negative['PC_1'], y=negative['PC_2'], z=negative['PC_3'],
                             mode='markers', marker=dict(size=10, color=negative.Colour), opacity=0.8,
                             name='Non Anomaly'),

                go.Scatter3d(x=point_df['PC_1'], y=point_df['PC_2'], z=point_df['PC_3'],
                             mode='markers', marker=dict(size=15, color='green'), opacity=0.4,
                             name='Current Point')]

        #         fig = px.scatter_3d(comp_normalized, x='PC_1', y='PC_2', z='PC_3',
        #                             opacity=0.7,
        #                             size_max=18,
        #                             color=comp_normalized.Colour,
        #                             color_discrete_map= {'Blue (Not Anomaly)': 'blue',
        #                                                  'Red (Anomaly)': 'red',},
        #                                                  #'Green (Current Point)': 'green'},
        #                             text=comp_normalized['header'])

        #         fig = px.scatter_3d(point_df, x='PC_1', y='PC_2', z='PC_3',
        #                     opacity=0.7,
        #                     size_max=50,
        #                     color=point_df.Colour,
        #                     color_discrete_map= {'Blue (Not Anomaly)': 'blue',
        #                                          'Red (Anomaly)': 'red',},
        #                                          #'Green (Current Point)': 'green'},
        #                     text=point_df['header'])

        fig = go.Figure(data)
        fig.update_layout(scene=dict(
            xaxis=dict(
                backgroundcolor="rgb(200, 200, 230)",
                gridcolor="white",
                showbackground=True,
                zerolinecolor="white", ),

            yaxis=dict(
                backgroundcolor="rgb(230, 200, 230)",
                gridcolor="white",
                showbackground=True,
                zerolinecolor="white"),

            zaxis=dict(
                backgroundcolor="rgb(230, 230, 200)",
                gridcolor="white",
                showbackground=True,
                zerolinecolor="white", ), ),
        )

        fig.update_layout(margin=dict(l=0, r=0, b=0, t=0))
        fig.update_layout(legend_title_text='Legend')
        return fig

    elif dummy_value == 'dummy3':
        country = data_table.iloc[slctd_rows[0]][0]
        row = df_with_shap.loc[df_with_shap.country == country].iloc[0]
        shaps = row[shap_cols].sort_values(ascending=True).head(5)
        sorted_pairs = sorted(dict(shaps).items(), key=lambda k: abs(k[1]), reverse=False)
        ordered_dict = OrderedDict(sorted_pairs)
        country_shap_df = pd.DataFrame.from_dict(ordered_dict, orient='index', columns=['shapley_value'])
        country_shap_df = country_shap_df.reset_index().rename(columns={'index': 'top_features'})
        country_shap_df['top_features'] = country_shap_df['top_features'].apply(lambda x: x[5:])

        country_shap_df.loc[country_shap_df['shapley_value'] < 0, 'Colour'] = 'Red'
        country_shap_df.loc[country_shap_df['shapley_value'] > 0, 'Colour'] = 'Blue'

        fig = px.bar(country_shap_df, x="shapley_value", y="top_features", orientation='h',
                     color=country_shap_df.Colour,
                     color_discrete_map={'Red': 'red', 'Blue': 'blue'})

        fig.update_layout(yaxis={'categoryorder': 'array', 'categoryarray': country_shap_df.top_features})
        fig.update_layout(margin=dict(l=0, r=0, b=0, t=0))
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        fig.update_xaxes(showline=True, linewidth=1, linecolor='black')
        fig.update_yaxes(showline=True, linewidth=1, linecolor='black')

        #         positive = country_shap_df.loc[country_shap_df.shapley_value>0]
        #         negative = country_shap_df.loc[country_shap_df.shapley_value<0]

        #         annotations = []
        #         for yd, xd in zip(negative.shapley_value, negative.top_features):
        #             annotations.append(dict(xref='x1', yref='y1',
        #                                     y=xd, x=yd - 0.005,
        #                                     text=round(yd,3),
        #                                     font=dict(family='Arial', size=12, color='black'),
        #                                     showarrow=False))

        #         for yd, xd in zip(positive.shapley_value, positive.top_features):
        #             annotations.append(dict(xref='x1', yref='y1',
        #                                     y=xd, x=yd + 0.005,
        #                                     text=round(yd,3),
        #                                     font=dict(family='Arial', size=12, color='black'),
        #                                     showarrow=False))

        #         fig.update_layout(annotations=annotations)

        return fig


if __name__ == '__main__':
    app.run_server(debug=True)
