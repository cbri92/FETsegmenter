# -*- coding: utf-8 -*-
"""
Created on Fri Dec 11 13:50:05 2020

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

#%%Set Working directory
        
data_supradir = 'C:/Users/cbri3325/Dropbox (Sydney Uni)/Caterina Brighi/Data/FET GBM/Analysed/' #Set working directory

Results_df = pd.read_excel(data_supradir+'OverallResults.xlsx', sheet_name=None, index_col=None)
n_patients = len(Results_df)

Patients_names = list(Results_df.keys())

# users = list(Results_df.get(Patients_names[0]).User.unique())
storeResults = {patient: pd.DataFrame(columns=['User', 'Mean CTRL SUVmean MI [SUV]', 'Mean CTRL SUVmean CS [SUV]', 'Mean BTV Volume MI [mm3]', 'Mean BTV Volume CS [mm3]', 'CoV CTRL SUVmean MI [SUV]', 'CoV CTRL SUVmean CS [SUV]', 'CoV BTV Volume MI [mm3]', 'CoV BTV Volume CS [mm3]']) for patient in Patients_names}
writer = pd.ExcelWriter(data_supradir +'InterUserResults.xlsx', engine='xlsxwriter')

for e in range(0, n_patients):
    
    patient_df = Results_df.get(Patients_names[e])
    patient = Patients_names[e]
    users = list(patient_df.User.unique())
    patient_df = patient_df.set_index('User')
    # methods = list(patient_df.Method.unique())
    repeats = list(patient_df.Repeats.unique())
    
    for user in users:
        CTRL_SUVmean = patient_df.loc[user, 'CTRL VOI Mean intensity [SUV]' ]
        CTRL_SUVmean_MI = CTRL_SUVmean[:len(repeats)]
        CTRL_SUVmean_CS = CTRL_SUVmean[len(repeats):2*len(repeats)]
        
        BTV_vol = patient_df.loc[user, 'BTV Volume [mm3]' ]
        BTV_vol_MI = BTV_vol[:len(repeats)]
        BTV_vol_CS = BTV_vol[len(repeats):2*len(repeats)]
        
        Mean_CTRL_MI = CTRL_SUVmean_MI.mean()
        Mean_CTRL_CS = CTRL_SUVmean_CS.mean()
        
        Mean_BTV_MI = BTV_vol_MI.mean()
        Mean_BTV_CS = BTV_vol_CS.mean()
        
        storeResults[patient] = storeResults[patient].append({'User': user,
                                                         'Mean CTRL SUVmean MI [SUV]':Mean_CTRL_MI,
                                                         'Mean CTRL SUVmean CS [SUV]':Mean_CTRL_CS, 
                                                         'Mean BTV Volume MI [mm3]':Mean_BTV_MI, 
                                                         'Mean BTV Volume CS [mm3]':Mean_BTV_CS
                                                         }, ignore_index=True)
        
    CoV_CTRL_MI = storeResults[patient].get('Mean CTRL SUVmean MI [SUV]').std()/storeResults[patient].get('Mean CTRL SUVmean MI [SUV]').mean()
    CoV_CTRL_CS = storeResults[patient].get('Mean CTRL SUVmean CS [SUV]').std()/storeResults[patient].get('Mean CTRL SUVmean CS [SUV]').mean()
    CoV_BTV_MI = storeResults[patient].get('Mean BTV Volume MI [mm3]').std()/storeResults[patient].get('Mean BTV Volume MI [mm3]').mean()
    CoV_BTV_CS = storeResults[patient].get('Mean BTV Volume CS [mm3]').std()/storeResults[patient].get('Mean BTV Volume CS [mm3]').mean()
    
    storeResults[patient] = storeResults[patient].append({'CoV CTRL SUVmean MI [SUV]':CoV_CTRL_MI,
                                                         'CoV CTRL SUVmean CS [SUV]':CoV_CTRL_CS, 
                                                         'CoV BTV Volume MI [mm3]':CoV_BTV_MI, 
                                                         'CoV BTV Volume CS [mm3]':CoV_BTV_CS
                                                         }, ignore_index=True)
    

for name, df in storeResults.items():
    df.to_excel(writer, sheet_name=name, index=False)
writer.save()
