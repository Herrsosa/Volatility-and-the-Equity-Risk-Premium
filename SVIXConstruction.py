# -*- coding: utf-8 -*-
"""
Created on Fri Oct  5 16:17:42 2018

@author: nilsh
"""
import pandas as pd
import numpy as np
import os
import pdb
import math

def f7(seq): # Function to format a set
    seen = set()
    seen_add = seen.add
    return[x for x in seq if not(x in seen or seen_add(x))]

def Slice_by_day(): # Reads in data and calls the SVIX construction function for every day
    path = os.getcwd() + "\Data\Option_Data 28-29 Dec 2017.xlsx"
    path1 = os.getcwd() + "\Data\Index_And_Rf.xlsx"
    data = pd.read_excel(path, sheet_name = "WRDS")
    data1 = pd.read_excel(path1, sheet_name = "Sheet1")
    dates = f7(data["The Date of this Price"])
    SVIX = pd.DataFrame(columns = ["Date", "1mo", "2mo", "3mo", "6mo", "12mo"])

    for i in range(0,len(dates)):
        SVIX.loc[i] = ""
        df = data[data["The Date of this Price"].isin([dates[i]])]
        SVIX.iloc[i][0] = dates[i]
        Rf1 = data1.loc[data1["Date"] == dates[i], "Rf,t-1"].iloc[0]
        Rf2 = data1.loc[data1["Date"] == dates[i], "Rf,t-2"].iloc[0]
        Rf3 = data1.loc[data1["Date"] == dates[i], "Rf,t-3"].iloc[0]
        Rf6 = data1.loc[data1["Date"] == dates[i], "Rf,t-6"].iloc[0]
        Rf12 = data1.loc[data1["Date"] == dates[i], "Rf,t-12"].iloc[0]
        Index = data1.loc[data1["Date"] == dates[i], "S&P 500"].iloc[0]
        SVIX.iloc[i][1] = Compute_SVIX(df, 30, Index, Rf1)
        SVIX.iloc[i][2] = Compute_SVIX(df, 60, Index, Rf2)
        SVIX.iloc[i][3] = Compute_SVIX(df, 91, Index, Rf3)
        SVIX.iloc[i][4] = Compute_SVIX(df, 182, Index, Rf6)
        SVIX.iloc[i][5] = Compute_SVIX(df, 365, Index, Rf12)
  
    return SVIX 
        
        
