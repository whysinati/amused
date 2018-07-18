#Read a JSON file into Python/Pandas
#Original dataset for IoT gadget providing sensor data
#Here's my partial solution, which leave the timestamps, samples and channel names as lists within cells. I'm betting I can extract those further, but wanted to share the interim in case you had thoughts. This could also be expanded to put the "metadata" and the "annotations" in separate dataframes.

# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import json

fname = 'Muse-85D0_2018-06-12--13-11-39_1528830859605.json'
fhand = open(fname) #open the file and save the handle into a variable
data = fhand.read() #read into the 'data' variable
js = json.loads(data) #read the 'data' into a format that python can process (using the import JSON library)

lev0 = []            #['timeseries', 'annotations', 'meta_data']
for lst in js:
    lev0.append(lst)

museList  = js[lev0[0]] #dictionary under 'timeseries' {'eeg': {'name': 'eeg', 'fs': 256.0, 'emp_fs': 256.0, 'timestamps': [1528830699.4576273, 1528830699.4615335,

lev1 = []            #[list of names under the 'timeseries']
for lst_2 in museList:
    lev1.append(lst_2)

museList2 = js[lev0[0]][lev1[0]] #dictionary under 'timeseries'/device {'name': 'eeg', 'fs': 256.0, 'emp_fs': 256.0, 'timestamps': [1528830699.4576273, 

lev2 = []            #['name', 'fs', 'emp_fs', 'timestamps', 'samples', 'channel_names']
for lst_3 in museList2:
    lev2.append(lst_3)

rows = []            # append list of items as rows to create dataframe

for device in museList:    
    museName = museList[device][lev2[0]]       #museList[device]['name'] #js['timeseries']['name']
    muse_fs = museList[device][lev2[1]]        #['fs']
    muse_emp_fs = museList[device][lev2[2]]    #['emp_fs']
    for ts, smps in zip(museList[device][lev2[3]], museList[device][lev2[4]]): #['timestamps']#['samples']
        muse_tmstp = ts                        #unpack list of ['timestamps']
        for sm, cn in zip(smps, museList[device][lev2[5]]): #['channel_names']
            muse_smpl = sm                     #unpack list of ['samples'] or museList[device][lev2[4]] 
            muse_ch_nm = cn                    #unpack list of ['channel_names']
            rows.append([museName, muse_fs, muse_emp_fs, muse_tmstp, muse_smpl, muse_ch_nm])        
m_df = pd.DataFrame(rows, columns=lev2)        #create dataframe from rows
m_df['timestamps'] = pd.to_datetime(m_df['timestamps'], unit='s') #format the timestamps as datetime
m_df = m_df.set_index(['name', 'fs', 'emp_fs', 'timestamps', 'samples']) #set multiIndex

m_df
