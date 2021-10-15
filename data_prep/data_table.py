import json
import pandas as pd
from synthetic_data.qtq_change_by_country_name import qtq_change_many_months
from synthetic_data.agg_txn_by_country_name import agg_txn_by_country_names
from synthetic_data.risk_score_and_seasonality import risk_score_and_seasonality_many_months
from data_prep.time_series_prep import qtq_change_by_country_name_from_db, risk_score_and_seasonality_from_db, \
    agg_txn_by_country_name_from_db

CONFIG = json.load(open('./pfa_dash/config/config_dash.json'))


def make_data_table(data_source=CONFIG['data_source']):
    # Import Data
    if data_source == 'syn':
        qtq_change_by_country_name = qtq_change_many_months()
        risk_score_and_seasonality = risk_score_and_seasonality_many_months()
    elif data_source == 'db':
        qtq_change_by_country_name = qtq_change_by_country_name_from_db(db_path=CONFIG['ts_db_path'])
        risk_score_and_seasonality = risk_score_and_seasonality_from_db(db_path=CONFIG['ts_db_path'])
    else:
        raise ValueError("data_source could only take values from 'syn' or 'db'!")

    merged_table = pd.merge(qtq_change_by_country_name, risk_score_and_seasonality, on='country_name',
                            suffixes=('_left', '_right'))
    merged_table = merged_table.loc[merged_table['selected_month_left'] == merged_table['selected_month_right']]
    latest_month = merged_table['selected_month_left'].unique()[-1]
    merged_table_latest_month = merged_table.loc[merged_table['selected_month_left'] == latest_month]

    country = merged_table_latest_month['country_name']
    qtq_debit = merged_table_latest_month['qtq_change_inflow']
    qtq_credit = merged_table_latest_month['qtq_change_outflow']
    risk_score = merged_table_latest_month['risk_score_ma']

    data_table = pd.DataFrame(data={'Country': country,
                                    'QtQ Amount Change Credit (%)': (qtq_debit * 100).round(0),
                                    'QtQ Amount Change Debit (%)': (qtq_credit * 100).round(0),
                                    'Risk Score': risk_score.round(2)})
    return data_table


def make_table_agg_txn_by_country_name(data_source=CONFIG['data_source']):
    if data_source == 'syn':
        return agg_txn_by_country_names()
    elif data_source == 'db':
        return agg_txn_by_country_name_from_db(db_path=CONFIG['ts_db_path'])
    else:
        raise ValueError("data_source could only take values from 'syn' or 'db'!")
        return
