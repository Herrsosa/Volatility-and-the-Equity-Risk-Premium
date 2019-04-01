# -*- coding: utf-8 -*-
"""
Created on Mon Nov 12 11:23:30 2018

@author: nilsh
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import datetime


def EquityPremium(T2_T1,T2_t,T1_t,SVIXT1,SVIXT2,First_Month): # Returns spot or forward equity risk premium
    if First_Month == True: 
        return (1/(T1_t))*np.log(1+SVIXT1*(T1_t))
    else:
        return (1/(T2_T1))*np.log((1+SVIXT2*(T2_t))/(1+SVIXT1*(T1_t)))

def f7(seq): # Function to format a set
    seen = set()
    seen_add = seen.add
    return[x for x in seq if not(x in seen or seen_add(x))]

# Reads in the data
path = os.getcwd() + "\Data\SVIX.xlsx"
data = pd.read_excel(path,sheet_name="Sheet1")
dates = f7(data["Date"])
Term_Structure = pd.DataFrame(columns=["Date", "W EP0_1", "W EP1_2", "W EP2_3", "W EP3_6", "W EP6_12"])

# Constructs the term structure of the equity risk premia for the time series
for i in range(len(dates)):
    df = data[data["Date"].isin([dates[i]])]
    Term_Structure.loc[i] = ""
    Term_Structure.iloc[i][0] = dates[i]
    SVIX1,SVIX2,SVIX3,SVIX6,SVIX12 = df["1mo"].iloc[0],df["2mo"].iloc[0],df["3mo"].iloc[0],df["6mo"].iloc[0],df["12mo"].iloc[0]
    EP0_1 = EquityPremium(None,None,1/12,SVIX1,None,True)
    EP1_2 = EquityPremium(1/12,1/6,1/12,SVIX1,SVIX2,False)
    EP2_3 = EquityPremium(1/12,1/4,1/6,SVIX2,SVIX3,False)
    EP3_6 = EquityPremium(1/4,1/2,1/4,SVIX3,SVIX6,False)
    EP6_12 = EquityPremium(1/2,1,1/2,SVIX6,SVIX12,False)
    
    Term_Structure.iloc[i][1] = 1/12*EP0_1 
    Term_Structure.iloc[i][2] = 1/12*EP1_2
    Term_Structure.iloc[i][3] = 1/12*EP2_3
    Term_Structure.iloc[i][4] = 1/4*EP3_6
    Term_Structure.iloc[i][5] = 1/2*EP6_12
    
# Formats the data for the plot
dates = []
for i in range(0,len(Term_Structure["Date"])):
    dates.append(datetime.datetime.strptime(Term_Structure["Date"].iloc[i], "%d/%m/%Y"))
  
Term_Structure["Date"] = dates
Term_Structure["0_2"] = Term_Structure["W EP0_1"] + Term_Structure["W EP1_2"]
Term_Structure["0_3"] = Term_Structure["0_2"] + Term_Structure["W EP2_3"]
Term_Structure["0_6"] = Term_Structure["0_3"] + Term_Structure["W EP3_6"]
Term_Structure["0_12"] = Term_Structure["0_6"] + Term_Structure["W EP6_12"]
Term_Structure["0_1R10"] = Term_Structure["W EP0_1"].rolling(window=10).mean()
Term_Structure["0_2R10"] = Term_Structure["0_2"].rolling(window=10).mean()
Term_Structure["0_3R10"] = Term_Structure["0_3"].rolling(window=10).mean()
Term_Structure["0_6R10"] = Term_Structure["0_6"].rolling(window=10).mean()
Term_Structure["0_12R10"] = Term_Structure["0_12"].rolling(window=10).mean()
Term_Structure = Term_Structure.set_index("Date")

# Plots the complete term structure 
fig,ax = plt.subplots(figsize=(12,8))
Term_Structure["0_1R10"].plot(x_compat=True,ax=ax,label="_nonlegend_")
Term_Structure["0_2R10"].plot(x_compat=True,ax=ax,c="firebrick",label="_nonlegend_")
Term_Structure["0_3R10"].plot(x_compat=True,ax=ax,c="b",label="_nonlegend_")
Term_Structure["0_6R10"].plot(x_compat=True,ax=ax,c="peachpuff",label="_nonlegend_")
Term_Structure["0_12R10"].plot(x_compat=True,ax=ax,label="_nonlegend_",c="gray")
ax.fill_between(Term_Structure.index,Term_Structure["0_12R10"],Term_Structure["0_6R10"],color="lightgray",
                label="6 Months -> 12 Months")
ax.fill_between(Term_Structure.index,Term_Structure["0_6R10"],Term_Structure["0_3R10"],color="peachpuff",
                label="3 Months -> 6 Months")
ax.fill_between(Term_Structure.index,Term_Structure["0_3R10"],Term_Structure["0_2R10"],color="b",
                label="2 Months -> 3 Months")
ax.fill_between(Term_Structure.index,Term_Structure["0_2R10"],Term_Structure["0_1R10"],color="firebrick",
                label="1 Month -> 2 Months")
ax.fill_between(Term_Structure.index,Term_Structure["0_1R10"],color="skyblue",
                label="0 Month -> 1 Month")
plt.tick_params(axis="both",which="major",labelsize=15)
ax.set_xlabel("")
plt.xticks(rotation=0,ha="center")
plt.xlim("1996","2018")
ax.legend(loc=0,fontsize=17)
plt.show()
 
    









