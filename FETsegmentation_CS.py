# -*- coding: utf-8 -*-
"""
Created on Thu Oct  1 09:13:49 2020

@author: cbri3325
"""

#%% Import functions 

import matplotlib.pyplot as plt
import matplotlib as mpl
import SimpleITK as sitk
import numpy as np
import pandas as pd
import datetime
import os
import glob
import gzip
import shutil
import xlsxwriter
import time
from scipy.stats.stats import pearsonr
import dicom2nifti
from multiprocessing.pool import ThreadPool
from functools import partial
from ImageAnalysisFunctions import *

#%% Set Working directory
        
data_supradir = 'path to supradirectory containing individual patients directories' #Set working directory

#Set path to seeds list excel file
seeds_file_path = data_supradir +'Seeds_list.xlsx'
seeds_dfs = pd.read_excel(seeds_file_path, sheet_name=None, index_col='Patient ID')
n_sheets = len(seeds_dfs)

subjs_path = [ f.path for f in os.scandir(data_supradir) if f.is_dir() ] #Create a list of the paths to the subjects directories
subjs_name = [ f.name for f in os.scandir(data_supradir) if f.is_dir() ] #Create a lisdt of subjects names

n_subj = len(subjs_name) #Total number of subjects

#Generate excel file containing voxelwise results
Results = pd.ExcelWriter(data_supradir +'Results_CS.xlsx')


#Create empty dataframes to populate as going through the loop
d={}
for repeat in range(1, n_sheets+1):
    d[repeat] = pd.DataFrame(columns=['Subject_ID', 'BTV Volume [mm3]', 'BTV Mean intensity [SUV]', 'BTV Std of Mean [SUV]', 'CTRL VOI Volume [mm3]', 'CTRL VOI Mean intensity [SUV]', 'CTRL VOI Std of Mean [SUV]', 'BTV TBR Mean', 'BTV TBR Std of Mean'])
    


#%%Create a for loop to perform image analysis on each subject sequentially

