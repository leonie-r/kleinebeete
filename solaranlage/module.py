import os
import pandas as pd
import glob
import matplotlib.pyplot as plt
import numpy as np
from pandas.core.reshape import reshape

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

for i in modules:
    mp1 = glob.glob(str("*"+i+"-SolarHistory.csv"))
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
    first_date = df_merged.index[0].strftime('%Y%m%d')
    last_date = df_merged.index[-1].strftime('%Y%m%d')
    df_merged.to_csv(str(first_date)+"_"+str(last_date)+"_"+str(i)+".csv")
    



##################################

# plot data
# in order to compare both modules, load created csv's into dataframes

# ['Days ago', 'Yield(Wh)', 'Max. PV power(W)', 'Max. PV voltage(V)',
    #    'Min. battery voltage(V)', 'Max. battery voltage(V)', 'Time in bulk(m)',
    #    'Time in absorption(m)', 'Time in float(m)', 'Last error',
    #    '2nd last error', '3rd last error', '4th last error']
#################################



mppt1 = pd.read_csv(str(first_date)+"_"+str(last_date)+"_mppt-1.csv",index_col=0)
mppt2 = pd.read_csv(str(first_date)+"_"+str(last_date)+"_mppt-2.csv",index_col=0)

mppt1.index = pd.to_datetime(mppt1.index)
mppt2.index = pd.to_datetime(mppt2.index)

framelist = [mppt1, mppt2]
framevar = ["mppt1","mppt2"]

from matplotlib.dates import MO, WeekdayLocator, DateFormatter, AutoDateLocator, AutoDateFormatter, ConciseDateFormatter
import matplotlib.dates as mdates
# tick on mondays every week
locator = WeekdayLocator(byweekday=MO)
# display day of week (here:Monday), date of month and month on major ticks
date_form = DateFormatter("%a\n%d\n%b")


# 'Yield(Wh)', 'Max. PV power(W)', 'Max. PV voltage(V)' as bar plot
"""
fig, axs = plt.subplots(nrows=3,ncols=1,sharex=True)
x = np.arange(len(mppt1.index)) # for bar positions
width = 0.35 # for bar extension
for ax,cols in zip(axs.reshape(-1),mppt1.columns[1:4]):
    ax.bar(x - width/2,mppt1[cols],0.35,label=str(cols+" from mppt1"))
    ax.bar(x + width/2,mppt2[cols],0.35,label=str(cols+" from mppt2"))
    ax.legend()
    ax.set_xticks(x)
    #ax.set_xticklabels(mppt1[cols].index.date)
    ax.set_xticklabels(mppt1.index)
    ax.xaxis.set_major_locator(locator)
    ax.xaxis.set_minor_locator(mdates.DayLocator(interval=1))
    ax.xaxis.set_major_formatter(date_form)
savefig = os.path.join("../plots/",str(last_date)+"_"+str(first_date)+"_yield_power_voltage.png")
plt.tight_layout()
plt.savefig(savefig)
plt.close()
"""

# 3er plot
# Yield, Max PV power (W), Max PV voltage (V)

fig, axs = plt.subplots(nrows=3,ncols=1)
x = np.arange(len(mppt1.index)) # for bar positions
width = 0.35 # for bar extension
for ax,cols in zip(axs.reshape(-2),mppt1.columns[1:3]):
    ax.bar(x - width/2,mppt1[cols],0.35,label=str(cols+" from mppt1"))
    ax.bar(x + width/2,mppt2[cols],0.35,label=str(cols+" from mppt2"))
    ax.legend()
    ax.set_xticks(x)
    ax.set_xticklabels([])
    #ax.set_xticklabels(mppt1[cols].index.date)
axs[2].plot(mppt1.index, mppt1['Max. PV voltage(V)'],label='Max. PV voltage(V) from mppt1')
axs[2].plot(mppt1.index, mppt2['Max. PV voltage(V)'],label='Max. PV voltage(V) from mppt2')    
axs[2].legend()
axs[2].set_xticklabels(mppt1.index)
axs[2].xaxis.set_major_locator(locator)
axs[2].xaxis.set_minor_locator(mdates.DayLocator(interval=1))
axs[2].xaxis.set_major_formatter(date_form)
savefig = os.path.join("../plots/",str(last_date)+"_"+str(first_date)+"_yield_power_voltage.png")
plt.tight_layout()
plt.savefig(savefig)
plt.close()






