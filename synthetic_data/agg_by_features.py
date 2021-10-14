import random
import pandas as pd
from datetime import datetime


def make_features_one_month(month):
    countries = ['Afghanistan', 'Albania', 'Algeria', 'Andorra', 'Angola', 'Antigua & Deps',
                 'Argentina', 'Armenia', 'Australia', 'Austria', 'Azerbaijan', 'Bahamas',
                 'Bahrain', 'Bangladesh', 'Barbados', 'Belarus', 'Belgium', 'Belize', 'Benin',
                 'Bhutan', 'Bolivia', 'Bosnia Herzegovina', 'Botswana', 'Brazil', 'Brunei',
                 'Bulgaria', 'Burkina', 'Burundi', 'Cambodia', 'Cameroon', 'Canada', 'Cape Verde',
                 'Central African Rep']

    features_df = pd.DataFrame(columns=['country_name', 'code', 'period_id', 'corporate_tax_is_high',
                                        'income_tax_is_high', 'country_risk', 'all_txn_credit_amt_7d',
                                        'all_txn_debit_amt_7d', 'is_outlier'])
    for country in countries:
        corporate_tax = random.randint(0, 1)
        income_tax = random.randint(0, 1)
        country_risk = random.randint(0, 3)
        credit = random.normalvariate(0, 1)
        debit = random.normalvariate(0, 1)
        outlier = random.randint(0, 1)
        features_df = features_df.append({'country_name': country.upper(),
                                          'code': 'AA',
                                          'period_id': month,
                                          'corporate_tax_is_high': corporate_tax,
                                          'income_tax_is_high': income_tax,
                                          'country_risk': country_risk,
                                          'all_txn_credit_amt_7d': credit,
                                          'all_txn_debit_amt_7d': debit,
                                          'is_outlier': outlier},
                                         ignore_index=True)

    return features_df


def make_features_many_months():
    d1 = datetime.strptime('1/2/2021', '%d/%m/%Y')
    d2 = datetime.strptime('1/3/2021', '%d/%m/%Y')
    d3 = datetime.strptime('1/4/2021', '%d/%m/%Y')
    durations = [d1, d2, d3]

    features_df = pd.DataFrame(columns=['country_name', 'code', 'period_id', 'corporate_tax_is_high',
                                        'income_tax_is_high', 'country_risk', 'all_txn_credit_amt_7d',
                                        'all_txn_debit_amt_7d', 'is_outlier'])

    for month in durations:
        features_df = features_df.append(make_features_one_month(month))

    features = features_df.columns[3:-1]
    return features_df, features


def make_axis_features_one_month(month):
    features_df, features = make_features_many_months()
    countries = ['Afghanistan', 'Albania', 'Algeria', 'Andorra', 'Angola', 'Antigua & Deps',
                 'Argentina', 'Armenia', 'Australia', 'Austria', 'Azerbaijan', 'Bahamas',
                 'Bahrain', 'Bangladesh', 'Barbados', 'Belarus', 'Belgium', 'Belize', 'Benin',
                 'Bhutan', 'Bolivia', 'Bosnia Herzegovina', 'Botswana', 'Brazil', 'Brunei',
                 'Bulgaria', 'Burkina', 'Burundi', 'Cambodia', 'Cameroon', 'Canada', 'Cape Verde',
                 'Central African Rep']

    axis_df = pd.DataFrame(columns=['country', 'period_id', 'f_x', 'f_y', 'f_z'])

    for country in countries:
        fx = features[random.randint(0, len(features) - 1)]
        fy = features[random.randint(0, len(features) - 1)]
        fz = features[random.randint(0, len(features) - 1)]
        axis_df = axis_df.append({'country': country.upper(),
                                  'period_id': month,
                                  'f_x': fx,
                                  'f_y': fy,
                                  'f_z': fz},
                                 ignore_index=True)

    return axis_df


def make_axis_features_many_month():
    d1 = datetime.strptime('1/2/2021', '%d/%m/%Y')
    d2 = datetime.strptime('1/3/2021', '%d/%m/%Y')
    d3 = datetime.strptime('1/4/2021', '%d/%m/%Y')
    durations = [d1, d2, d3]

    axis_df = pd.DataFrame(columns=['country', 'period_id', 'f_x', 'f_y', 'f_z'])

    for month in durations:
        axis_df = axis_df.append(make_axis_features_one_month(month))

    return axis_df