def SVIX_TimeFrame(data, time_in_days): # Returns adjacent maturities and the corresponding option dataframes
    Expiration_Days = list(set(data["Days Until Expiration"]))
    Expiration_Days = sorted(Expiration_Days)

    Far_Maturity = None
    Close_Maturity = None
    
    check_close = False
    check_far = False
    for i in range(0,len(set(data["Days Until Expiration"]))):
        if time_in_days <= Expiration_Days[i] and Expiration_Days[i-1] >= 7 and i-1 >=0:
            while check_close == False:
                count = 0
                close_mat_strikes = data.loc[(data["Days Until Expiration"] == Expiration_Days[i-1]), "Strike Price of the Option Times 1000"] 
                close_cal_strikes = data.loc[(data["C=Call, P=Put"]=="C") & (data["Days Until Expiration"] == Expiration_Days[i-1]), "Strike Price of the Option Times 1000"]
                close_put_strikes = data.loc[(data["C=Call, P=Put"]=="P") & (data["Days Until Expiration"] == Expiration_Days[i-1]), "Strike Price of the Option Times 1000"]
                for j in range(0,len(close_mat_strikes)):                    
                    if close_mat_strikes.iloc[j] in close_cal_strikes.values and close_mat_strikes.iloc[j] in close_put_strikes.values:
                        count += 1
                        if count == 2:
                            Close_Maturity = Expiration_Days[i-1]
                            check_close = True
                            break
                
                if check_close == False: 
                    i +=1
                    
            while check_far == False:
                count = 0
                far_mat_strikes = data.loc[(data["Days Until Expiration"] == Expiration_Days[i]), "Strike Price of the Option Times 1000"]
                far_cal_strikes = data.loc[(data["C=Call, P=Put"]=="C") & (data["Days Until Expiration"] == Expiration_Days[i]), "Strike Price of the Option Times 1000"]
                far_put_strikes = data.loc[(data["C=Call, P=Put"]=="P") & (data["Days Until Expiration"] == Expiration_Days[i]), "Strike Price of the Option Times 1000"]
                for j in range(0,len(far_mat_strikes)): 
                    if far_mat_strikes.iloc[j] in far_cal_strikes.values and far_mat_strikes.iloc[j] in far_put_strikes.values:                             
                        count += 1
                        if count == 2:
                            Far_Maturity = Expiration_Days[i]
                            check_far = True
                            break
                
                if check_far == False:
                    i +=1

            break

    if Far_Maturity == None:
        for i in range(len(set(data["Days Until Expiration"]))-1,1,-1):
            while check_close == False:
                count = 0
                close_mat_strikes = data.loc[(data["Days Until Expiration"] == Expiration_Days[i-1]), "Strike Price of the Option Times 1000"]
                close_cal_strikes = data.loc[(data["C=Call, P=Put"]=="C") & (data["Days Until Expiration"] == Expiration_Days[i-1]), "Strike Price of the Option Times 1000"]
                close_put_strikes = data.loc[(data["C=Call, P=Put"]=="P") & (data["Days Until Expiration"] == Expiration_Days[i-1]), "Strike Price of the Option Times 1000"]
                for j in range(0,len(close_mat_strikes)):                    
                    if close_mat_strikes.iloc[j] in close_cal_strikes.values and close_mat_strikes.iloc[j] in close_put_strikes.values:
                        count += 1
                        if count == 2:
                            Close_Maturity = Expiration_Days[i-1]
                            check_close = True
                            break
                
                if check_close == False: 
                    i +=1
                    
            while check_far == False:
                count = 0
                far_mat_strikes = data.loc[(data["Days Until Expiration"] == Expiration_Days[i]), "Strike Price of the Option Times 1000"]
                far_cal_strikes = data.loc[(data["C=Call, P=Put"]=="C") & (data["Days Until Expiration"] == Expiration_Days[i]), "Strike Price of the Option Times 1000"]
                far_put_strikes = data.loc[(data["C=Call, P=Put"]=="P") & (data["Days Until Expiration"] == Expiration_Days[i]), "Strike Price of the Option Times 1000"]
                for j in range(0,len(far_mat_strikes)): 
                    if far_mat_strikes.iloc[j] in far_cal_strikes.values and far_mat_strikes.iloc[j] in far_put_strikes.values:                             
                        count += 1
                        if count == 2:
                            Far_Maturity = Expiration_Days[i]
                            check_far = True
                            break
                
                if check_far == False:
                    i +=1
            break
    
    dates_far = data[data["Days Until Expiration"].isin([Far_Maturity])]
    dates_far = dates_far.reset_index()
    dates_close = data[data["Days Until Expiration"].isin([Close_Maturity])]
    dates_close= dates_close.reset_index()
    
    
    dates_far_return = pd.DataFrame(columns = ["K", "Call Price", "Put Price", "Dif Mid", "DK"])
    Strikes_Far = sorted(set(dates_far["Strike Price of the Option Times 1000"].copy()))
        
    for i in range(0, len(Strikes_Far)):
        dates_far_return.loc[i] = ""
        
        dates_far_return.iloc[i][0] = Strikes_Far[i]
        try:
            dates_far_return.iloc[i][1] = dates_far.loc[(dates_far["Strike Price of the Option Times 1000"] == dates_far_return.iloc[i][0]) & (dates_far["C=Call, P=Put"]=="C"), "Mid Price"].copy().iloc[0]
        except: 
            dates_far_return.iloc[i][1] = np.nan
        try: 
            dates_far_return.iloc[i][2] = dates_far.loc[(dates_far["Strike Price of the Option Times 1000"] == dates_far_return.iloc[i][0]) & (dates_far["C=Call, P=Put"]=="P"), "Mid Price"].copy().iloc[0]
        except:
            dates_far_return.iloc[i][2] = np.nan
  
        dates_far_return.iloc[i][3] = abs(dates_far_return.iloc[i][1]-dates_far_return.iloc[i][2])
    
    Forward_Far = Return_Forward(dates_far_return)

    del_i = [] 

    for i in range(0, len(Strikes_Far)):
        if dates_far_return.iloc[i][0] < Forward_Far: 
            if math.isnan(dates_far_return.iloc[i][2]):
                del_i.append(i)
        elif dates_far_return.iloc[i][0] >= Forward_Far:
            if math.isnan(dates_far_return.iloc[i][1]):
                del_i.append(i)
    
    dates_far_return = dates_far_return.drop(del_i, axis = 0)        

    for i in range(1, len(dates_far_return)-1):
        dates_far_return.iloc[i][4] = (dates_far_return.iloc[i+1][0]-dates_far_return.iloc[i-1][0])/2
    
    dates_far_return.iloc[0][4] = dates_far_return.iloc[1][0] - dates_far_return.iloc[0][0]
    dates_far_return.iloc[len(dates_far_return)-1][4] = dates_far_return.iloc[len(dates_far_return)-1][0] - dates_far_return.iloc[len(dates_far_return)-2][0]
        
    dates_close_return = pd.DataFrame(columns = ["K", "Call Price", "Put Price", "Dif Mid", "DK"])
    Strikes_Close = sorted(set(dates_close["Strike Price of the Option Times 1000"].copy())) 
    
    for i in range(0, len(Strikes_Close)):
        dates_close_return.loc[i] = ""
        
        dates_close_return.iloc[i][0] = Strikes_Close[i]
        try:
            dates_close_return.iloc[i][1] = dates_close.loc[(dates_close["Strike Price of the Option Times 1000"] == dates_close_return.iloc[i][0]) & (dates_close["C=Call, P=Put"]=="C"), "Mid Price"].copy().iloc[0]
        except: 
            dates_close_return.iloc[i][1] = np.nan
        try: 
            dates_close_return.iloc[i][2] = dates_close.loc[(dates_close["Strike Price of the Option Times 1000"] == dates_close_return.iloc[i][0]) & (dates_close["C=Call, P=Put"]=="P"), "Mid Price"].copy().iloc[0]
        except:
            dates_close_return.iloc[i][2] = np.nan 
  
        dates_close_return.iloc[i][3] = abs(dates_close_return.iloc[i][1]-dates_close_return.iloc[i][2])

    
    Forward_Close = Return_Forward(dates_close_return)
    
    del_i = [] 

    for i in range(0, len(Strikes_Close)):
        if dates_close_return.iloc[i][0] < Forward_Close: 
            if math.isnan(dates_close_return.iloc[i][2]):
                del_i.append(i)
        elif dates_close_return.iloc[i][0] >= Forward_Close:
            if math.isnan(dates_close_return.iloc[i][1]):
                del_i.append(i)
    
    dates_close_return = dates_close_return.drop(del_i, axis = 0)        

    for i in range(1, len(dates_close_return)-1):
        dates_close_return.iloc[i][4] = (dates_close_return.iloc[i+1][0]-dates_close_return.iloc[i-1][0])/2
    
    dates_close_return.iloc[0][4] = dates_close_return.iloc[1][0] - dates_close_return.iloc[0][0]
    dates_close_return.iloc[len(dates_close_return)-1][4] = dates_close_return.iloc[len(dates_close_return)-1][0] - dates_close_return.iloc[len(dates_close_return)-2][0]    
    
    dates_close_return.reset_index(drop=True, inplace = True)
    dates_far_return.reset_index(drop=True, inplace = True)

    return dates_far_return, dates_close_return, Far_Maturity, Close_Maturity