# battery bulk/absorption/float stack bar plot

stack_bar_var = ['Time in bulk(m)','Time in absorption(m)', 'Time in float(m)']
width = 0.65
for frame, var in zip(framelist,framevar):
    fig, ax = plt.subplots()
    ax.bar(frame.index.date, frame[stack_bar_var[0]], width, label=stack_bar_var[0]+" = laden") #edgecolor = 'black'
    ax.bar(frame.index.date, frame[stack_bar_var[1]], width, bottom=frame[stack_bar_var[0]], label=stack_bar_var[1])
    ax.bar(frame.index.date, frame[stack_bar_var[2]], width, bottom=frame[stack_bar_var[0]]+frame[stack_bar_var[1]], label=stack_bar_var[2]+" = voll geladen")
    ax.legend()
    ax.set_ylabel('time in minutes')
    ax.xaxis.set_major_locator(locator)
    ax.xaxis.set_minor_locator(mdates.DayLocator(interval=1))
    ax.xaxis.set_major_formatter(date_form)
    fig.suptitle("Parameters for module "+var)
    savefig = os.path.join("../plots/",str(last_date)+"_"+str(first_date)+"_bulk-float-absorption_"+var+".png")
    plt.tight_layout()
    plt.savefig(savefig)
plt.close()



# min/max battery voltage
# to show that min max voltage of both modules are pretty close
stylelist = ["solid","dashed"]
line_var = ['Min. battery voltage(V)', 'Max. battery voltage(V)']
for frame, var, style in zip(framelist,framevar,stylelist):
    plt.plot(frame.index,frame[line_var[1]],label=line_var[1]+" "+var,linestyle=style)
    plt.plot(frame.index,frame[line_var[0]],label=line_var[0]+" "+var,linestyle=style)
plt.legend()
plt.xticks(rotation=45)
plt.title("Min-Max Battery Voltage - mppt1 & mppt2")
savefig = os.path.join("../plots/",str(last_date)+"_"+str(first_date)+"_min-max-voltage_beide-module-im-vergleich.png")
plt.tight_layout()
plt.savefig(savefig)
plt.close()



# Max. PV Voltage
# Max. PV power
line_var2 = ['Max. PV voltage(V)', 'Max. PV power(W)']
save_var = ['max-PV-voltage', 'max-PV-power']
for i in range(len(line_var2)):
    for frame, var in zip(framelist,framevar):
        plt.plot(frame.index,frame[line_var2[i]],label=line_var2[i]+" "+var)
        print(str(line_var2[i]))
        plt.legend()
        plt.title(str(line_var2[i]))
        plt.xticks(rotation=45)
    plt.tight_layout()
    savefig = os.path.join("../plots/",str(last_date)+"_"+str(first_date)+"_"+str(save_var[i])+".png")
    plt.savefig(savefig)
    plt.show()
    plt.close()
    print("saved")
    print(savefig)
plt.close()



################

# COMPARE climate data and solar history

################

# additional climate data: 
# Leipzig Holzhausen 02928
os.chdir("../holzhausen_klima_dwd")
import glob
data = pd.read_csv((glob.glob("produkt*")[0]), sep=";") # file is named 'produkt_klima_tag_20191221_20210622_02928.txt'

# Leipzig/Halle 02932
os.chdir("../halleleipzig_klima_dwd")
data2 = pd.read_csv((glob.glob("produkt*")[0]), sep=";")

data["date"] = pd.to_datetime(data["MESS_DATUM"], format="%Y%m%d")
data2["date"] = pd.to_datetime(data2["MESS_DATUM"], format="%Y%m%d")
# select climate data of sloar history period
#xlim = (pd.to_datetime("2021-04-23"),pd.to_datetime("2021-05-25"))
#missing_dates = pd.date_range(start=data["date"].max(),end=frame.index.max())
# concat series dates
#try1 = pd.concat([data["date"],missing_dates],axis=0) #series, obj.. Fehler

