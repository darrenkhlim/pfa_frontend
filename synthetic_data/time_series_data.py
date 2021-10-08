import random
import pandas as pd
from datetime import timedelta, datetime

def make_data_table():
    countries = ['Afghanistan', 'Albania', 'Algeria', 'Andorra', 'Angola', 'Antigua & Deps',
                 'Argentina', 'Armenia', 'Australia', 'Austria', 'Azerbaijan', 'Bahamas',
                 'Bahrain', 'Bangladesh', 'Barbados', 'Belarus', 'Belgium', 'Belize', 'Benin',
                 'Bhutan', 'Bolivia', 'Bosnia Herzegovina', 'Botswana', 'Brazil', 'Brunei',
                 'Bulgaria', 'Burkina', 'Burundi', 'Cambodia', 'Cameroon', 'Canada', 'Cape Verde',
                 'Central African Rep']

    data_table = pd.DataFrame(columns=['Country', 'QtQ amount change credit (%)',
                                       'QtQ amount change debit (%)', 'Risk Score'])
    for country in countries:
        debit = random.randint(-100,100)
        credit = random.randint(-100,100)
        ai_score = random.randint(0, 100)
        data_table = data_table.append({'Country': country, 'QtQ amount change credit (%)': credit,
                                        'QtQ amount change debit (%)': debit, 'Risk Score': ai_score},
                                        ignore_index=True)
    return data_table

def make_country_data(country, moving_window):
    agg_num = []
    d1 = datetime.strptime('1/1/2020', '%d/%m/%Y')
    d2 = datetime.strptime('1/12/2023', '%d/%m/%Y')
    duration = pd.date_range(d1, d2 - timedelta(days=7), freq='w')
    week_idx = [i for i in range(len(duration))]
    agg_amount = [random.randint(1000, 10000) for i in range(len(duration))]
    agg_count = [random.randint(1, 20) for i in range(len(duration))]
    country = [country] * len(duration)
    agg = pd.DataFrame(data={'week': duration, 'week_idx': week_idx, 'agg_amount': agg_amount, 'agg_count': agg_count,
                             'country_name': country})
    agg['mv_mean'] = agg.iloc[:, 2].rolling(moving_window).mean()
    agg['mv_std'] = agg.iloc[:, 2].rolling(moving_window).std()
    agg['upper'] = agg['mv_mean'] + 1.96 * agg['mv_std']
    agg['lower'] = agg['mv_mean'] - 1.96 * agg['mv_std']

    return agg

def make_synthetic_data(time_series_df):
    time_series_df.reset_index(inplace=True, drop=True)
    for i in range(round(0.02 * time_series_df.shape[0])):
        time_series_df.at[random.randint(0, time_series_df.index[-1]), 'agg_amount'] = random.randint(10000, 20000)
        time_series_df.at[random.randint(0, time_series_df.index[-1]), 'agg_amount'] = random.randint(100, 1000)
    return time_series_df

def time_series_data():
    countries = ['Afghanistan', 'Albania', 'Algeria', 'Andorra', 'Angola', 'Antigua & Deps',
                 'Argentina', 'Armenia', 'Australia', 'Austria', 'Azerbaijan', 'Bahamas',
                 'Bahrain', 'Bangladesh', 'Barbados', 'Belarus', 'Belgium', 'Belize', 'Benin',
                 'Bhutan', 'Bolivia', 'Bosnia Herzegovina', 'Botswana', 'Brazil', 'Brunei',
                 'Bulgaria', 'Burkina', 'Burundi', 'Cambodia', 'Cameroon', 'Canada', 'Cape Verde',
                 'Central African Rep']
    agg_num = []
    for country in countries:
        agg_country = make_country_data(country, 26)
        agg_num.append(agg_country)

    agg = pd.concat(agg_num, axis=0)
    return make_synthetic_data(agg)

def anomalies_df(time_series_df):
    anomalies = time_series_df[(time_series_df.agg_amount < time_series_df.lower) | (time_series_df.agg_amount > time_series_df.upper)]
    return anomalies
