import random
import pandas as pd

def make_features_df():
    countries = ['Afghanistan', 'Albania', 'Algeria', 'Andorra', 'Angola', 'Antigua & Deps',
                 'Argentina', 'Armenia', 'Australia', 'Austria', 'Azerbaijan', 'Bahamas',
                 'Bahrain', 'Bangladesh', 'Barbados', 'Belarus', 'Belgium', 'Belize', 'Benin',
                 'Bhutan', 'Bolivia', 'Bosnia Herzegovina', 'Botswana', 'Brazil', 'Brunei',
                 'Bulgaria', 'Burkina', 'Burundi', 'Cambodia', 'Cameroon', 'Canada', 'Cape Verde',
                 'Central African Rep']

    features_df = pd.DataFrame(columns=['country', 'corporate_tax_is_high', 'income_tax_is_high',
                                        'country_risk', 'all_txn_credit_amt_7d', 'all_txn_debit_amt_7d'])
    for country in countries:
        corporate_tax = random.randint(0, 1)
        income_tax = random.randint(0, 1)
        country_risk = random.randint(0, 3)
        credit = random.randint(10000, 100000)
        debit = random.randint(10000, 100000)
        outlier = random.randint(0, 1)  # prediction from CBLOF
        features_df = features_df.append({'country': country.upper(), 'corporate_tax_is_high': corporate_tax,
                                          'income_tax_is_high': income_tax, 'country_risk': country_risk,
                                          'all_txn_credit_amt_7d': credit, 'all_txn_debit_amt_7d': debit,
                                          'is_outlier': outlier}, ignore_index=True)

    features = list(features_df.columns)[1:-1]

    return features_df, features