from datetime import timedelta
datelim = (frame.index[0],frame.index[-1]) # sollte bestenfalls 1 Tag vorher und 1 Tag später sein
data_cut = data[(data["date"] > datelim[0]) & (data["date"] < datelim[1])]
data2_cut = data2[(data2["date"] > datelim[0]) & (data2["date"] < datelim[1])]
xlim = (datelim[0]+ timedelta(days = -1),datelim[1]+ timedelta(days = 1))
delta = np.arange((abs((xlim[0] - xlim[1]).days)))

fig, ax = plt.subplots(nrows=4,ncols=1,figsize=(12,7))#,sharex=True)
ax[0].plot(data_cut["date"],data_cut['  NM'],label = "Tagesmittel des Bedeckungsgrades [Achtel]; Holzhausen")
ax[0].plot(data2_cut["date"],data2_cut["  NM"],label = "Tagesmittel des Bedeckungsgrades [Achtel]; Leipzig/Halle")
ax[0].plot(data2_cut["date"],data2_cut[" SDK"],label = "Sonnenscheindauer Tagessumme [Stunden]; Leipzig/Halle")

#x = np.arange(len(mppt1.index))
#ax[1] = mppt1.plot(x=mppt1.index, y='Yield(Wh)', kind="bar")
###

# Hier klappt was nicht!!
# x achse soll 1 Tag vor Zqehlung beginnen und 1 Tag weitergehen, damit nicht der Balken an der y achse klebt
# aber: kommt dann nicht mehr hin mit den geteilten bars die den tick mittig haben sollen
# 
# ###
 
ax[1].bar(delta[1:-1] - width/2,mppt1['Yield(Wh)'],0.35,label=str("Yield(Wh) from mppt1"))
ax[1].bar(x + width/2,mppt2['Yield(Wh)'],0.35,label=str("Yield(Wh) from mppt2"))
ax[1].set_xticks(x)

for frame, var, position in zip(framelist,framevar,range(2,4)):
    ax[position].bar(frame.index.date, frame[stack_bar_var[0]], width, label=stack_bar_var[0]+" = laden") #edgecolor = 'black'
    ax[position].bar(frame.index.date, frame[stack_bar_var[1]], width, bottom=frame[stack_bar_var[0]], label=stack_bar_var[1])
    ax[position].bar(frame.index.date, frame[stack_bar_var[2]], width, bottom=frame[stack_bar_var[0]]+frame[stack_bar_var[1]], label=stack_bar_var[2]+" = voll geladen")
    ax[position].title.set_text("parameter from "+str(var))
    ax[position].set_ylabel('time in minutes')

for i in range(4):
    ax[i].legend()
    ax[i].xaxis.set_major_locator(locator)
    ax[i].xaxis.set_minor_locator(mdates.DayLocator(interval=1))
    ax[i].xaxis.set_major_formatter(date_form)
    ax[i].set_xlim(xlim)

#
plt.tight_layout()
plt.savefig("../plots/klimadaten_nm_sdk_"+str(xlim[0].date())+"_"+str(xlim[1].date())+".png")



variables = [
   # 'QN_3', 
    '  NM',
    ' RSK',
    ' SDK', 
    ' TMK',
    ' TNK',
    ' TXK', 
    ' UPM',
    ' VPM',
    '  FX', 
    '  FM', 
       #'RSKF', 
    #'  PM',    
    #' TGK', 
    ##'SHK_TAG',
    ## 'QN_4', 
   ## 'eor'
        ]

