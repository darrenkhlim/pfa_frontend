import random
import pandas as pd


def make_country_data(country, moving_window):
    """ Create synthetic time series data for a particular country
    :param country: country of interest
    :type country: String
    :param moving_window: moving average window length
    :type moving_window: int
    ...
    :return: time series data with randomized aggregate amount & count for a particular country
    :rtype: pd.DataFrame
    """
    duration = pd.date_range('6-1-2017', '4-1-2021', freq='MS').strftime("%Y-%m").tolist()
    duration = list(map(lambda x: str(x), duration))
    begin_date = []
    for year_month in duration:
        year_month_str = str(year_month) + '-01'
        begin_date.append(year_month_str)
    month_idx = [i for i in range(len(duration))]
    agg_amount = [random.randint(1000, 10000) for i in range(len(duration))]
    agg_count = [random.randint(1, 20) for i in range(len(duration))]
    raw_data_ind = [random.randint(0, 1) for i in range(len(duration))]
    country = [country.upper()] * len(duration)
    agg = pd.DataFrame(data={'month': duration, 'month_idx': month_idx, 'agg_amount': agg_amount, 'agg_count': agg_count,
                             'raw_data_ind': raw_data_ind, 'begin_date': begin_date})
    agg['mv_mean'] = agg.loc[:, 'agg_amount'].rolling(moving_window).mean()
    agg['mv_std'] = agg.loc[:, 'agg_amount'].rolling(moving_window).std()
    agg['country_name'] = country
    return agg


def make_outliers(time_series_df):
    """ Changes aggregate amount values to force outlier data
    :param time_series_df: time series dataframe
    :type time_series_df: pd.DataFrame
    ...
    :return: time series dataframe with outlier
    :rtype: pd.DataFrame
    """
    time_series_df.reset_index(inplace=True, drop=True)
    for i in range(round(0.02 * time_series_df.shape[0])):
        time_series_df.at[random.randint(0, time_series_df.index[-1]), 'agg_amount'] = random.randint(10000, 20000)
        time_series_df.at[random.randint(0, time_series_df.index[-1]), 'agg_amount'] = random.randint(100, 1000)
    return time_series_df


def agg_txn_by_country_names():
    """ Create synthetic time series data for a group of countries
    :return: times series data for several countries
    :rtype: pd.DataFrame
    """
    countries = ['Afghanistan', 'Albania', 'Algeria', 'Andorra', 'Angola', 'Antigua & Deps',
                 'Argentina', 'Armenia', 'Australia', 'Austria', 'Azerbaijan', 'Bahamas',
                 'Bahrain', 'Bangladesh', 'Barbados', 'Belarus', 'Belgium', 'Belize', 'Benin',
                 'Bhutan', 'Bolivia', 'Bosnia Herzegovina', 'Botswana', 'Brazil', 'Brunei',
                 'Bulgaria', 'Burkina', 'Burundi', 'Cambodia', 'Cameroon', 'Canada', 'Cape Verde',
                 'Central African Rep', 'Cayman', 'Myanmar']
    agg_num = []
    for country in countries:
        agg_country = make_country_data(country, 13)
        agg_num.append(agg_country)

    agg = pd.concat(agg_num, axis=0)
    return make_outliers(agg)

