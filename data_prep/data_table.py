import pandas as pd
from synthetic_data.qtq_change_by_country_name import qtq_change_many_months
from synthetic_data.risk_score_and_seasonality import risk_score_and_seasonality_many_months


def make_data_table():
    ## Import Data
    qtq_change_by_country_name = qtq_change_many_months()
    risk_score_and_seasonality = risk_score_and_seasonality_many_months()

    merged_table = pd.merge(qtq_change_by_country_name, risk_score_and_seasonality, on='country_name', suffixes=('_left', '_right'))
    merged_table = merged_table.loc[merged_table['selected_month_left'] == merged_table['selected_month_right']]
    latest_month = merged_table['selected_month_left'].unique()[-1]
    merged_table_latest_month = merged_table.loc[merged_table['selected_month_left'] == latest_month]

    country = merged_table_latest_month['country_name']
    qtq_debit = merged_table_latest_month['qtq_change_inflow']
    qtq_credit = merged_table_latest_month['qtq_change_outflow']
    risk_score = merged_table_latest_month['risk_score_ma']

    data_table = pd.DataFrame(data={'Country': country,
                                    'QtQ amount change credit (%)': qtq_debit.round(2),
                                    'QtQ amount change debit (%)': qtq_credit.round(2),
                                    'Risk Score': risk_score.round(2)})
    return data_table