# NM;Tagesmittel des Bedeckungsgrades;Achtel;Klimadaten aus der Klimaroutine nach 1.4.2001, generiert aus SYNOP-Meldungen (3 Termine 06, 12, 18 UTC und Tageswerte aus st�ndlichen Werten oder Beobachtungen an Hauptterminen);arithm.Mittel aus mind. 21 Stundenwerten;;;eor;
# RSK;tgl. Niederschlagshoehe;mm;Klimadaten aus der Klimaroutine nach 1.4.2001, generiert aus SYNOP-Meldungen (3 Termine 06, 12, 18 UTC und Tageswerte aus st�ndlichen Werten oder Beobachtungen an Hauptterminen);06:00 - 06:00 FT. UTC;;;eor;
# SDK;Sonnenscheindauer Tagessumme;Stunde;Klimadaten aus der Klimaroutine nach 1.4.2001, generiert aus SYNOP-Meldungen (3 Termine 06, 12, 18 UTC und Tageswerte aus st�ndlichen Werten oder Beobachtungen an Hauptterminen);00:00 - 24:00 UTC;;;eor;
# TMK;Tagesmittel der Temperatur;�C;Klimadaten aus der Klimaroutine nach 1.4.2001, generiert aus SYNOP-Meldungen (3 Termine 06, 12, 18 UTC und Tageswerte aus st�ndlichen Werten oder Beobachtungen an Hauptterminen);arithm.Mittel aus mind. 21 Stundenwerten;;;eor;
# TNK;Tagesminimum der Lufttemperatur in 2m Hoehe;�C;Klimadaten aus der Klimaroutine nach 1.4.2001, generiert aus SYNOP-Meldungen (3 Termine 06, 12, 18 UTC und Tageswerte aus st�ndlichen Werten oder Beobachtungen an Hauptterminen);00:00 - 24:00 UTC gemessen;;;eor;
# TXK;Tagesmaximum der Lufttemperatur in 2m H�he;�C;Klimadaten aus der Klimaroutine nach 1.4.2001, generiert aus SYNOP-Meldungen (3 Termine 06, 12, 18 UTC und Tageswerte aus st�ndlichen Werten oder Beobachtungen an Hauptterminen);00:00 - 24:00 UTC gemessen;;;eor;
# UPM;Tagesmittel der Relativen Feuchte;%;Klimadaten aus der Klimaroutine nach 1.4.2001, generiert aus SYNOP-Meldungen (3 Termine 06, 12, 18 UTC und Tageswerte aus st�ndlichen Werten oder Beobachtungen an Hauptterminen);arithm.Mittel aus mind. 21 Stundenwerten;;;eor;
# VPM;Tagesmittel des Dampfdruckes;hpa;Klimadaten aus der Klimaroutine nach 1.4.2001, generiert aus SYNOP-Meldungen (3 Termine 06, 12, 18 UTC und Tageswerte aus st�ndlichen Werten oder Beobachtungen an Hauptterminen);arithm.Mittel aus mind. 21 Stundenwerten;;;eor;

