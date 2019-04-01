# -*- coding: utf-8 -*-
"""
Created on Tue Nov  6 08:54:22 2018

@author: nilsh
"""

import os
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures


def f7(seq): # Function to format a set
    seen = set()
    seen_add = seen.add
    return[x for x in seq if not(x in seen or seen_add(x))]

def SliceByDay(): # Reads in data and calls the probability calculation for every day, 
    # Returns daily and average monthly crash probabilities
    path = os.getcwd() + "\Data\Put_Option_Data 28-29 Dec 2017.xlsx"
    path1 = os.getcwd() + "\Data\Index_And_Rf.xlsx"
    data = pd.read_excel(path, sheet_name = "WRDS")
    dates = f7(data["The Date of this Price"])
    data1 = pd.read_excel(path1, sheet_name = "Sheet1")
    CrashProb = pd.DataFrame(columns=["Date","1mo", "6mo","12mo","Mo"])
    CrashProbAv = pd.DataFrame(columns=["Month","1mo","6mo","12mo"])

    for i in range(len(dates)):
        CrashProb.loc[i] = ""
        Index = data1.loc[data1["Date"] == dates[i], "S&P 500"].iloc[0]
        df = data[data["The Date of this Price"].isin([dates[i]])]
        CrashProb.iloc[i][0] = dates[i]
        CrashProb.iloc[i][1] = SliceByExpiry(df, Index, 30, 0.8)
        CrashProb.iloc[i][2] = SliceByExpiry(df, Index, 182, 0.8)
        CrashProb.iloc[i][3] = SliceByExpiry(df, Index, 365, 0.8)
        CrashProb.iloc[i][4] = dates[i][3:]
        
    j = 0 
    for i in range(1,CrashProb.shape[0]):
        if dates[i][3:] != dates[i-1][3:]:
            CrashProbAv.loc[j] = ""
            df_av = CrashProb[CrashProb["Mo"] == dates[i-1][3:]]
            CrashProbAv.iloc[j][0] = dates[i-1][3:]
            CrashProbAv.iloc[j][1] = df_av["1mo"].mean()
            CrashProbAv.iloc[j][2] = df_av["6mo"].mean()
            CrashProbAv.iloc[j][3] = df_av["12mo"].mean()
            j +=1
   
    CrashProbAv.loc[j] = ""
    df_av = CrashProb[CrashProb["Mo"] == dates[i-1][3:]]
    CrashProbAv.iloc[j][0] = dates[i-1][3:]
    CrashProbAv.iloc[j][1] = df_av["1mo"].mean()
    CrashProbAv.iloc[j][2] = df_av["6mo"].mean()
    CrashProbAv.iloc[j][3] = df_av["12mo"].mean()
    
    return CrashProb, CrashProbAv


def SliceByExpiry(df,Index,time_frame,alpha = 0.8): # Returns the adjacent maturities, calls the procedure
    # to calculate their probabilities, and interpolates these to obtain the final daily probability
    Expiration_days = list(set(df["Days Until Expiration"]))
    Expiration_days = sorted(Expiration_days)
    
    j = 0 
    for i in range(len(Expiration_days)):
        data = df.loc[df["Days Until Expiration"].isin([Expiration_days[i-j]])]
        if data.shape[0] <= 6: 
            Expiration_days.remove(Expiration_days[i-j])
            j+=1
    
    app_maturity_first = min(Expiration_days, key=lambda x:abs(x-time_frame))
    data_first = df.loc[df["Days Until Expiration"].isin([app_maturity_first])]
    Expiration_days.remove(app_maturity_first)
    app_maturity_second = min(Expiration_days, key=lambda x:abs(x-time_frame))
    data_second = df.loc[df["Days Until Expiration"].isin([app_maturity_second])]
    
    if app_maturity_second > app_maturity_first: 
        app_maturity_close = app_maturity_first
        data_close = data_first
        app_maturity_far = app_maturity_second
        data_far = data_second
    elif app_maturity_second < app_maturity_first: 
        app_maturity_close = app_maturity_second
        data_close = data_second
        app_maturity_far = app_maturity_first
        data_far = data_first
    
    daily_prob_close = DailyProb(data_close,Index,time_frame,alpha)
    daily_prob_far = DailyProb(data_far,Index,time_frame,alpha)
    
    if app_maturity_close == time_frame:
        daily_prob = daily_prob_close
    elif app_maturity_far == time_frame:
        daily_prob = daily_prob_far
    else: 
        daily_prob = (app_maturity_far - time_frame)/(app_maturity_far-app_maturity_close)*daily_prob_close + (time_frame-app_maturity_close)/(app_maturity_far-app_maturity_close)*daily_prob_far

    return daily_prob

 
def Slope(Close_price, Close_strike, Far_price, Far_strike): # Returns the slope of the option price curve
    slope = (Far_price-Close_price)/(Far_strike-Close_strike)
        
    return slope


def DailyProb(data,St,time_frame,alpha=0.8): # Returns the probability of a market crash for the day provided
    alpha_st = alpha*St
    Strikes = list(set(data["Strike"]))
    Strikes = sorted(Strikes)
    data = data.sort_values(by=["Strike"])
    data = data.reset_index()
    i = 0 
    
    if data.iloc[0]["Strike"] >= alpha_st:
        if time_frame >= 182:
            data.loc[-1] = ""
            data.loc[-1]["Strike"] = 0
            data.loc[-1]["Mid Price"] = 0
            data.index = data.index+1
            data = data.sort_index()
            X = np.array(data["Strike"][1:3])
            y = data["Mid Price"][1:3]
        else:
            data.loc[-1] = ""
            data.loc[-1]["Strike"] = 0
            data.loc[-1]["Mid Price"] = 0
            data.index = data.index+1
            data = data.sort_index()
            X = np.array(data["Strike"][:3])    
            y = data["Mid Price"][:3]       
    else:
        closest_strike = min(data["Strike"], key=lambda x:abs(x-alpha_st))
        index = data.index[data["Strike"] == closest_strike][0]
        if closest_strike > alpha_st:
            i = 1 
        if index > 0:
            X = np.array(data["Strike"][index-i:index+3-i])
            y = data["Mid Price"][index-i:index+3-i]
        else: 
            X = np.array(data["Strike"][index:index+4])
            y = data["Mid Price"][index:index+4]

    poly = PolynomialFeatures(degree=30) 
    X_poly = poly.fit_transform(X.reshape(-1,1))
    regr = LinearRegression()
    regr.fit(X_poly, y)

    plot_x1 = np.linspace(min(X),alpha_st, 10000)
    plot_x2 = np.linspace(alpha_st, max(X), 10000)
    plot_x = np.concatenate((plot_x1,plot_x2[1:]), axis = 0)
    plot_y = regr.intercept_ + np.sum(regr.coef_*poly.fit_transform(plot_x.reshape(-1,1)),axis = 1)
    
    alpha_st_index = np.where(plot_x==alpha_st)[0][0]
    put_aSt = plot_y[alpha_st_index]
    slope =  (plot_y[alpha_st_index+1]-plot_y[alpha_st_index])/(plot_x[alpha_st_index+1]-plot_x[alpha_st_index])
    prob = alpha*(slope-put_aSt/alpha_st)
    
    return prob


prob, probAV = SliceByDay()  # Returns dataframes with the daily and average monthly probability
print(probAV.head()) # Prints the head of the dataframe with average monthly probabilities  



