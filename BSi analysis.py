import pandas as pd
import numpy as np


def bsi_func():

    filename = input('Please enter the file path to the CSV file of BSi data')
    db = pd.read_csv(filename)
    samples = input('Please enter the sample IDs separated by a comma. PACS-2 samples should include the term '
                    'PACS-2, blanks should include the term blank')
    weights = input('Please enter the measured weights of each sample in ug separated by a comma.'
                    ' Blanks should be entered as 0')
    samples = samples.split(',')
    db.index = samples

    weights = weights.split(',')
    for i in range(len(weights)):
        weights[i] = float(weights[i])
    db['measured_weights_ug'] = weights

#    find average value of blanks
    df_b = db.filter(like='blank', axis=0)
    avg_blanks = df_b.iloc[:, 4].mean()
    print('The average blank value is ' + str(avg_blanks) + 'uM')

# create column of blank corrected results
    db['blank_corrected_result_uM'] = db.iloc[:, 4] - avg_blanks

# convert to SiO2-Si
    db['convert_to_umol/L_and_10mL_sample'] = (db['blank_corrected_result_uM'] / 1000) * 10
    db['dilution_factor'] = db['convert_to_umol/L_and_10mL_sample'] * (5/4)

# convert to BSi
    db['BSi_ug'] = db['dilution_factor'] * 28.09
    db['BSiO2_ug'] = db['dilution_factor'] * (28.09+2*16)

# Bsi as % of mass
    db['BSi_pc'] = (db['BSi_ug'] / db['measured_weights_ug']) * 100
    db['BSiO2_pc'] = (db['BSiO2_ug']/db['measured_weights_ug']) * 100

# difference between PACS-2 average
    df_pacs = db.filter(like='PACS-2', axis=0).copy()
    avg_pacs = df_pacs.iloc[:, 11].mean()
    pacs_std = np.std(df_pacs.iloc[:, 11])
    print('The average PACS-2 value is ' + str(avg_pacs) + ' %')
    print('The standard deviation of the PACS-2 values is ' + str(pacs_std) + ' %')
    df_pacs['pc_difference_between_pacs'] = (df_pacs['BSi_pc'] - avg_pacs)/avg_pacs*100
    print(df_pacs)

# difference between duplicates
    response = input('Do you want to check the percentage difference between duplicate samples? Y/N')
    if response == 'Y' or response == 'y':
        def duplicate_func():
            dup_position1 = int(
                input('Type the position of the first duplicate in the sample order, beginning at 0 for the'
                      ' first sample'))
            dup_position2 = int(
                input('Type the position of the second duplicate in the sample order, beginning at 0 for '
                      'the first sample'))
            dup_value1 = db.iloc[dup_position1, 11]
            dup_value2 = db.iloc[dup_position2, 11]
            pc_diff = (dup_value1 - dup_value2) / ((dup_value1 + dup_value2) / 2) * 100
            print('The % difference between samples ' + str(db.index[dup_position1]) + ' and ' + str(
                db.index[dup_position2]) + ' is ' + str(pc_diff))
            question = input('Do you want to check the percentage difference between more duplicate samples? Y/N')
            if question == 'y' or question == 'Y':
                duplicate_func()
        duplicate_func()

    with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
        print(db)


bsi_func()
