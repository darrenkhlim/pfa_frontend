import json
import sqlite3
import numpy as np
import pandas as pd
from synthetic_data.agg_by_features import make_axis_features_many_month, make_features_many_months


CONFIG = json.load(open('./pfa_dash/config/config_dash.json'))


def text_header(country, features_df, data_source=CONFIG['data_source']):
    """ Prepares the features dataframe for plotly visualization
    :param country: country of interest
    :type country: String
    :param features_df: transactional and risk features of countries
    :type features_df: pd.DataFrame
    :param data_source: directs the data source towards synthetic ('syn') or actual transaction data ('db')
    :type data_source: String
    ...
    :return: processed features dataframe
    :rtype: pd.DataFrame

    """
    if data_source == 'syn':
        axis_df = make_axis_features_many_month()
    elif data_source == 'db':
        axis_df = axis_features(db_path=CONFIG['features_db_path'])
    else:
        raise ValueError("data_source could only take values from 'syn' or 'db'!")

    extracted_row = axis_df.loc[axis_df['country'] == country]  # extract the country of interest (contains axis + dt)
    extracted_period = extracted_row.iloc[0]['period_id']  # extract the period for that country
    extracted_axes = list(extracted_row.iloc[0][['f_x', 'f_y', 'f_z']])  # extract the axes for that country
    features_df['period_id'] = features_df['period_id'].str[:10]  # remove 00:00:00
    features_df = features_df.loc[features_df['period_id'] == extracted_period]  # filter the main frame by period
    features_df = rename_features_header(features_df)  # rename the headers to the more explainable one

    plot_df = features_df[extracted_axes]  # filter the main frame to the required axes only
    plot_df['result'] = features_df['is_outlier']
    plot_df['country'] = features_df['country_name']
    plot_df['header'] = np.where(features_df['is_outlier'] == 1.0, plot_df['country'], '')

    return plot_df


def make_features_df(data_source=CONFIG['data_source']):
    """ Extract features dataframe containing countries and their associated feature (transactional & risk) values
    :param data_source: directs the data source towards synthetic ('syn') or actual transaction data ('db')
    :type data_source: String
    ...
    :return: features dataframe (& features of data source is 'db')
    :rtype: pd.DataFrame (& list)
    """
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
    """ rename features to business oriented naming conventions
    :param features_df: transactional and risk features of countries
    :type features_df: pd.DataFrame
    ...
    :return: renamed features df
    :rtype: pd.DataFrame
    """
    new_headers = []
    feature_headers = features_df.columns
    for feature in feature_headers:
        if feature not in CONFIG['feature_meaning'].keys():
            new_headers.append(feature)
        else:
            new_headers.append(CONFIG['feature_meaning'][feature])
    features_df.columns = new_headers
    return features_df


def read_from_db(query_sql, db_path):
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
    """ Query top 3 features of anomalous countries
    :param db_path: directory for db file
    :type db_path: String
    ...
    :return: dataframe containing top 3 features for detected countries based on shapley values
    :rtype: pd.DataFrame
    """
    query = '''SELECT * FROM AXIS_FEATURES'''
    return read_from_db(query, db_path)


def all_countries_features(db_path):
    """ Query features data
    :param db_path: directory for db file
    :type db_path: String
    ...
    :return: dataframe containing feature values for each country
    :rtype: pd.DataFrame
    """
    query = '''SELECT * FROM ALL_COUNTRIES_FEATURES'''
    return read_from_db(query, db_path)
