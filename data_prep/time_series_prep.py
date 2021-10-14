import numpy as np
import pandas as pd
import sqlite3


def upper_lower(agg):
    agg['upper'] = agg['mv_mean'] + 1.96*agg['mv_std']
    agg['lower'] = agg['mv_mean'] - 1.96*agg['mv_std']
    return agg

def set_interpolated_zero(agg):
    agg['agg_amount'] = np.where((agg.raw_data_ind == 1), agg.agg_amount, 0)
    agg['agg_count'] = np.where((agg.raw_data_ind == 1), agg.agg_count, 0)
    return agg

def anomalies_df(agg):
    anomalies = agg[(agg.agg_amount < agg.lower) | (agg.agg_amount > agg.upper)]
    return anomalies

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

def qtq_change_by_country_name_from_db(db_path):
    query = '''SELECT * FROM qtq_change_by_country_name'''
    return read_from_db(query, db_path)

def risk_score_and_seasonality_from_db(db_path):
    query = '''SELECT * FROM risk_score_and_seasonality'''
    return read_from_db(query, db_path)

def agg_txn_by_country_name_from_db(db_path):
    query = '''SELECT * FROM agg_txn_by_country_name'''
    return read_from_db(query, db_path)