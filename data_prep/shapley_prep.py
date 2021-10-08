import shap
import pandas as pd
from pyod.models.iforest import IForest
from collections import OrderedDict

def iforest_shap(features_df, features):
    if 'is_outlier' in features_df.columns:
        forest_df = features_df.copy().drop('is_outlier', axis=1)
    forest_df, if_features = features_df.copy(), features
    columns_to_norm = forest_df.columns[1:-1]
    forest_df[columns_to_norm] = forest_df[columns_to_norm].apply(lambda x: (x - x.mean()) / x.std())

    forest_clf = IForest(contamination=0.03, random_state=42)
    forest_clf.fit(forest_df[if_features])
    y_pred = forest_clf.predict(forest_df[if_features])
    forest_df['is_outlier'] = y_pred

    explainer = shap.TreeExplainer(forest_clf)
    shap_values = explainer.shap_values(forest_df[if_features])
    shap_df = pd.DataFrame(shap_values, columns=[f'shap_{f}' for f in if_features])
    df_with_shap = pd.concat([forest_df, shap_df], axis=1)
    shap_cols = [c for c in df_with_shap.columns if c.startswith('shap')]

    return df_with_shap, shap_cols

