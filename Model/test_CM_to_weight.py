# D. import required libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import re

#
OUTPUT_FILE = "Correlation.txt"
REDIRECTION = False
DEBUG = True;

# D. change value to show visual plots and ALL data
EXTRA_DATA = False


# D. create the correlation matrix model for one year
def get_correlation_matrix(df, corr_year):
    from matplotlib import pyplot as plt
    from matplotlib import cm as cm

    # D. prints off all columns with their data
    if DEBUG:
        print(df)

    # D. create the plot
    fig = plt.figure()
    ax1 = fig.add_subplot(1,1,1)
    cmap = cm.get_cmap('jet', 30)
    cax = ax1.imshow(df.corr(), interpolation="nearest", cmap=cmap)

    arr=[];
    for i in range(df.shape[1]):
        arr.append(i)
    # D. set the number of ticks
    ax1.set_xticks(arr)
    ax1.set_yticks(arr)
    # D. create grid based on ticks
    ax1.grid(linestyle=':',)
    # D. title of model
    plt.title('{} Feature Correlation'.format(corr_year))
    # D. create labels and format for each
    labels=df.columns[0:df.shape[1]]
    ax1.set_xticklabels(labels, fontsize=6, rotation=90)
    ax1.set_yticklabels(labels, fontsize=6)
    # D. add colorbar and add ticks for values (from -1 to 1)
    fig.colorbar(cax, ticks=[-1.0, -.75, -.50, -.25, 0, .25, .50, .75, 1])
    plt.show()

# D. remove pairs of correlations to themselves
def remove_redundant_pairs(df):
    # D. diagonal and lower triangular pairs of matrix
    drop_pairs = set()
    cols = df.columns
    for i in range(0, df.shape[1]):
        for j in range(0, i + 1):
            drop_pairs.add((cols[i], cols[j]))
    return drop_pairs

# D. find and return the top correlations
def get_top_correlations(df, n):
    # D. get all correlations in absolute form
    au_corr = df.corr().abs().unstack()
    # D. call for and drop redundant pairs
    drop_labels = remove_redundant_pairs(df)
    au_corr = au_corr.drop(labels = drop_labels).sort_values(ascending = False)
    return get_win_correlations(au_corr, n)

# D. specify the target correlation attribute and return list of most correlations
def get_win_correlations(au_corr, n):
    corr_target = abs(au_corr["Act W %"])
    corr_list = []
    for i in range(n-1):
        corr_list.append(str(corr_target[i:i+1]))
    return corr_list

# D. have to do this instead of strictly removing n values off end
#    (stupid issue with corr and python)
def remove_values(list):
    pattern = '[0-9]'
    list = [re.sub(pattern, '', r) for r in list]
    return list

### MAIN CODE ############################
year = ['2005', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018']
xlsx =  pd.ExcelFile('NCAAstats.xls')

for e in range(len(year)):
    #get features 
    data = pd.read_excel(xlsx, year[e])
    for i in range(len(data['Conf'].unique())):
        data_for_BE = data.loc[data['Conf'] == (data['Conf'].unique()[i])];
        data_for_BE =  data_for_BE.drop(['Team', 'Conf', 'Rk', 'Rk.1', 'Rk.2', 'Rk.3', 'Pyth Rank', 'Opp Pyth Rank'], axis = 1)
        #just in case things wrong 
        temp_BE=[];
        temp_BE.copy()
        values = get_top_correlations(data_for_BE, 30)
        # D. remove extra information data
        # still removes to much on some title " ex:Opp % of Plays as Rus{h}
        for v in range(len(values)):
            #number need to be changed for vlaues
            values[v] = values[v][:-26]
            x = re.findall('\s',values[v][-1]);
            if x:
                values[v] = values[v][:-1]
            #TODO : fix for when coming in from mysql 
            if values[v] == 'Opp % of Plays as Rus':
                values[v] = 'Opp % of Plays as Rush';
            elif values[v] == 'Pts / G':
                values[v] = 'Pts / Gm';
            elif values[v] == 'Avg F':
                values[v] = 'Avg FP';
            elif values[v] == 'Pts / Pos':
                values[v] = 'Pts / Poss';
            elif values[v] == 'Adj':
                values[v] = 'Adj O';
            elif values[v] == 'Off % of Plays w/ T':
                values[v] = 'Off % of Plays w/ TO';
                
        #1.5.2) goes team by team (need the names)
        temp = data.loc[data['Conf'] == (data['Conf'].unique()[i])];
        if DEBUG:
            print("year[e]",year[e]);
            print("values\n",values);
            #temp = temp.loc[0:64,:]
            #print(temp);
        # how many rows its needs: 
        from Maximum_Likelihood_Estimation_Weights import*;
        features_by_weight = MLEW(temp[values],temp["Act W %"]);
        print(features_by_weight);
    

