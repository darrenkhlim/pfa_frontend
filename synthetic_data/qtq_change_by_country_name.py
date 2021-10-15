import pandas as pd
import random


def qtq_change_one_month(month):
    countries = ['Afghanistan', 'Albania', 'Algeria', 'Andorra', 'Angola', 'Antigua & Deps',
                 'Argentina', 'Armenia', 'Australia', 'Austria', 'Azerbaijan', 'Bahamas',
                 'Bahrain', 'Bangladesh', 'Barbados', 'Belarus', 'Belgium', 'Belize', 'Benin',
                 'Bhutan', 'Bolivia', 'Bosnia Herzegovina', 'Botswana', 'Brazil', 'Brunei',
                 'Bulgaria', 'Burkina', 'Burundi', 'Cambodia', 'Cameroon', 'Canada', 'Cape Verde',
                 'Central African Rep']

    qtq_change = pd.DataFrame(columns=['country_name', 'qtq_change_inflow', 'selected_month', 'qtq_change_outflow'])
    for country in range(len(countries)):
        qtq_change_inflow = random.normalvariate(0, 1)
        qtq_change_outflow = random.normalvariate(0, 1)
        qtq_change = qtq_change.append({'country_name': countries[country].upper(),
                                        'qtq_change_inflow': qtq_change_inflow,
                                        'selected_month': month,
                                        'qtq_change_outflow': qtq_change_outflow},
                                       ignore_index=True)
    return qtq_change


def qtq_change_many_months():
    d1 = '2021-02-01'
    d2 = '2021-03-01'
    d3 = '2021-04-01'
    durations = [d1, d2, d3]
    qtq_change_by_country_name = pd.DataFrame(columns=['country_name',
                                                       'qtq_change_inflow',
                                                       'selected_month',
                                                       'qtq_change_outflow'])
    for month in durations:
        qtq_change_by_country_name = qtq_change_by_country_name.append(qtq_change_one_month(month))

    return qtq_change_by_country_name

