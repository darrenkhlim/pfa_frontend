import random
import pandas as pd


def make_pca_data():
    countries = ['Afghanistan', 'Albania', 'Algeria', 'Andorra', 'Angola', 'Antigua & Deps',
                 'Argentina', 'Armenia', 'Australia', 'Austria', 'Azerbaijan', 'Bahamas',
                 'Bahrain', 'Bangladesh', 'Barbados', 'Belarus', 'Belgium', 'Belize', 'Benin',
                 'Bhutan', 'Bolivia', 'Bosnia Herzegovina', 'Botswana', 'Brazil', 'Brunei',
                 'Bulgaria', 'Burkina', 'Burundi', 'Cambodia', 'Cameroon', 'Canada', 'Cape Verde',
                 'Central African Rep']

    pca_df = pd.DataFrame(columns=['PC_1', 'PC_2', 'PC_3', 'result'])

    for i in range(len(countries)):
        pc1, pc2, pc3 = random.normalvariate(0, 1), random.normalvariate(0, 1), random.normalvariate(0, 1)
        result = random.randint(0, 1)
        pca_df = pca_df.append({'PC_1': pc1,
                                'PC_2': pc2,
                                'PC_3': pc3,
                                'result': result},
                               ignore_index=True)

    return pca_df
