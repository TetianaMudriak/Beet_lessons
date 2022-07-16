""" This is docstring for this script"""
import csv
from pprint import pprint


import matplotlib.pyplot as plt


def count_row(data):
    row_count = len(data)
    print('У файлі', row_count, 'рядків.')


def get_period(years):
    start_year = min(years)
    last_year = max(years)
    research_period = int(last_year[:4]) - int(start_year[:4])
    print('Спостереження ведеться', research_period, 'років.')


def get_industries_amount(industries):
    unique_fields = len(industries)
    print(unique_fields, 'галузі еокономіки були під спостереженням.', )


def get_gdp_amount(data, industries):
    industry_amounts = dict.fromkeys(industries, 0.0)

    for row in data:
        for key, value in industry_amounts.items():
            if row['Description'] == key:
                industry_amounts[key] = round(value + float(row['Amount']), 2)
    return industry_amounts


def get_lead_industry(data, industries):
    ind = get_gdp_amount(data, industries)
    lead_industry = max(ind, key=ind.get)
    return lead_industry


def lead_industry_amount(data, industries):
    ind = get_gdp_amount(data, industries)
    lead_ind = get_lead_industry(data, industries)
    lead_gdp_amount = ind[lead_ind]
    return lead_gdp_amount


def lead_industry_share(data, industries):
    sum_ind = get_gdp_amount(data, industries)
    lead_gdp = lead_industry_amount(data, industries)
    total_gdp = sum(sum_ind.values())
    lead_field_share = round((lead_gdp / total_gdp * 100), 2)
    print('Дана галузь становить', lead_field_share,
          '% усієї економіки за період спостереження.')


def first_year_amounts(data, industries, years):
    first_year = min(years)
    first_year_amount = dict.fromkeys(industries, 0.0)

    for row in data:
        for key, value in first_year_amount.items():
            if row['Quarter'] == first_year:
                if row['Description'] == key:
                    first_year_amount[key] = float(row['Amount'])

    return first_year_amount


def last_year_amounts(data, industries, years):
    last_year = max(years)
    last_year_amount = dict.fromkeys(industries, 0.0)

    for row in data:
        for key, value in last_year_amount.items():
            if row['Quarter'] == last_year:
                if row['Description'] == key:
                    last_year_amount[key] = float(row['Amount'])

    return last_year_amount


def highest_increase(data, industries, years):
    f_y = first_year_amounts(data, industries, years)
    l_y = last_year_amounts(data, industries, years)
    amount_difference = {x: l_y[x] - f_y[x] for x in l_y if x in f_y}
    h_increase_ind = max(amount_difference, key=amount_difference.get)
    print('Галузь із найбільшим зростанням за весь період - ' + h_increase_ind +
          '\nЗростання становить - ' + str(amount_difference[h_increase_ind]))


def get_plot(data, industries):
    data_range = get_gdp_amount(data, industries)
    names = list(data_range.keys())
    values = list(data_range.values())

    plt.bar(range(len(data_range)), values, tick_label=names)
    plt.show()


def main():
    with open(
            'Gross-domestic-product-March-2022-quarter'
            '-visualisation-csv.csv',
            newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        data = []
        for row in reader:
            data.append(row)

    industries = {dict1['Description'] for dict1 in data}
    years = [col['Quarter'] for col in data]

    count_row(data)
    get_period(years)
    get_industries_amount(industries)
    pprint(get_gdp_amount(data, industries), width=70)
    print('\nГалузь \"', get_lead_industry(data, industries),
          '\" отримала найбільший обсяг ВВП за весь період спостереження'
          ' у розмірі',
          round(lead_industry_amount(data, industries), 2))
    lead_industry_share(data, industries)
    highest_increase(data, industries, years)
    get_plot(data, industries)


if __name__ == '__main__':
    main()
