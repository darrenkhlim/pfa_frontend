import random
from synthetic_data.agg_by_features import make_features_df


def iforest_prediction(features_df):
    outlier = [random.randint(0,1) for i in range(len(features_df.index))]
    features_df['is_outlier'] = outlier
    return features_df


def make_shap_df():
    countries = ['Afghanistan', 'Albania', 'Algeria', 'Andorra', 'Angola', 'Antigua & Deps',
                 'Argentina', 'Armenia', 'Australia', 'Austria', 'Azerbaijan', 'Bahamas',
                 'Bahrain', 'Bangladesh', 'Barbados', 'Belarus', 'Belgium', 'Belize', 'Benin',
                 'Bhutan', 'Bolivia', 'Bosnia Herzegovina', 'Botswana', 'Brazil', 'Brunei',
                 'Bulgaria', 'Burkina', 'Burundi', 'Cambodia', 'Cameroon', 'Canada', 'Cape Verde',
                 'Central African Rep']

    features_df, features = make_features_df()
    features_df = iforest_prediction(features_df)
    features_shap = list(map(lambda x: 'shap_' + x, features))
    for feature in features_shap:
        values = [random.normalvariate(0, 1) for i in range(len(countries))]
        features_df[feature] = values

    return features_df, features_shap







