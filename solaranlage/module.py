"""
Script that 
- loads existing .csv (containing solar power plant parameters of the last 30 days, 1 value each day) into dataframes
- merges dataframes in order to
- update existing dataframe
- plot essential variables from updated dataframe
"""

import numpy as np
import os
import sys
import pandas as pd
import glob
import matplotlib.pyplot as plt

path = os.path.abspath(os.path.dirname(__file__))
# zset as working directory
os.chdir(path)
# change into data folder -> data/.csv
os.chdir(os.path.abspath("../../solaranlage/solar_history"))

# two loops, one for each mppt module
modules = ["mppt-1","mppt-2"]
mp1 = glob.glob(str("*"+modules[0]+"*"))
mp2 = glob.glob(str("*"+modules[1]+"*"))

df_from_each_file = []
for f in mp1:
    df_temp = pd.read_csv(f, sep=',')
    df_temp["Date"] = pd.to_datetime(df_temp["Date"])
    df_temp = df_temp.set_index("Date")
    df_from_each_file.append(df_temp)
df_merged = pd.concat(df_from_each_file, ignore_index=True)
#drop duplicates

plt.plot(df_merged["Date"], df_merged["Yield(Wh)"])

mx = os.listdir(os.getcwd()) # filter by string, e.g. mppt-1, and storage date



raw = pd.DataFrame 


os.getcwd()

path2csv = 
csv_dir = os.chdir("..")
print(csv_dir)
#solaranlage\solar_history

