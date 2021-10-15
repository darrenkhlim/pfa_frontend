from data_prep.data_table import make_data_table, make_table_agg_txn_by_country_name
from data_prep.threed_prep import text_header, make_features_df
from data_prep.time_series_prep import upper_lower, anomalies_df, set_interpolated_zero

import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
import dash_table
from dash import Dash
from dash.dependencies import Input, Output
from dateutil.relativedelta import relativedelta
import plotly.graph_objects as go
from datetime import datetime

# Synthetic Data
data_table, agg = make_data_table(), upper_lower(make_table_agg_txn_by_country_name())
anomalies = anomalies_df(agg)  # extract out anomalous data
features_df, features = make_features_df()  # entry point to change df

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
                           'padding': '0.8em 0',
                           'text-indent': '1em'}),
        ),
    ),

    html.Br(),

    dbc.Row([
        dbc.Col([
            html.Div([
                # html.P(
                #     "Selection Visualization", className="lead"
                # ),
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
                       "width": "16rem",  # total width of the side bar
                       "padding": "2rem 1rem",  # top and side gaps
                       "background-color": "#f8f9fa",
                       "color": "black",
                       'fontSize': '12',
                       'font-family': 'Arial'
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
                        'whiteSpace': 'normal',
                        'fontSize': '12',
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
                    },
                    style_header={
                        'fontWeight': 'bold',
                    },
                ),
            ]),
        ]),
    ], style={"margin-left": "18rem",
              "margin-right": "2rem",
              'text-indent': '1em'}),

    html.Br(),

    html.Div([
        dcc.Graph(id="page-content", figure={}, responsive=True)
    ], style={"margin-left": "18rem",
              "margin-right": "0rem"},
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
            yaxis_title="Transaction Amount",
            legend_title="Legend",
            font=dict(
                family="Arial",
                size=14,
            )
        )

        max_date_str = df_ref.begin_date.max()
        max_date = datetime.strptime(max_date_str, '%Y-%m-%d')
        min_date = max_date - relativedelta(years=1)
        fig.update_layout(xaxis_range=[min_date, max_date])
        fig.update_layout(margin=dict(l=0, r=0, b=0, t=0))
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        fig.update_xaxes(showline=True, linewidth=1, linecolor='black')
        fig.update_yaxes(showline=True, linewidth=1, linecolor='black')
        return fig

    elif dummy_value == 'dummy2':
        # country = data_table.iloc[slctd_rows[0]][0]
        # comp_normalized = text_header(country, features_df)
        # marker_colors = ['red' if r == country else 'rgb(23,190,207)' for r in comp_normalized['country']]
        # marker_sizes = [14 if r == country else 7 for r in comp_normalized['country']]
        # marker_dict = dict(size=marker_sizes, color=marker_colors)
        # texts = [country if r == country else None for r in comp_normalized['country']]
        #
        # f1 = comp_normalized.columns[0]
        # f2 = comp_normalized.columns[1]
        # f3 = comp_normalized.columns[2]
        #
        # scatter = dict(
        #     mode = "markers+text",
        #     name = "y",
        #     type = "scatter3d",
        #     x = comp_normalized[f1], y = comp_normalized[f2], z = comp_normalized[f3],
        #     text = texts,
        #     marker = marker_dict,
        # )
        #
        # clusters = dict(
        #     alphahull = 7,
        #     name = "y",
        #     opacity = 0.1,
        #     type = "mesh3d",
        #     color = "rgb(23, 190, 207)",
        #     x = comp_normalized[f1], y = comp_normalized[f2], z = comp_normalized[f3],
        # )
        #
        # layout = dict(
        #     height=1000,
        #     scene = dict(
        #         xaxis=dict(
        #             backgroundcolor="white",
        #             gridcolor="rgb(200, 200, 200)",
        #             showbackground=True,
        #             showgrid=True,),
        #
        #         yaxis=dict(
        #             backgroundcolor="white",
        #             gridcolor="rgb(200, 200, 200)",
        #             showbackground=True,
        #             showgrid=True),
        #
        #         zaxis=dict(
        #             backgroundcolor="white",
        #             gridcolor="rgb(200, 200, 200)",
        #             showbackground=True,
        #             showgrid=True,),
        #
        #         xaxis_title=dict(
        #             text=f1, font=dict(size=12)
        #             ),
        #
        #         yaxis_title=dict(
        #             text=f2, font=dict(size=12)
        #             ),
        #
        #         zaxis_title=dict(
        #             text=f3, font=dict(size=12)
        #             ),
        #
        #         xaxis_showspikes=False,
        #         yaxis_showspikes=False,
        #         zaxis_showspikes=False,
        #     )
        # )
        #
        # fig = go.Figure(dict(data=[scatter, clusters], layout=layout))
        # #plot(fig, image='png', image_filename='plot_image', filename='./im.png', output_type='div')
        # return fig

        country = data_table.iloc[slctd_rows[0]][0]
        comp_normalized = text_header(country, features_df)
        comp_normalized.loc[comp_normalized.result == 0.0, 'Colour'] = 'rgb(23, 190, 207)'
        comp_normalized.loc[comp_normalized.result == 1.0, 'Colour'] = 'red'

        positive = comp_normalized.loc[comp_normalized.result == 1.0]
        negative = comp_normalized.loc[comp_normalized.result == 0.0]
        point_df = comp_normalized.loc[comp_normalized.country == country]

        x = comp_normalized.columns[0]
        y = comp_normalized.columns[1]
        z = comp_normalized.columns[2]

        # data = [go.Scatter3d(x=positive[x], y=positive[y], z=positive[z],
        #                      mode='markers+text', marker=dict(size=14, color=positive.Colour), opacity=0.8,
        #                      text=list(positive['header'].values),
        #                      name='Anomaly'),
        #
        #         go.Scatter3d(x=negative[x], y=negative[y], z=negative[z],
        #                      mode='markers', marker=dict(size=7, color=negative.Colour), opacity=0.8,
        #                      name='Non Anomaly'),
        #
        #         go.Scatter3d(x=point_df[x], y=point_df[y], z=point_df[z],
        #                      mode='markers', marker=dict(size=15, color='green'), opacity=0.4,
        #                      name='Current Point')]

        scatter1 = dict(
            mode="markers+text",
            name="Anomaly",
            type="scatter3d",
            x=positive[x], y=positive[y], z=positive[z],
            text=list(positive['header'].values),
            textfont=dict(family="Arial", size=12),
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
            mode="markers",
            name="Current Point",
            type="scatter3d",
            x=point_df[x], y=point_df[y], z=point_df[z],
            marker=dict(size=15, color='green'),
            opacity=0.4,
        )

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

        clusters = dict(
            alphahull=7,
            name="Clusters",
            opacity=0.1,
            type="mesh3d",
            # color="rgb(23, 190, 207)",
            x=comp_normalized[x], y=comp_normalized[y], z=comp_normalized[z],
        )

        fig = go.Figure(dict(data=[scatter1, scatter2, scatter3, clusters]))

        fig.update_layout(scene=dict(
            xaxis=dict(
                backgroundcolor="white",
                gridcolor="rgb(200, 200, 200)",
                showbackground=True,
                showgrid=True,),

            yaxis=dict(
                backgroundcolor="white",
                gridcolor="rgb(200, 200, 200)",
                showbackground=True,
                showgrid=True),

            zaxis=dict(
                backgroundcolor="white",
                gridcolor="rgb(200, 200, 200)",
                showbackground=True,
                showgrid=True,),

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
            zaxis_showspikes=False,),
        )

        fig.update_layout(margin=dict(l=0, r=0, b=0, t=0))
        fig.update_layout(legend_title_text='Legend')
        return fig

    elif dummy_value == 'dummy3':
        # country = data_table.iloc[slctd_rows[0]][0]
        # row = df_with_shap.loc[df_with_shap.country == country].iloc[0]
        # shaps = row[shap_cols].sort_values(ascending=True).head(5)
        # sorted_pairs = sorted(dict(shaps).items(), key=lambda k: abs(k[1]), reverse=False)
        # ordered_dict = OrderedDict(sorted_pairs)
        # country_shap_df = pd.DataFrame.from_dict(ordered_dict, orient='index', columns=['shapley_value'])
        # country_shap_df = country_shap_df.reset_index().rename(columns={'index': 'top_features'})
        # country_shap_df['top_features'] = country_shap_df['top_features'].apply(lambda x: x[5:])
        #
        # country_shap_df.loc[country_shap_df['shapley_value'] < 0, 'Colour'] = 'Red'
        # country_shap_df.loc[country_shap_df['shapley_value'] > 0, 'Colour'] = 'Blue'
        #
        # fig = px.bar(country_shap_df, x="shapley_value", y="top_features", orientation='h',
        #              color=country_shap_df.Colour,
        #              color_discrete_map={'Red': 'red', 'Blue': 'blue'})
        #
        # fig.update_layout(yaxis={'categoryorder': 'array', 'categoryarray': country_shap_df.top_features})
        # fig.update_layout(margin=dict(l=0, r=0, b=0, t=0))
        # fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        # fig.update_xaxes(showline=True, linewidth=1, linecolor='black')
        # fig.update_yaxes(showline=True, linewidth=1, linecolor='black')

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

        return {}


if __name__ == '__main__':
    app.run_server(debug=True)
