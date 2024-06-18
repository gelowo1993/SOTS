import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import statistics


def chn_analysis():
#   read in data file
    filename = input('Please provide the file path to the CSV file of CHN data')
    chn_db = pd.read_csv(filename)
# tidy csv file
    chn_db = chn_db.drop([75, 76, 77])
    samples = input('Please provide the sample IDs separated by a comma. PAC-2 samples should contain the phrase '
                    'PACS-2, standards should contain the phrase std and acetanilide samples should contain the phrase '
                    'acetanilide')
    samples = samples.split(',')
    chn_db.index = samples

# acetanilide % distance from the mean for N and C
    a_db = chn_db.filter(like='acetanilide', axis=0).copy()
    n_avg_a = a_db.iloc[:, 3].mean()
    c_avg_a = a_db.iloc[:, 4].mean()
    print('The average %N acetanilide value is ' + str(n_avg_a))
    print('The average %C acetanilide value is ' + str(c_avg_a))
    a_db['%N_difference_from_mean'] = (a_db['N%']-n_avg_a)/n_avg_a*100
    a_db['%C_difference_from_mean'] = (a_db['C%']-c_avg_a)/c_avg_a*100
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
        print(a_db)
# acetanilide plot
    fig, ax = plt.subplots()
    ax.scatter(a_db['N%'], a_db['C%'])
    ax.set_xlabel('N%')
    ax.set_ylabel('C%')
    ax.set_title('Acetanilide results')
    plt.show()
# PACS-2 % distance from the mean for N and C
    pacs_db = chn_db.filter(like='PACS-2', axis=0).copy()
    n_avg_pacs = pacs_db.iloc[:, 3].mean()
    c_avg_pacs = pacs_db.iloc[:, 4].mean()
    print('The average %N PACS-2 value is ' + str(n_avg_pacs))
    print('The average %C PACS-2 value is ' + str(c_avg_pacs))
    pacs_db['%N_difference_from_mean'] = (pacs_db['N%']-n_avg_pacs)/n_avg_pacs*100
    pacs_db['%C_difference_from_mean'] = (pacs_db['C%']-c_avg_pacs)/c_avg_pacs*100
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
        print(pacs_db)
# calculate C/N
    chn_db['C/N'] = chn_db.iloc[:, 4] / chn_db.iloc[:, 3]

# plot C/N
    graph_1000 = chn_db.loc[chn_db.index.str.contains('1000', case=False)].copy()
    graph_2000 = chn_db.loc[chn_db.index.str.contains('2000', case=False)].copy()
    graph_3800 = chn_db.loc[chn_db.index.str.contains('3800', case=False)].copy()
    graph_pacs = chn_db.loc[chn_db.index.str.contains('pacs', case=False)].copy()

    fig, ax = plt.subplots()
    ax.scatter(graph_1000['N%'], graph_1000['C%'], color='r', label='1000m')
    ax.scatter(graph_2000['N%'], graph_2000['C%'], color='b', label='2000m')
    ax.scatter(graph_3800['N%'], graph_3800['C%'], color='m', label='3800m')
    ax.scatter(graph_pacs['N%'], graph_pacs['C%'], color='g', label='PACS-2')
# plot trendlines
    coef_1000 = np.polyfit(graph_1000['N%'], graph_1000['C%'], 1)
    y_1000 = np.poly1d(coef_1000)
    ax.plot(graph_1000['N%'], y_1000(graph_1000['N%']), color='r', linestyle=':')
    ax.annotate('1000m y = ' + str(y_1000), xy=(2.5, 10), xytext=(2.5, 10))

    coef_2000 = np.polyfit(graph_2000['N%'], graph_2000['C%'], 1)
    y_2000 = np.poly1d(coef_2000)
    ax.plot(graph_2000['N%'], y_2000(graph_2000['N%']), color='b', linestyle=':')
    ax.annotate('2000m y = ' + str(y_2000), xy=(2.5, 8), xytext=(2.5, 7))

    coef_3800 = np.polyfit(graph_3800['N%'], graph_3800['C%'], 1)
    y_3800 = np.poly1d(coef_3800)
    ax.plot(graph_3800['N%'], y_3800(graph_3800['N%']), color='m', linestyle=':')
    ax.annotate('3800m y = ' + str(y_3800), xy=(2.5, 6), xytext=(2.5, 4))

    ax.legend()
    ax.set_xlabel('N%')
    ax.set_ylabel('C%')
    ax.set_title('C/N')
    plt.show()

    with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
        print(chn_db)

# check duplicates
    response = input('Do you want to check the percentage difference between duplicate samples? Y/N')
    if response == 'Y' or response == 'y':
        def duplicate_func():
            dup_position1 = int(
                input('Type the position of the first duplicate in the sample order, beginning at 0 for the first '
                      'sample'))

            dup_position2 = int(
                input('Type the position of the second duplicate in the sample order, beginning at 0 for the first '
                      'sample'))
# %N difference
            dup_value1_n = chn_db.iloc[dup_position1, 3]
            dup_value2_n = chn_db.iloc[dup_position2, 3]
            pc_diff_n = ((dup_value1_n - dup_value2_n) / statistics.mean([dup_value1_n, dup_value2_n])) * 100
            print('The N% difference between samples ' + str(chn_db.index[dup_position1]) + ' and ' + str(
                    chn_db.index[dup_position2]) + ' is ' + str(pc_diff_n))
# %C difference
            dup_value1_c = chn_db.iloc[dup_position1, 4]
            dup_value2_c = chn_db.iloc[dup_position2, 4]
            pc_diff_c = ((dup_value1_c - dup_value2_c) / statistics.mean([dup_value1_c, dup_value2_c])) * 100
            print('The C% difference between samples ' + str(chn_db.index[dup_position1]) + ' and ' + str(
                chn_db.index[dup_position2]) + ' is ' + str(pc_diff_c))
            question = input('Do you want to check the percentage difference between more duplicate samples? Y/N')
            if question == 'y' or question == 'Y':
                duplicate_func()

        duplicate_func()


chn_analysis()
