import os
import pandas as pd
import glob
import matplotlib.pyplot as plt
import numpy as np
from pandas.core.reshape import reshape
import datetime

"""
Script that 
- loads existing .csv (containing solar power plant parameters of the last 30 days, 1 value each day) into dataframes
- merges dataframes in order to
- update existing dataframe
- plot essential variables from updated dataframe
"""



##################################

# collect .csv's of each module (mppt1, mppt2) and merge into one dataframe + save updated csv

#################################

path = os.path.abspath(os.path.dirname(__file__))
# set as working directory
os.chdir(path)
# change into folder cotaining data e.g. csv files
os.chdir(os.path.abspath("../../../solaranlage/solar_history"))

# get csv strings, differ between the two modules
modules = ["mppt-1","mppt-2"]

for module in modules:
    mp1 = glob.glob(str("*"+module+"-SolarHistory.csv"))
    df_from_each_file = []
    for f in mp1:
        df_temp = pd.read_csv(f, sep=',')
        df_from_each_file.append(df_temp)
    df_merged = pd.concat(df_from_each_file, ignore_index=True)
    #drop duplicates
    df_merged["Date"] = pd.to_datetime(df_merged["Date"])
    df_merged = df_merged.set_index("Date")
    df_merged = df_merged.sort_index()
    df_merged = df_merged[~df_merged.index.duplicated()]


    # save dataframe to csv
    # overwrite older one
    df_merged.to_csv(str("merged_history_"+module+".csv"))
    



##################################

# plot data
# in order to compare both modules, load created csv's into dataframes

# ['Days ago', 'Yield(Wh)', 'Max. PV power(W)', 'Max. PV voltage(V)',
    #    'Min. battery voltage(V)', 'Max. battery voltage(V)', 'Time in bulk(m)',
    #    'Time in absorption(m)', 'Time in float(m)', 'Last error',
    #    '2nd last error', '3rd last error', '4th last error']
#################################


# load dfs
mppt1 = pd.read_csv("merged_history_mppt-1.csv",index_col=0)
mppt2 = pd.read_csv("merged_history_mppt-2.csv",index_col=0)

mppt1.index = pd.to_datetime(mppt1.index)
mppt2.index = pd.to_datetime(mppt2.index)

framelist = [mppt1, mppt2]
framevar = ["mppt1","mppt2"]





# define new dataframes
# combine mppt1 & mppt2 for Yield PV
# combine mppt1 & mppt2 for max. PV Power
# combine mppt1 & mppt2 for min. battery voltage
# combine float, bulk, absorption for mppt1 & mppt2 each

# weather data
# align y axis ranges over year

yield_df = pd.concat([mppt1["Yield(Wh)"], mppt2["Yield(Wh)"]], axis=1)
pv_power_df = pd.concat([mppt1["Max. PV power(W)"], mppt2["Max. PV power(W)"]], axis=1)
min_bat_v_df = pd.concat([mppt1['Min. battery voltage(V)'], mppt2['Min. battery voltage(V)']], axis=1)
bat_condition_mppt1_df = pd.concat([mppt1['Time in bulk(m)'],mppt1['Time in absorption(m)'],mppt1['Time in float(m)']], axis=1)
bat_condition_mppt2_df = pd.concat([mppt2['Time in bulk(m)'],mppt2['Time in absorption(m)'],mppt2['Time in float(m)']], axis=1)

dfs = [yield_df,pv_power_df,min_bat_v_df,bat_condition_mppt1_df,bat_condition_mppt2_df]
for df in dfs:
    df['year_month'] = df.index.to_period('M')

year_month = pd.unique(mppt1.index.to_period('M'))
#year_month = [str(yymm) for yymm in year_month]
# months conversion, choose for monthly plotting
#month_list = pd.unique(mppt1.index.month) # get months of mppt1
#month_strings = [str(month_int) for month_int in month_list]
#datetime_object = [datetime.datetime.strptime(m, "%m") for m in month_strings]
#month_names = [do.strftime("%B") for do in datetime_object]




for ym in year_month:
    print(ym)

    fig, ax = plt.subplots(nrows=5,ncols=1,figsize=(20,12),sharex=True)
    yield_df[yield_df.year_month == ym].plot.bar(rot=0,ax=ax[0])
    pv_power_df[pv_power_df.year_month == ym].plot.bar(rot=0,ax=ax[1])
    min_bat_v_df[min_bat_v_df.year_month == ym].plot.bar(rot=0,ax=ax[2])
    bat_condition_mppt1_df[bat_condition_mppt1_df.year_month == ym].plot.bar(stacked=True,rot=0,ax=ax[3])
    bat_condition_mppt2_df[bat_condition_mppt2_df.year_month == ym].plot.bar(stacked=True,rot=0,ax=ax[4])
    #ax[4].set_xticklabels(yield_df[yield_df.index.month == mint].index.date)    

    ax[4].set_xticklabels(labels=yield_df[yield_df.year_month == ym].index.date, rotation=70, rotation_mode="anchor", ha="right")

    ax[0].legend(['Yield(Wh) mppt1', 'Yield(Wh) mppt2'])
    ax[0].set_ylim([yield_df.min().min(), yield_df.max().max()])
    ax[1].legend(['Max. PV power(W) mppt1', 'Max. PV power(W) mppt2'])
    ax[1].set_ylim([pv_power_df.min().min(), pv_power_df.max().max()])
    ax[2].legend(['Min. battery voltage(V) mppt1', 'Min. battery voltage(V) mppt2'])
    ax[2].set_ylim([min_bat_v_df.min().min(), min_bat_v_df.max().max()])
    ax[3].legend(['laden','Nutzung','voll geladen'], title = 'mppt1, in Minuten')
    ax[4].legend(['laden','Nutzung','voll geladen'], title = 'mppt2, in Minuten')
    #fig.suptitle(str("Overview for "+ym))
    #plt.savefig(str('../plots/overview_'+ym+'.jpg'))


