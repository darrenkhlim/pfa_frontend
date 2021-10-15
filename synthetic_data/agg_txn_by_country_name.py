import random
import pandas as pd
from datetime import timedelta, datetime


def make_country_data(country, moving_window):
    d1 = datetime.strptime('1-1-2020', '%d-%m-%Y')
    d2 = datetime.strptime('1-12-2023', '%d-%m-%Y')
    duration = pd.date_range(d1, d2 - timedelta(days=7), freq='w').astype(str)
    week = []
    for i in duration:
        i = datetime.strptime(i, '%Y-%m-%d')
        week.append(str(i)+'/'+str(i+timedelta(days=6)))
    week_idx = [i for i in range(len(duration))]
    agg_amount = [random.randint(1000, 10000) for i in range(len(duration))]
    agg_count = [random.randint(1, 20) for i in range(len(duration))]
    raw_data_ind = [random.randint(0,1) for i in range(len(duration))]
    country = [country.upper()] * len(duration)
    agg = pd.DataFrame(data={'week': week, 'week_idx': week_idx, 'agg_amount': agg_amount, 'agg_count': agg_count,
                             'raw_data_ind': raw_data_ind, 'begin_date': duration})
    agg['mv_mean'] = agg.loc[:, 'agg_amount'].rolling(moving_window).mean()
    agg['mv_std'] = agg.loc[:, 'agg_amount'].rolling(moving_window).std()
    agg['country_name'] = country
    return agg


def make_outliers(time_series_df):
    time_series_df.reset_index(inplace=True, drop=True)
    for i in range(round(0.02 * time_series_df.shape[0])):
        time_series_df.at[random.randint(0, time_series_df.index[-1]), 'agg_amount'] = random.randint(10000, 20000)
        time_series_df.at[random.randint(0, time_series_df.index[-1]), 'agg_amount'] = random.randint(100, 1000)
    return time_series_df


def agg_txn_by_country_names():
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
    return make_outliers(agg)