def Return_Forward(df): # Returns the forward price of the S&P 500 index
    min_dif = df["Dif Mid"].min()
    try:
        Forward = df.loc[df["Dif Mid"] == min_dif, "K"].copy().iloc[0]
    except:
        pdb.set_trace()     
    return Forward

def Compute_SVIX(df, time_frame, Index, Rf): # Computes the SVIX for the chosen maturity
    [dates_far, dates_close, Far_Maturity, Close_Maturity] = SVIX_TimeFrame(df, time_frame)
    
    Forward_Close = Return_Forward(dates_close)
    Forward_Far = Return_Forward(dates_far)
    
    location_far = dates_far.index[dates_far["K"] == Forward_Far].tolist()[0]
    location_close = dates_close.index[dates_close["K"] == Forward_Close].tolist()[0]
    
    contributions_far = []
    contributions_close = []
    
    for i in range(0, location_far):
        if not math.isnan(dates_far.iloc[i][2]) and not math.isnan(dates_far.iloc[i][4]):
            contributions_far.append(dates_far.iloc[i][2] * dates_far.iloc[i][4])
        else:
            contributions_far.append(0)
    
    for i in range(location_far, len(dates_far)):
        if not math.isnan(dates_far.iloc[i][1]) and not math.isnan(dates_far.iloc[i][4]):
            contributions_far.append(dates_far.iloc[i][1] * dates_far.iloc[i][4])
        else:
            contributions_far.append(0)
    
    sum_far_cont = sum(contributions_far)
    T_t_far = Far_Maturity/365
    Rf_far = 1+((Rf-1)*(Far_Maturity/time_frame))
    SVIX_far = 2*sum_far_cont/(T_t_far*Rf_far*Index**2)
    
    for i in range(0, location_close):
        if not math.isnan(dates_close.iloc[i][2]) and not math.isnan(dates_close.iloc[i][4]):
            contributions_close.append(dates_close.iloc[i][2] * dates_close.iloc[i][4])
        else:
            contributions_close.append(0)
    
    for i in range(location_close, len(dates_close)):
        if not math.isnan(dates_close.iloc[i][1]) and not math.isnan(dates_close.iloc[i][4]):
            contributions_close.append(dates_close.iloc[i][1] * dates_close.iloc[i][4])
        else:
            contributions_close.append(0)

    
    sum_close_cont = sum(contributions_close)
    T_t_close = Close_Maturity/365
    Rf_close = 1+((Rf-1)*(Close_Maturity/time_frame))
    SVIX_close = 2*sum_close_cont/(T_t_close*Rf_close*Index**2)
    
    SVIX = (Far_Maturity-time_frame)/(Far_Maturity-Close_Maturity)*SVIX_close +(time_frame-Close_Maturity)/(Far_Maturity-Close_Maturity)*SVIX_far
    SVIX = SVIX*Rf
        
    return SVIX  

SVIX = Slice_by_day() # Returns a dataframe with the SVIX time series for various maturities
print(SVIX.head()) # Prints the head of the SVIX dataframe

