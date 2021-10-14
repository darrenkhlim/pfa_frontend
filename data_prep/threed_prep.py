import numpy as np
from synthetic_data.agg_by_features import make_axis_features_many_month


def text_header(country, features_df):
    latest_month = features_df['period_id'].unique()[-1]
    features_df = features_df.loc[features_df['period_id'] == latest_month]

    axis_df = make_axis_features_many_month()  # entry point to change df
    axis_df = axis_df.loc[axis_df['period_id'] == latest_month]
    axes = axis_df.loc[axis_df.country == country].values[0][2:]

    plot_df = features_df[axes]
    plot_df['result'] = features_df['is_outlier']
    plot_df['country'] = features_df['country_name']
    plot_df['header'] = np.where(features_df['is_outlier'] == 1.0, plot_df['country'], '')

    return plot_df

