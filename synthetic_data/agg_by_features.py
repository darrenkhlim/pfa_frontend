import random
import json
import pandas as pd

CONFIG = json.load(open('./pfa_dash/config/config_dash.json'))


def make_features_one_month(month):
    """ Create synthetic feature values for a particular month
    :param month: month of interest
    :type month: String
    ...
    :return: sample features for all countries in a month
    :rtype: pd.DataFrame
    """
    countries = ['Afghanistan', 'Albania', 'Algeria', 'Angola', 'Antigua & Deps',
                 'Argentina', 'Armenia', 'Australia', 'Austria', 'Azerbaijan', 'Bahamas',
                 'Bahrain', 'Bangladesh', 'Barbados', 'Belarus', 'Belgium', 'Belize', 'Benin',
                 'Bhutan', 'Bolivia', 'Bosnia Herzegovina', 'Botswana', 'Brazil', 'Brunei',
                 'Bulgaria', 'Burkina', 'Burundi', 'Cambodia', 'Cameroon', 'Canada', 'Cape Verde',
                 'Central African Rep', 'Cayman', 'Myanmar']

    features_df = pd.DataFrame(columns=['country_name', 'code', 'period_id', "all_txn_total_avg_14d",
                                        "all_txn_total_amt_7d", "all_txn_credit_avg_150d", "all_txn_debit_ct_90d",
                                        "all_txn_credit_avg_30d", 'is_outlier'])
    for country in countries:
        txn_total_avg_14d = random.lognormvariate(0, 1)
        txn_total_amt_7d = random.lognormvariate(0, 1)
        txn_credit_avg_150d = random.lognormvariate(0, 1)
        txn_debit_ct_90d = random.lognormvariate(0, 1)
        txn_credit_avg_30d = random.lognormvariate(0, 1)
        outlier = random.randint(0, 1)
        features_df = features_df.append({'country_name': country.upper(),
                                          'code': 'AA',
                                          'period_id': month,
                                          "all_txn_total_avg_14d": txn_total_avg_14d,
                                          "all_txn_total_amt_7d": txn_total_amt_7d,
                                          "all_txn_credit_avg_150d": txn_credit_avg_150d,
                                          "all_txn_debit_ct_90d": txn_debit_ct_90d,
                                          "all_txn_credit_avg_30d": txn_credit_avg_30d,
                                          'is_outlier': outlier},
                                         ignore_index=True)

    return features_df


def make_features_many_months():
    """ Create synthetic feature values for numerous months
    :return: sample features for all countries in a range of months & feature names
    :rtype: pd.DataFrame & list
    """
    d1 = '2021-02-01 00:00:00'
    d2 = '2021-03-01 00:00:00'
    d3 = '2021-04-01 00:00:00'
    durations = [d1, d2, d3]

    features_df = pd.DataFrame(columns=['country_name', 'code', 'period_id', "all_txn_total_avg_14d",
                                        "all_txn_total_amt_7d", "all_txn_credit_avg_150d", "all_txn_debit_ct_90d",
                                        "all_txn_credit_avg_30d", 'is_outlier'])

    for month in durations:
        features_df = features_df.append(make_features_one_month(month))

    features = features_df.columns[3:-1]
    return features_df, features


def make_axis_features_one_month(month):
    """ Create synthetic top 3 features for each country in a given month
    :param month: month of interest
    :type month: String
    ...
    :return: sample top 3 features for all countries in a given month
    :rtype: pd.DataFrame
    """
    features_df, features = make_features_many_months()
    countries = ['Afghanistan', 'Albania', 'Algeria', 'Andorra', 'Angola', 'Antigua & Deps',
                 'Argentina', 'Armenia', 'Australia', 'Austria', 'Azerbaijan', 'Bahamas',
                 'Bahrain', 'Bangladesh', 'Barbados', 'Belarus', 'Belgium', 'Belize', 'Benin',
                 'Bhutan', 'Bolivia', 'Bosnia Herzegovina', 'Botswana', 'Brazil', 'Brunei',
                 'Bulgaria', 'Burkina', 'Burundi', 'Cambodia', 'Cameroon', 'Canada', 'Cape Verde',
                 'Central African Rep', 'Cayman', 'Myanmar']

    axis_df = pd.DataFrame(columns=['country', 'period_id', 'f_x', 'f_y', 'f_z'])

    for country in countries:
        fx = CONFIG['feature_meaning'][features[random.randint(0, len(features) - 1)]]
        fy = CONFIG['feature_meaning'][features[random.randint(0, len(features) - 1)]]
        fz = CONFIG['feature_meaning'][features[random.randint(0, len(features) - 1)]]
        axis_df = axis_df.append({'country': country.upper(),
                                  'period_id': month,
                                  'f_x': fx,
                                  'f_y': fy,
                                  'f_z': fz},
                                 ignore_index=True)

    return axis_df


def make_axis_features_many_month():
    """ Create synthetic top 3 features for numerous months
    :return: sample top 3features for all countries in a range of months
    :rtype: pd.DataFrame
    """
    d1 = '2021-02-01'
    durations = [d1]
    axis_df = pd.DataFrame(columns=['country', 'period_id', 'f_x', 'f_y', 'f_z'])
    for month in durations:
        axis_df = axis_df.append(make_axis_features_one_month(month))

    return axis_df
