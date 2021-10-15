import json
import numpy as np
from synthetic_data.agg_by_features import make_axis_features_many_month, make_features_many_months
import sqlite3
import pandas as pd

CONFIG = json.load(open('D:\payment_flow_analytics\pfa_dash\config\config_dash.json'))


def text_header(country, features_df, data_source=CONFIG['data_source']):
    if data_source == 'syn':
        axis_df = make_axis_features_many_month()
    elif data_source == 'db':
        axis_df = all_countries_features(db_path=CONFIG['features_db_path'])
    else:
        raise ValueError("data_source could only take values from 'syn' or 'db'!")

    latest_month = features_df['period_id'].unique()[-1]
    features_df = features_df.loc[features_df['period_id'] == latest_month]
    axis_df = axis_df.loc[axis_df['period_id'] == latest_month]
    axes = axis_df.loc[axis_df.country == country].values[0][2:]
    features_df = rename_features_header(features_df)

    plot_df = features_df[axes]
    plot_df['result'] = features_df['is_outlier']
    plot_df['country'] = features_df['country_name']
    plot_df['header'] = np.where(features_df['is_outlier'] == 1.0, plot_df['country'], '')

    return plot_df


def make_features_df(data_source=CONFIG['data_source']):
    if data_source == 'syn':
        return make_features_many_months()
    elif data_source == 'db':
        features_df = all_countries_features(db_path=CONFIG['features_db_path'])
        features = features_df.columns[3:-1]
        return features_df, features
    else:
        raise ValueError("data_source could only take values from 'syn' or 'db'!")
        return


def rename_features_header(features_df):
    new_headers = []
    feature_headers = features_df.columns
    for feature in feature_headers:
        if feature not in CONFIG['feature_meaning'].keys():
            new_headers.append(feature)
        else:
            new_headers.append(CONFIG['feature_meaning'][feature])
    features_df.columns = new_headers
    return features_df


def read_from_db(query_sql, db_path):  # TODO: need move to utils
    """ Read from SQLiteDB
    :param query_sql: SQL query
    :type query_sql: String
    :param db_path: path of the db
    :type db_path: String
    ...
    :return: dataframe with values in the list as one column
    :rtype: pd.DataFrame
    """
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query(query_sql, conn)
    conn.close()
    return df


def axis_features(db_path):
    query = '''SELECT * FROM AXIS_FEATURES'''
    return read_from_db(query, db_path)


def all_countries_features(db_path):
    query = '''SELECT * FROM ALL_COUNTRIES_FEATURES'''
    return read_from_db(query, db_path)