for current in subjs_name:
    subj_dir = data_supradir+current
    subj_name = current
    
    #Unzip all nii.gz files and delete original gzipped files
    for filename in glob.glob(subj_dir +'/' +'*.gz'):
        gunzip_shutil(filename, filename[:-3])
    
    # # #Rename all the image files in format "subjectName_scanType.nii"
    # # rename_img_files(subj_dir, subj_name)
    
   
    # #Perform brain extraction on PET image
    # print('Perform brain extraction on PET image for '+subj_name)
    # PET_FET = sitk.ReadImage(subj_dir +'/'+ subj_name +'_PET_FET_inFETCT.nii', sitk.sitkFloat32) #read PET FET image
    # brain_mask = sitk.ReadImage(subj_dir +'/brain_mask.nii') #read brain mask
    
    # brain_mask_filled = sitk.BinaryMorphologicalClosing(brain_mask, (1,1,1), sitk.sitkBall, 1.0) #fill holes in brain mask
    # # sitk.WriteImage(brain_mask_filled, subj_dir +'/brain_mask_filled.nii') #save filled mask
    
    # brain_mask_cleaned = sitk.BinaryMorphologicalOpening(brain_mask_filled, (1,1,1), sitk.sitkBall, 0.0, 1.0) #remove small structures in brain mask filled
    # # sitk.WriteImage(brain_mask_cleaned, subj_dir +'/brain_mask_cleaned.nii') #save cleaned mask
    
    # # brain_mask_cleaned = sitk.ReadImage(subj_dir +'/brain_mask_cleaned.nii')
    
    # PET_FET_bet = generate_mask(PET_FET, brain_mask_cleaned)
    # sitk.WriteImage(PET_FET_bet, subj_dir +'/' + subj_name + '_PET_FET_bet.nii')
    PET_FET_bet = sitk.ReadImage(subj_dir +'/' + subj_name + '_PET_FET_bet.nii')
    
    # # Apply transformations to re-align KF006 and GF002 imageS to axes
    # if current == 'KF006':
    #     print('Apply transformations to re-align KF006 image to axes')
    #     PET_FET_bet_rot = rotation3d(PET_FET_bet, theta_z=6, show=False) #Rotate KF006 PET image by 6 degrees anticlockwise around z axis
    #     PET_FET_bet_transl = affine_translate(PET_FET_bet_rot, 3, x_translation=-9.0, y_translation=0.0, z_translation=0.0)
    #     sitk.WriteImage(PET_FET_bet_transl, subj_dir +'/' + subj_name + '_PET_FET_bet.nii')
    #     PET_FET_bet = sitk.ReadImage(subj_dir +'/' + subj_name + '_PET_FET_bet.nii')
        
    # elif current == 'GF002':
    #     print('Apply transformations to re-align GF002 image to axes')
    #     PET_FET_bet_rot = rotation3d(PET_FET_bet, theta_z=5, show=False) #Rotate KF006 PET image by 5 degrees anticlockwise around z axis
    #     PET_FET_bet_transl = affine_translate(PET_FET_bet_rot, 3, x_translation=4.0, y_translation=0.0, z_translation=0.0)
    #     sitk.WriteImage(PET_FET_bet_transl, subj_dir +'/' + subj_name + '_PET_FET_bet.nii')
    #     PET_FET_bet = sitk.ReadImage(subj_dir +'/' + subj_name + '_PET_FET_bet.nii')
        
    # elif current == 'FF004':
    #     print('Apply transformations to re-align FF004 image to axes')
    #     PET_FET_bet_rot = rotation3d(PET_FET_bet, theta_z=-3, show=False) #Rotate FF004 PET image by 6 degrees anticlockwise around z axis
    #     PET_FET_bet_transl = affine_translate(PET_FET_bet_rot, 3, x_translation=0.0, y_translation=0.0, z_translation=0.0)
    #     sitk.WriteImage(PET_FET_bet_transl, subj_dir +'/' + subj_name + '_PET_FET_bet.nii')
    #     PET_FET_bet = sitk.ReadImage(subj_dir +'/' + subj_name + '_PET_FET_bet.nii')
        
    # elif current == 'AB001':
    #     print('Apply transformations to re-align AB001 image to axes')
    #     PET_FET_bet_rot = rotation3d(PET_FET_bet, theta_z=3, show=False) #Rotate AB001 PET image by 3 degrees anticlockwise around z axis
    #     PET_FET_bet_transl = affine_translate(PET_FET_bet_rot, 3, x_translation=-3.0, y_translation=10.0, z_translation=0.0)
    #     sitk.WriteImage(PET_FET_bet_transl, subj_dir +'/' + subj_name + '_PET_FET_bet.nii')
    #     PET_FET_bet = sitk.ReadImage(subj_dir +'/' + subj_name + '_PET_FET_bet.nii')
        
    
    #Create empty Dictionary with results of stats to populate as going through the loop
    Results_dict = {}
    
    
    
    for e in range(1, n_sheets+1):
        
        seeds_df = seeds_dfs.get('Sheet'+str(e))
    
        print('Start automated segmentation number '+str(e)+' for '+subj_name)
        
        start = time.time()
        
        # Generate subfolder for a repeat in subj_dir    
        os.mkdir(subj_dir +'/Repeat_'+str(e))
        
        #Set paths to the repeat folder   
        repeat_dir = subj_dir +'/Repeat_'+str(e)
        
        #Move CTRL_VOI file in respective Repeat folder
        for file in glob.glob(subj_dir +'/CTRL_VOI'+str(e)+'.nii'):
            shutil.move(os.path.join(subj_dir, file), repeat_dir)
        
        
        #Read CS CTRL VOI
        CTRL_VOI = sitk.ReadImage(repeat_dir +'/CTRL_VOI'+str(e)+'.nii') #read CTRL VOI
     
        #Calculate CTRL VOI mean value of SUV
        CTRL_VOI_stats = getStatsRoi(CTRL_VOI, PET_FET_bet)
        CTRL_VOI_MeanSUV = CTRL_VOI_stats.get('Mean intensity [SUV]')
        CTRL_VOI_Volume = int(CTRL_VOI_stats.get('Volume [mm3]'))
                
        #Generate PET FET TBR map    
        PET_FET_TBR_map = PET_FET_bet/CTRL_VOI_MeanSUV
        sitk.WriteImage(PET_FET_TBR_map, subj_dir +'/PET_FET_TBR_map.nii')     
        # PET_FET_TBR_map = sitk.ReadImage(subj_dir +'/PET_FET_TBR_map.nii')
        
        #Get seed from excel file
        subj_seeds = seeds_df.loc[subj_name].values
        
        #Determine how many seeds are there 
        n_seeds = int(np.count_nonzero(~np.isnan(subj_seeds))/3)
        
        if n_seeds != 1:
            print(str(n_seeds) +' seeds found')
    
        elif n_seeds == 1:     
            print('Only one seed found')
            
        for i in range(0, n_seeds):
            seed = (int(subj_seeds[3*i]), int(subj_seeds[3*i+1]), int(subj_seeds[3*i+2]))
        
            #Generate BTV based on TBR>1.9
            BTV = sitk.ConnectedThreshold(PET_FET_TBR_map, seedList=[seed], lower=1.9, upper=50) #Region growing VOI from the seed with connected component method
            BTV = sitk.BinaryMorphologicalClosing(BTV, (1,1,1), sitk.sitkBall, 1.0) #fill holes in VOI
            BTV = sitk.BinaryMorphologicalOpening(BTV, (1,1,1), sitk.sitkBall, 0.0, 1.0) #remove small structures in VOI
            
            
            maxBTV = getMaxVox(BTV)[0]
            if maxBTV > 0.0:
                sitk.WriteImage(BTV, repeat_dir +'/' + subj_name + '_BTV'+str(i)+'.nii')
                print('BTV exists: found a tumour lesion for seed '+ str(i))                
                             
            else:
                print('BTV doesnt exist: did NOT found a tumour lesion for seed '+ str(i))
        
        end = time.time()
        print('Time elapsed for segmentation number '+str(e)+' for '+subj_name+' is (sec): '+ str(end - start))
        
        n_lesions = len(glob.glob(repeat_dir+'/'+'*BTV*'))        
        
        if n_lesions == 0:
            print('No lesion found for Repeat '+str(e))
            
        elif n_lesions == 1:
            for filename in glob.glob(repeat_dir+'/'+'*0.nii'):
                os.rename(filename, filename.replace(filename[-5:], '.nii'))
            
        else:
            
            CTRL = sitk.ReadImage(repeat_dir +'/CTRL_VOI'+str(e)+'.nii')
            CTRL_dim = CTRL.GetSize()
            BTV = sitk.Image(CTRL_dim, sitk.sitkUInt8)
            BTV.CopyInformation(CTRL)
               
            for filename in glob.glob(repeat_dir+'/'+'*BTV*'):
                img = sitk.ReadImage(filename)
                BTV = BTV+img 
            
            BTV = sitk.BinaryThreshold(BTV, 1, n_seeds*2, 1, 0)
            sitk.WriteImage(BTV, repeat_dir +'/' + subj_name + '_BTV.nii')
            
            
        CTRL_VOI = sitk.ReadImage(repeat_dir +'/CTRL_VOI'+str(e)+'.nii')
        PET_FET_TBR_map = sitk.ReadImage(subj_dir +'/PET_FET_TBR_map.nii')
            
           
        #Calculate CTRL VOI stats
        CTRL_VOI_stats = getStatsRoi(CTRL_VOI, PET_FET_bet) #Calculate new CTRL_VOI stats
        CTRL_VOI_MeanSUV = CTRL_VOI_stats.get('Mean intensity [SUV]') #Calculate CTRL_VOI mean value of SUV
        CTRL_VOI_StdSUV = CTRL_VOI_stats.get('Std of Mean [SUV]') #Calculate CTRL_VOI Std value of mean SUV
        CTRL_VOI_volume = int(CTRL_VOI_stats.get('Volume [mm3]')) #Calculate CTRL_VOI volume in mm3
            
        if os.path.isfile(repeat_dir +'/' + subj_name + '_BTV.nii'):    
            BTV = sitk.ReadImage(repeat_dir +'/' + subj_name + '_BTV.nii')

            #Calculate BTV stats
            BTV_stats = getStatsRoi(BTV, PET_FET_bet) #Calculate new BTV stats
            BTV_MeanSUV = BTV_stats.get('Mean intensity [SUV]') #Calculate BTV mean value of SUV
            BTV_StdSUV = BTV_stats.get('Std of Mean [SUV]') #Calculate BTV Std value of mean SUV
            BTV_volume = int(BTV_stats.get('Volume [mm3]')) #Calculate BTV volume in mm3
        
            #Calculate BTV TBR stats
            BTV_TBR_stats = getStatsRoi(BTV, PET_FET_TBR_map)
            BTV_MeanTBR = BTV_TBR_stats.get('Mean intensity [SUV]') #Calculate BTV TBR mean value
            BTV_StdTBR = BTV_TBR_stats.get('Std of Mean [SUV]') #Calculate BTV Std value of mean TBR
                
        else:
                
            BTV_MeanSUV = float("NaN")
            BTV_StdSUV = float("NaN")
            BTV_volume = float("NaN")
            BTV_MeanTBR = float("NaN")
            BTV_StdTBR = float("NaN")
                
            
        #Save statistics of various VOIs
            
        sheet_df = {'Subject_ID': subj_name, 'BTV Volume [mm3]': BTV_volume, 'BTV Mean intensity [SUV]': BTV_MeanSUV, 'BTV Std of Mean [SUV]': BTV_StdSUV, 'CTRL VOI Volume [mm3]': CTRL_VOI_volume, 'CTRL VOI Mean intensity [SUV]': CTRL_VOI_MeanSUV, 'CTRL VOI Std of Mean [SUV]': CTRL_VOI_StdSUV, 'BTV TBR Mean': BTV_MeanTBR, 'BTV TBR Std of Mean': BTV_StdTBR}
        Results_dict[e] = pd.DataFrame(sheet_df, index=[0], columns=['Subject_ID', 'BTV Volume [mm3]', 'BTV Mean intensity [SUV]', 'BTV Std of Mean [SUV]', 'CTRL VOI Volume [mm3]', 'CTRL VOI Mean intensity [SUV]', 'CTRL VOI Std of Mean [SUV]', 'BTV TBR Mean', 'BTV TBR Std of Mean']) 
        d[e] = d[e].append(Results_dict[e], ignore_index=True)
            

for df_name, df in d.items():
    df.to_excel(Results, sheet_name='Repeat'+str(df_name), index=False)

Results.save()
