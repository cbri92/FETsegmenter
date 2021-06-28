# -*- coding: utf-8 -*-
"""
Created on Mon Apr 26 09:10:23 2021

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
import pingouin as pg

#%%Set Working directory
        
data_supradir = 'C:/Users/cbri3325/Dropbox (Sydney Uni)/Caterina Brighi/Data/FET GBM/Analysed/' #Set working directory

IntraICC_df = pd.read_excel(data_supradir+'IntraICCdf.xlsx', sheet_name=None, index_col=None)
n_readers = len(IntraICC_df)
Readers_names = list(IntraICC_df.keys())

InterICC_df = pd.read_excel(data_supradir+'InterICCdf2.xlsx', sheet_name='Sheet1', index_col=None)
# n_subjects = len(InterICC_df)
# Subjects_names = list(InterICC_df.keys())

Results_IntraICC = {'BTV_MI': pd.DataFrame(columns=['Reader', 'Type', 'Description','ICC', 'F', 'df1', 'df2', 'pval', 'CI95%']), 'BTV_CS': pd.DataFrame(columns=['Reader', 'Type', 'Description','ICC', 'F', 'df1', 'df2', 'pval', 'CI95%']), 'CTRLmean_MI': pd.DataFrame(columns=['Reader', 'Type', 'Description','ICC', 'F', 'df1', 'df2', 'pval', 'CI95%']), 'CTRLmean_CS': pd.DataFrame(columns=['Reader', 'Type', 'Description','ICC', 'F', 'df1', 'df2', 'pval', 'CI95%'])}
IntraWriter = pd.ExcelWriter(data_supradir +'IntraICCResults.xlsx', engine='xlsxwriter')

Results_InterICC = {'BTV_MI': pd.DataFrame(columns=['Type', 'Description','ICC', 'F', 'df1', 'df2', 'pval', 'CI95%']), 'BTV_CS': pd.DataFrame(columns=['Type', 'Description','ICC', 'F', 'df1', 'df2', 'pval', 'CI95%']), 'CTRLmean_MI': pd.DataFrame(columns=['Type', 'Description','ICC', 'F', 'df1', 'df2', 'pval', 'CI95%']), 'CTRLmean_CS': pd.DataFrame(columns=['Type', 'Description','ICC', 'F', 'df1', 'df2', 'pval', 'CI95%'])}
InterWriter = pd.ExcelWriter(data_supradir +'InterICCResults.xlsx', engine='xlsxwriter')

for e in range(0, n_readers):
    
    reader_df = IntraICC_df.get(Readers_names[e])
    reader_df = reader_df.fillna(0)
    reader = Readers_names[e]
    
    IntraICC_reader_BTVmi = pg.intraclass_corr(data=reader_df, targets='Patient', raters='Measurement', ratings='BTV(MI)')    
    Results_IntraICC['BTV_MI'] = Results_IntraICC['BTV_MI'].append({'Reader': reader,
                                                         'Type':IntraICC_reader_BTVmi.loc[1, 'Type'],
                                                         'Description':IntraICC_reader_BTVmi.loc[1, 'Description'], 
                                                         'ICC':IntraICC_reader_BTVmi.loc[1, 'ICC'], 
                                                         'F':IntraICC_reader_BTVmi.loc[1, 'F'],
                                                         'df1':IntraICC_reader_BTVmi.loc[1, 'df1'],
                                                         'df2':IntraICC_reader_BTVmi.loc[1, 'df2'],
                                                         'pval':IntraICC_reader_BTVmi.loc[1, 'pval'],
                                                         'CI95%':IntraICC_reader_BTVmi.loc[1, 'CI95%']
                                                         }, ignore_index=True)
    
    IntraICC_reader_BTVcs = pg.intraclass_corr(data=reader_df, targets='Patient', raters='Measurement', ratings='BTV(CS)')    
    Results_IntraICC['BTV_CS'] = Results_IntraICC['BTV_CS'].append({'Reader': reader,
                                                         'Type':IntraICC_reader_BTVcs.loc[1, 'Type'],
                                                         'Description':IntraICC_reader_BTVcs.loc[1, 'Description'], 
                                                         'ICC':IntraICC_reader_BTVcs.loc[1, 'ICC'], 
                                                         'F':IntraICC_reader_BTVcs.loc[1, 'F'],
                                                         'df1':IntraICC_reader_BTVcs.loc[1, 'df1'],
                                                         'df2':IntraICC_reader_BTVcs.loc[1, 'df2'],
                                                         'pval':IntraICC_reader_BTVcs.loc[1, 'pval'],
                                                         'CI95%':IntraICC_reader_BTVcs.loc[1, 'CI95%']
                                                         }, ignore_index=True)
     
    IntraICC_reader_CTRLmi = pg.intraclass_corr(data=reader_df, targets='Patient', raters='Measurement', ratings='CTRL VOImean(MI)')    
    Results_IntraICC['CTRLmean_MI'] = Results_IntraICC['CTRLmean_MI'].append({'Reader': reader,
                                                         'Type':IntraICC_reader_CTRLmi.loc[1, 'Type'],
                                                         'Description':IntraICC_reader_CTRLmi.loc[1, 'Description'], 
                                                         'ICC':IntraICC_reader_CTRLmi.loc[1, 'ICC'], 
                                                         'F':IntraICC_reader_CTRLmi.loc[1, 'F'],
                                                         'df1':IntraICC_reader_CTRLmi.loc[1, 'df1'],
                                                         'df2':IntraICC_reader_CTRLmi.loc[1, 'df2'],
                                                         'pval':IntraICC_reader_CTRLmi.loc[1, 'pval'],
                                                         'CI95%':IntraICC_reader_CTRLmi.loc[1, 'CI95%']
                                                         }, ignore_index=True)
    
    IntraICC_reader_CTRLcs = pg.intraclass_corr(data=reader_df, targets='Patient', raters='Measurement', ratings='CTRL VOImean(CS)')    
    Results_IntraICC['CTRLmean_CS'] = Results_IntraICC['CTRLmean_CS'].append({'Reader': reader,
                                                         'Type':IntraICC_reader_CTRLcs.loc[1, 'Type'],
                                                         'Description':IntraICC_reader_CTRLcs.loc[1, 'Description'], 
                                                         'ICC':IntraICC_reader_CTRLcs.loc[1, 'ICC'], 
                                                         'F':IntraICC_reader_CTRLcs.loc[1, 'F'],
                                                         'df1':IntraICC_reader_CTRLcs.loc[1, 'df1'],
                                                         'df2':IntraICC_reader_CTRLcs.loc[1, 'df2'],
                                                         'pval':IntraICC_reader_CTRLcs.loc[1, 'pval'],
                                                         'CI95%':IntraICC_reader_CTRLcs.loc[1, 'CI95%']
                                                         }, ignore_index=True)
    
    
    
    

InterICC_reader_BTVmi = pg.intraclass_corr(data=InterICC_df, targets='Patient', raters='Reader', ratings='BTV(MI)')    
Results_InterICC['BTV_MI'] = Results_InterICC['BTV_MI'].append({'Type':InterICC_reader_BTVmi.loc[1, 'Type'],
                                                         'Description':InterICC_reader_BTVmi.loc[1, 'Description'], 
                                                         'ICC':InterICC_reader_BTVmi.loc[1, 'ICC'], 
                                                         'F':InterICC_reader_BTVmi.loc[1, 'F'],
                                                         'df1':InterICC_reader_BTVmi.loc[1, 'df1'],
                                                         'df2':InterICC_reader_BTVmi.loc[1, 'df2'],
                                                         'pval':InterICC_reader_BTVmi.loc[1, 'pval'],
                                                         'CI95%':InterICC_reader_BTVmi.loc[1, 'CI95%']
                                                         }, ignore_index=True)
    
InterICC_reader_BTVcs = pg.intraclass_corr(data=InterICC_df, targets='Patient', raters='Reader', ratings='BTV(CS)')    
Results_InterICC['BTV_CS'] = Results_InterICC['BTV_CS'].append({'Type':InterICC_reader_BTVcs.loc[1, 'Type'],
                                                         'Description':InterICC_reader_BTVcs.loc[1, 'Description'], 
                                                         'ICC':InterICC_reader_BTVcs.loc[1, 'ICC'], 
                                                         'F':InterICC_reader_BTVcs.loc[1, 'F'],
                                                         'df1':InterICC_reader_BTVcs.loc[1, 'df1'],
                                                         'df2':InterICC_reader_BTVcs.loc[1, 'df2'],
                                                         'pval':InterICC_reader_BTVcs.loc[1, 'pval'],
                                                         'CI95%':InterICC_reader_BTVcs.loc[1, 'CI95%']
                                                         }, ignore_index=True)
     
InterICC_reader_CTRLmi = pg.intraclass_corr(data=InterICC_df, targets='Patient', raters='Reader', ratings='CTRL VOImean(MI)')    
Results_InterICC['CTRLmean_MI'] = Results_InterICC['CTRLmean_MI'].append({'Type':InterICC_reader_CTRLmi.loc[1, 'Type'],
                                                         'Description':InterICC_reader_CTRLmi.loc[1, 'Description'], 
                                                         'ICC':InterICC_reader_CTRLmi.loc[1, 'ICC'], 
                                                         'F':InterICC_reader_CTRLmi.loc[1, 'F'],
                                                         'df1':InterICC_reader_CTRLmi.loc[1, 'df1'],
                                                         'df2':InterICC_reader_CTRLmi.loc[1, 'df2'],
                                                         'pval':InterICC_reader_CTRLmi.loc[1, 'pval'],
                                                         'CI95%':InterICC_reader_CTRLmi.loc[1, 'CI95%']
                                                         }, ignore_index=True)
    
InterICC_reader_CTRLcs = pg.intraclass_corr(data=InterICC_df, targets='Patient', raters='Reader', ratings='CTRL VOImean(CS)')    
Results_InterICC['CTRLmean_CS'] = Results_InterICC['CTRLmean_CS'].append({'Type':InterICC_reader_CTRLcs.loc[1, 'Type'],
                                                         'Description':InterICC_reader_CTRLcs.loc[1, 'Description'], 
                                                         'ICC':InterICC_reader_CTRLcs.loc[1, 'ICC'], 
                                                         'F':InterICC_reader_CTRLcs.loc[1, 'F'],
                                                         'df1':InterICC_reader_CTRLcs.loc[1, 'df1'],
                                                         'df2':InterICC_reader_CTRLcs.loc[1, 'df2'],
                                                         'pval':InterICC_reader_CTRLcs.loc[1, 'pval'],
                                                         'CI95%':InterICC_reader_CTRLcs.loc[1, 'CI95%']
                                                         }, ignore_index=True)
    
    
for name, df in Results_IntraICC.items():
    df.to_excel(IntraWriter, sheet_name=name, index=False)
IntraWriter.save()
    
for name, df in Results_InterICC.items():
    df.to_excel(InterWriter, sheet_name=name, index=False)
InterWriter.save()