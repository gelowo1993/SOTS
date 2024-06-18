def func1() :
    import pandas as pd
    import matplotlib.pyplot as plt
    import numpy as np
    from scipy import stats

    filename= input('Please enter the filepath to the CSV file of PIC data')

    f = pd.read_csv(filename, header=None)  #import csv file
    f = f.dropna(axis='columns', how='all')  #drop empty columns
    f = f.fillna(0.0)  #fill empty rows
    f = f.drop(f.columns[[0, 1]], axis=1)  #drop unnecessary first 2 columns
    f.columns = ['Analysis Element','Date','Analysis Time','read1','read2','read3','read4','read5','read6','read7','read8',
            'read9','read10','read11','read12','empty1','empty2','empty3','result','unit']  #provide column headings
    index_list = input('Please enter the names of the samples in analysis order separated by a comma. Blanks should '
                       'include the term blank and CaCO3 standards should include the term CaCO3')
    index_list = index_list.split(',')
    f.index = index_list

#add Measured Weights column

    weights = input('Please enter the measured weights of all samples in ug, separated by a comma. Enter 0 for blanks and the CaCO3 standards as their measured'
                ' weight multiplied by 0.9998')
    weights = weights.split(',')
    print(weights)
    for i in range(len(weights)):
        weights[i]=float(weights[i])
    f['Measured_Weights_ug'] = weights

#filter for dataframes of just blanks and just CaCO3 standards and plot
    df_b = f.filter(like='blank', axis=0)
    df_s = f.filter(like='CaCO3', axis=0)
    x_values = [1,2,3,4,5,6,7,8,9,10,11,12]
#blanks graph
    fig, ax = plt.subplots()
    for index, row in df_b.iterrows():
        ax.plot(x_values, row[3:15], label=index)
    ax.legend(ncols=3)
    ax.set_xlabel('Reading number')
    ax.set_ylabel('ug C')
    ax.set_title('Blank Results')
    plt.show()

#CaCO3 standards graph
    fig, ax = plt.subplots()
    for index, row in df_s.iterrows():
        ax.plot(x_values, row[3:15], label=index)
    ax.legend()
    ax.set_xlabel('Reading number')
    ax.set_ylabel('ug C')
    ax.set_title('CaCO3 results')
    plt.show()

#create column of blank subtracted values
    avg_blanks = df_b.loc[:, 'result'].mean()
    f['Blank_corrected_result_ugC'] = f.apply(lambda row: row.result-avg_blanks, axis=1)
    f.iloc[2,21] = avg_blanks

    print(f['Measured_Weights_ug'].iloc[2:8])
    print(f['Blank_corrected_result_ugC'].iloc[2:8])

#calculate and plot calibration curve
    fig, ax = plt.subplots()
    ax.scatter(f['Measured_Weights_ug'].iloc[2:8], f['Blank_corrected_result_ugC'].iloc[2:8])

#add trend line
    coef = np.polyfit(f['Measured_Weights_ug'].iloc[2:8], f['Blank_corrected_result_ugC'].iloc[2:8], 1)
    y = np.poly1d(coef)
    slope, intercept, r_value, p_value, std_err = stats.linregress(f['Measured_Weights_ug'].iloc[2:8],
                                                              f['Blank_corrected_result_ugC'].iloc[2:8])
    plt.plot(f['Measured_Weights_ug'].iloc[2:8], y(f['Measured_Weights_ug'].iloc[2:8]))
    plt.annotate('R2 = ' + str(r_value), xy=(2000, 100), xytext=(2000, 100))
    plt.annotate('y = ' + str(y), xy=(2000, 65), xytext=(2000, 65))
    ax.set_title('CaCO3 Calibration curve')
    ax.set_xlabel('Mass (ug)')
    ax.set_ylabel('ug C')
    plt.show()

#calculation of ug Carbon from standard curve and percentage of weight
    f['Result_from_calcurve_ug_CaCO3'] = (f.Blank_corrected_result_ugC-intercept)/slope
    f['calcurve_%CaCO3'] = (f.Result_from_calcurve_ug_CaCO3/f.Measured_Weights_ug)*100

#calculation of ug carbon from raw figures and percentage of weight
    f['Raw_data_estimate_ug_CaCO3'] = f.apply(lambda row: row.Blank_corrected_result_ugC*100.09/12.01, axis=1)
    f['raw_data_%CaCO3'] = f.Raw_data_estimate_ug_CaCO3 / f.Measured_Weights_ug * 100

    with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
        print(f)

func1()