# FM;Tagesmittel der Windgeschwindigkeit m/s  Messnetz 3;m/sec;Winddaten (Stundenmittel, maximale Windspitze 23:51-23:50 UTC) generiert aus 10-Minutenmittel von automatischen Stationen der 2. Generation (AMDA), Richtungsangaben in 36-teiliger Windrose;arithm.Mittel aus mind. 21 Stundenwerten;;;eor;
# FX;Maximum der Windspitze Messnetz 3;m/sec;Winddaten (Stundenmittel, maximale Windspitze 23:51-23:50 UTC) generiert aus 10-Minutenmittel von automatischen Stationen der 2. Generation (AMDA), Richtungsangaben in 36-teiliger Windrose;23:51 - 23:50 UTC;;;eor;
# PM;Tagesmittel des Luftdrucks;hpa;Klimadaten aus der Klimaroutine nach 1.4.2001, generiert aus SYNOP-Meldungen (3 Termine 06, 12, 18 UTC und Tageswerte aus st�ndlichen Werten oder Beobachtungen an Hauptterminen);arithm.Mittel aus mind. 21 Stundenwerten;;;eor;
# RSKF;tgl. Niederschlagsform (=Niederschlagshoehe_ind);numerischer Code;Klimadaten aus der Klimaroutine nach 1.4.2001, generiert aus SYNOP-Meldungen (3 Termine 06, 12, 18 UTC und Tageswerte aus st�ndlichen Werten oder Beobachtungen an Hauptterminen);06:00 - 06:00 FT. UTC;;;eor;
# SHK_TAG;Schneehoehe Tageswert;cm;Klimadaten aus der Klimaroutine nach 1.4.2001, generiert aus SYNOP-Meldungen (3 Termine 06, 12, 18 UTC und Tageswerte aus st�ndlichen Werten oder Beobachtungen an Hauptterminen);06 UTC;;;eor;
# TGK;Minimum der Lufttemperatur am Erdboden in 5cm Hoehe;�C;Klimadaten aus der Klimaroutine nach 1.4.2001, generiert aus SYNOP-Meldungen (3 Termine 06, 12, 18 UTC und Tageswerte aus st�ndlichen Werten oder Beobachtungen an Hauptterminen);00:00 - 24:00 UTC gemessen;;;eor;
dates = data["date"][(data["date"] > xlim[0]) & (data["date"] < xlim[1])]
fig, axes = plt.subplots(nrows=len(variables)+1, ncols=1, figsize=(25,15))#, sharex=True)
for i, variable in enumerate(variables):
    values = data[variable][(data["date"] > xlim[0]) & (data["date"] < xlim[1])]
    axes[i].plot(dates, values, label=variable)
    axes[i].legend()
axes[i+1].bar(frame.index.date, frame[stack_bar_var[0]], width, label=stack_bar_var[0]+" = laden") #edgecolor = 'black'
axes[i+1].bar(frame.index.date, frame[stack_bar_var[1]], width, bottom=frame[stack_bar_var[0]], label=stack_bar_var[1])
axes[i+1].bar(frame.index.date, frame[stack_bar_var[2]], width, bottom=frame[stack_bar_var[0]]+frame[stack_bar_var[1]], label=stack_bar_var[2]+" = voll geladen")
axes[i+1].legend()
axes[i+1].set_ylabel('time in minutes')
axes[i+1].xaxis.set_major_locator(locator)
axes[i+1].xaxis.set_minor_locator(mdates.DayLocator(interval=1))
axes[i+1].xaxis.set_major_formatter(date_form)


plt.tight_layout()

plt.savefig("../plots/compare_climate_variables_"+str(xlim[0].date())+"_"+str(xlim[1].date())+".png")



# """
# climate = pd.read_csv("produkt_klima_tag_20191120_20210522_02932.txt", sep=";")
# climate["MESS_DATUM"] = pd.to_datetime(climate["MESS_DATUM"],format="%Y%m%d")
# climate = climate.set_index("MESS_DATUM")
# climate = climate[(climate.index > first_date) & (climate.index < last_date)]
# # NM;Tagesmittel des Bedeckungsgrades;Achtel;Klimadaten aus der Klimaroutine nach 1.4.2001, generiert aus SYNOP-Meldungen (3 Termine 06, 12, 18 UTC und Tageswerte aus st�ndlichen Werten oder Beobachtungen an Hauptterminen);arithm.Mittel aus mind. 21 Stundenwerten;;;eor;
# cloudcover = climate["NM"]
# # SDK;Sonnenscheindauer Tagessumme;Stunde;Klimadaten aus der Klimaroutine nach 1.4.2001, generiert aus SYNOP-Meldungen (3 Termine 06, 12, 18 UTC und Tageswerte aus st�ndlichen Werten oder Beobachtungen an Hauptterminen);00:00 - 24:00 UTC;;;eor;
# sunshine = climate["SDK"]

# sunshine.plot.bar()
# """
# """
# fig, ax = plt.subplots()
# ax[0,0].bar(climate.index, climate["NM"])
# ax[1,0].bar(climate.index, climate["SDK"])
# plt.plot(mppt1.index, mppt1["Yield(Wh)"])
# #os.getcwd()
# """

# #locator = AutoDateLocator()
# #formatter = ConciseDateFormatter(locator) #exchangeabgle with AutoDateFormatter
# #formatter = AutoDateFormatter(locator)
