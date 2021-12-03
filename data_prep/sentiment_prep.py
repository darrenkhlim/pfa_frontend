from synthetic_data.sentiment import make_sentiments
import pandas as pd
import sqlite3
import json

CONFIG = json.load(open('./pfa_dash/config/config_dash.json'))


def sentiments_redefined_polarity(data_source=CONFIG['data_source']):
    """ Formatting changes for the news sentiment data
    :param data_source: directs the data source towards synthetic ('syn') or actual transaction data ('db')
    :type data_source: String
    ...
    :return: processed news sentiment dataframe
    :rtype: pd.DataFrame
    """
    if data_source == 'syn':
        sentiments_df = make_sentiments()
    elif data_source == 'db':
        sentiments_df = sentiments(db_path=CONFIG['sentiment_db_path'])
    else:
        raise ValueError("data_source could only take values from 'syn' or 'db'!")

    sentiments_df = sentiments_df.iloc[:, :4]
    sentiments_df = sentiments_df.round({'polarity': 2})
    sentiments_df['firstcreated'] = sentiments_df['firstcreated'].str[:10]
    cols = ['country_name', 'headline', 'firstcreated', 'polarity']
    sentiments_df = sentiments_df[cols]
    sentiments_df = sentiments_df.rename(columns={'country_name': 'Country',
                                                  'headline': 'Headline',
                                                  'firstcreated': 'Date',
                                                  'polarity': 'Polarity'})
    return sentiments_df


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


def sentiments(db_path):
    """ Query news data
    :param db_path: directory for db file
    :type db_path: String
    ...
    :return: dataframe containing news for each country
    :rtype: pd.DataFrame
    """
    query = '''SELECT * FROM sentiment'''
    return read_from_db(query, db_path)
