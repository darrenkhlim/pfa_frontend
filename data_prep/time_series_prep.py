import numpy as np
import pandas as pd
import sqlite3


def upper_lower(agg):
    """ Inserts two additional column to denote the 95% confidence interval
    :param agg: time series data aggregated by country names
    :type agg: pd.DataFrame
    ...
    :return: two additional columns of 'upper' and 'lower'
    :rtype: pd.DataFrame
    """
    agg['upper'] = agg['mv_mean'] + 1.96*agg['mv_std']
    agg['lower'] = agg['mv_mean'] - 1.96*agg['mv_std']
    return agg


def set_interpolated_zero(agg):
    """ Replace interpolated calculations (aggregated amount & aggregated count) with 0
    :param agg: time series data aggregated by country names
    :type agg: pd.DataFrame
    ...
    :return: revised time series data
    :rtype: pd.DataFrame
    """
    agg['agg_amount'] = np.where((agg.raw_data_ind == 1), agg.agg_amount, 0)
    agg['agg_count'] = np.where((agg.raw_data_ind == 1), agg.agg_count, 0)
    return agg


def anomalies_df(agg):
    """ Sieve out row data that are anomalous based on the % confidence interval
    :param agg: time series data aggregated by country names
    :type agg: pd.DataFrame
    ...
    :return: all anomalous data
    :rtype: pd.DataFrame
    """
    anomalies = agg[(agg.agg_amount < agg.lower) | (agg.agg_amount > agg.upper)]
    return anomalies


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


def qtq_change_by_country_name_from_db(db_path):
    """ Query quarter-on-quarter dataframe
    :param db_path: directory for db file
    :type db_path: String
    ...
    :return: dataframe containing qtq transactional changes
    :rtype: pd.DataFrame
    """
    query = '''SELECT * FROM qtq_change_by_country_name'''
    return read_from_db(query, db_path)


def risk_score_and_seasonality_from_db(db_path):
    """ Query risk score and seasonality dataframe
    :param db_path: directory for db file
    :type db_path: String
    ...
    :return: dataframe containing risk scores and seasonality
    :rtype: pd.DataFrame
    """
    query = '''SELECT * FROM risk_score_and_seasonality'''
    return read_from_db(query, db_path)


def agg_txn_by_country_name_from_db(db_path):
    """ Query time series dataframe
    :param db_path: directory for db file
    :type db_path: String
    ...
    :return: dataframe containing transactional data
    :rtype: pd.DataFrame
    """
    query = '''SELECT * FROM agg_txn_by_country_name'''
    return read_from_db(query, db_path)