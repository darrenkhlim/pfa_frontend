import numpy as np
import pandas as pd
from sklearn.decomposition import PCA

def features_pca(features_df, features):
    only_features_df = features_df[features]
    features_np = np.asarray(only_features_df, dtype='float64')
    pca = PCA(n_components=3)
    principalComponents = pca.fit_transform(features_np)
    components_df = pd.DataFrame(principalComponents, columns=['PC_1', 'PC_2', 'PC_3'])
    comp_normalized= (components_df - components_df.mean())/components_df.std()
    comp_normalized['result'] = features_df['is_outlier']
    comp_normalized['header'] = np.where(comp_normalized['result'] == 1.0, features_df['country'], '')
    comp_normalized['country'] = features_df['country']
    comp_normalized.loc[comp_normalized.result == 0.0, 'colour'] = 'b'
    comp_normalized.loc[comp_normalized.result == 1.0, 'colour'] = 'r'
    return comp_normalized

