import numpy as np


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