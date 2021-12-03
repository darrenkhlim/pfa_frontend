import pandas as pd
import numpy as np
import random


def risk_score_and_seasonality_one_month(month):
    """ Create synthetic risk and seasonality scores for a given month
    :param month: month of interest
    :type month: String
    ...
    :return:  risk and seasonality scores for a given month
    :rtype: pd.DataFrame
    """
    countries = ['Afghanistan', 'Albania', 'Algeria', 'Andorra', 'Angola', 'Antigua & Deps',
                 'Argentina', 'Armenia', 'Australia', 'Austria', 'Azerbaijan', 'Bahamas',
                 'Bahrain', 'Bangladesh', 'Barbados', 'Belarus', 'Belgium', 'Belize', 'Benin',
                 'Bhutan', 'Bolivia', 'Bosnia Herzegovina', 'Botswana', 'Brazil', 'Brunei',
                 'Bulgaria', 'Burkina', 'Burundi', 'Cambodia', 'Cameroon', 'Canada', 'Cape Verde',
                 'Central African Rep', 'Cayman', 'Myanmar']

    risk_score = pd.DataFrame(columns=['country_name',
                                       'risk_score_ma',
                                       'selected_month',
                                       'risk_score_arima',
                                       'ch_sea_len',
                                       'length',
                                       'sea_decomp_score'])

    for country in range(len(countries)):
        risk_score_ma = random.normalvariate(0, 1)
        risk_score_arima = random.normalvariate(0, 1)
        ch_sea_len = random.uniform(0, 50)
        length = random.uniform(100, 200)
        sea_decomp_score = random.normalvariate(0, 1)
        risk_score = risk_score.append({'country_name': countries[country].upper(),
                                        'risk_score_ma': risk_score_ma,
                                        'selected_month': month,
                                        'risk_score_arima': risk_score_arima,
                                        'ch_sea_len': ch_sea_len,
                                        'length': int(length),
                                        'sea_decomp_score': np.abs(sea_decomp_score)},
                                       ignore_index=True)
    return risk_score


def risk_score_and_seasonality_many_months():
    """ Create synthetic risk and seasonality scores for a range of months
    :return: synthetic risk and seasonality scores for a range of months
    :rtype: pd.DataFrame
    """
    d1 = '2021-01-01'
    d2 = '2021-02-01'
    d3 = '2021-03-01'
    durations = [d1, d2, d3]
    risk_score_and_seasonality = pd.DataFrame(columns=['country_name',
                                                       'risk_score_ma',
                                                       'selected_month',
                                                       'risk_score_arima',
                                                       'ch_sea_len',
                                                       'length',
                                                       'sea_decomp_score'])
    for month in durations:
        risk_score_and_seasonality = risk_score_and_seasonality.append(risk_score_and_seasonality_one_month(month))

    return risk_score_and_seasonality
