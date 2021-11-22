# -*- coding: utf-8 -*-
"""
Created on Sun Nov 1 12:21:00 2020

@author: cbri3325
"""

#%% Import functions 

import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import pandas as pd
import datetime
import os
import glob
import shutil
import xlsxwriter
import time
from scipy.stats.stats import pearsonr

def createList(r1, r2): 
    return [item for item in range(r1, r2+1)] 

#%% Set Working directory
        
data_supradir = 'path to directory containing analysis results xlsx files' #Set working directory


users_path = [ f.path for f in os.scandir(data_supradir) if f.is_dir() ] #Create a list of the paths to the users directories
users_name = [ f.name for f in os.scandir(data_supradir) if f.is_dir() ] #Create a lisdt of users names

n_users = len(users_name) #Total number of subjects

print(users_path)

subj_list = ['AB001', 'DA003', 'FF004', 'GF002', 'GW005', 'KF006']
storeResults = {subj: pd.DataFrame(columns=['User', 'Repeats', 'Method', 'BTV Volume [mm3]', 'CTRL VOI Mean intensity [SUV]']) for subj in subj_list}

for current in users_name:
    user_dir = data_supradir+current
    user_name = current
    
    #Set paths to subfolders    
    MI_dir = user_dir +'/MI method'
    CS_dir = user_dir +'/CS method'
    
    MI_results_df = pd.read_excel(MI_dir+'/Results_MI.xlsx', sheet_name=None)
    CS_results_df = pd.read_excel(CS_dir+'/Results_CS.xlsx', sheet_name=None)
    
    n_repeats = len(MI_results_df)
    
    n_subjs = len(MI_results_df.get('Repeat1')['Subject_ID'])
    # subj_list = MI_results_df.get('Repeat1')['Subject_ID'].tolist()
    
    MI_results_df = pd.read_excel(MI_dir+'/Results_MI.xlsx', sheet_name=None, index_col='Subject_ID')
    CS_results_df = pd.read_excel(CS_dir+'/Results_CS.xlsx', sheet_name=None, index_col='Subject_ID')

    #Create empty dataframes to populate as going through the loop
    # storeResults = {subj: pd.DataFrame(columns=['User', 'Repeats', 'Method', 'BTV Volume [mm3]', 'CTRL VOI Mean intensity [SUV]']) for subj in subj_list}
    
    for repeat in range(1, n_repeats+1):
        # Repeats_ns = Repeats_ns.append([repeat])
        MI_BTV_CTRL = MI_results_df.get('Repeat'+str(repeat)).loc[:, ['BTV Volume [mm3]','CTRL VOI Mean intensity [SUV]']]
        CS_BTV_CTRL = CS_results_df.get('Repeat'+str(repeat)).loc[:, ['BTV Volume [mm3]','CTRL VOI Mean intensity [SUV]']]
        method1, method2 = 'MI', 'CS'

        for subj in subj_list:
            storeResults[subj] = storeResults[subj].append({'User': current,
                                                         'Repeats': repeat,
                                                         'Method': method1,
                                                         'BTV Volume [mm3]': float(MI_BTV_CTRL.loc[subj, 'BTV Volume [mm3]']),
                                                         'CTRL VOI Mean intensity [SUV]': float(MI_BTV_CTRL.loc[subj, 'CTRL VOI Mean intensity [SUV]'])
                                                         }, ignore_index=True)
                                                         
            storeResults[subj] = storeResults[subj].append({'User': current,
                                                         'Repeats': repeat,
                                                         'Method': method2,
                                                         'BTV Volume [mm3]': float(CS_BTV_CTRL.loc[subj, 'BTV Volume [mm3]']),
                                                         'CTRL VOI Mean intensity [SUV]': float(CS_BTV_CTRL.loc[subj, 'CTRL VOI Mean intensity [SUV]'])
                                                         }, ignore_index=True)

# new_df = df.groupby(['User', 'Method']).['BTV Volume [mm3]'].agg({'mean','std'})
# df = df.merge(new_df, left_on=['User', 'Method'], right_index=True)

writer = pd.ExcelWriter(data_supradir +'OverallResults.xlsx', engine='xlsxwriter')

for name, df in storeResults.items():
    # Calculate CoV values for BTV and CTRL for each group of User, Method for each Subject
    BTV_df = df.groupby(['User', 'Method'])['BTV Volume [mm3]'].agg({'mean','std'})
    CTRL_df = df.groupby(['User', 'Method'])['CTRL VOI Mean intensity [SUV]'].agg({'mean','std'})

    BTV_df['BTV_CoV'] = BTV_df['std']/BTV_df['mean']
    CTRL_df['CTRL_CoV'] = CTRL_df['std']/CTRL_df['mean']

    df = df.merge(BTV_df['BTV_CoV'], left_on=['User', 'Method'], right_index=True)
    df = df.merge(CTRL_df['CTRL_CoV'], left_on=['User', 'Method'], right_index=True)

    df.to_excel(writer, sheet_name=name, index=False)
writer.save()

            
            
            
            
