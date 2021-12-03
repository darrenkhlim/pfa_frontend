import pandas as pd
import random
import string


def make_sentiments():
    """ Creates synthetic sentiment data
    :return: synthetic sentiment data
    :rtype: pd.DataFrame
    """
    countries = ['CAYMAN', 'MYANMAR', 'ST. LUCIA', 'FINLAND']
    total_data = 2800

    sentiment = pd.DataFrame(columns=['headline', 'firstcreated', 'country_name', 'polarity', 'tb_pa_polarity',
                                      'tb_nb_classification', 'tb_nb_p_pos', 'tb_nb_p_neg', 'vader_neg', 'vader_neu',
                                      'vader_pos', 'vader_compound', 'transformer_label'])
    for country in countries:
        for data in range(int(total_data/4)):
            time1 = str(random.randint(1, 30))
            time2 = str(random.randint(0, 24))
            time3 = str(random.randint(0, 59))
            time4 = str(random.randint(0, 59))

            if len(time1) == 1:
                time1 = '0' + time1
            if len(time2) == 1:
                time2 = '0' + time2
            if len(time3) == 1:
                time3 = '0' + time3
            if len(time4) == 1:
                time4 = '0' + time4

            time = "2021-0" + str(random.randint(1, 4)) + "-" + time1 + " " + time2 + ":" + time3 + ":" + time4
            headline = ''.join(random.choices(string.ascii_uppercase + string.digits, k=random.randint(80, 200)))
            polarity = random.uniform(-1, 1)
            tb_polarity = random.uniform(-1, 1)
            tb_nb_class = random.sample(['pos', 'neg'], 1)[0]
            tb_nb_pos = random.uniform(0, 1)
            tb_nb_neg = 1 - tb_nb_pos
            vader_neg = random.uniform(0, 1)
            vader_neu = random.uniform(0, 1)
            vader_pos = 1 - vader_neu - vader_neg
            vader_compound = random.normalvariate(0, 1)
            transformer = random.randint(1, 5)

            sentiment = sentiment.append({'headline': headline,
                                          'firstcreated': time,
                                          'country_name': country,
                                          'polarity': polarity,
                                          'tb_pa_polarity': tb_polarity,
                                          'tb_nb_classification': tb_nb_class,
                                          'tb_nb_p_pos': tb_nb_pos,
                                          'tb_nb_p_neg': tb_nb_neg,
                                          'vader_neg': vader_neg,
                                          'vader_neu': vader_neu,
                                          'vader_pos': vader_pos,
                                          'vader_compound': vader_compound,
                                          'transformer_label': transformer
                                          }, ignore_index=True)

    return sentiment