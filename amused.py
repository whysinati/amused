'''This script imports a JSON file of nested dictionaries and lists
containing IoT Muse activity data, formats the data into rows,
and generates a pandas dataframe for further analysis. '''
# coding: utf-8

# In[1]:

import json
#import numpy as np #not used in this code
import pandas as pd



FNAME = 'Muse-85D0_2018-06-12--13-11-39_1528830859605.json'
FHAND = open(FNAME) #open the file and save the handle into a variable
DATA = FHAND.read() #read into the 'data' variable
JS = json.loads(DATA) #read the 'data' into a format that python can process

LEV0 = []            #['timeseries', 'annotations', 'meta_data']
for lst in JS:
    LEV0.append(lst)

MUSE_LIST = JS[LEV0[0]] #dictionary under 'timeseries' {'eeg': {'name': 'eeg',

LEV1 = []            #[list of names under the 'timeseries']
for lst_2 in MUSE_LIST:
    LEV1.append(lst_2)

MUSE_LIST2 = JS[LEV0[0]][LEV1[0]] #dictionary under 'timeseries'/device

LEV2 = []            #['name', 'fs', 'emp_fs', 'timestamps', 'samples', 'channel_names']
for lst_3 in MUSE_LIST2:
    LEV2.append(lst_3)

ROWS = []            # append list of items as ROWS to create dataframe

for device in MUSE_LIST:
    museName = MUSE_LIST[device][LEV2[0]]       #MUSE_LIST[device]['name'] #js['timeseries']['name']
    muse_fs = MUSE_LIST[device][LEV2[1]]        #['fs']
    muse_emp_fs = MUSE_LIST[device][LEV2[2]]    #['emp_fs']
    for ts, smps in zip(MUSE_LIST[device][LEV2[3]], MUSE_LIST[device][LEV2[4]]):
#['timestamps']#['samples']
        muse_tmstp = ts                        #unpack list of ['timestamps']
        for sm, cn in zip(smps, MUSE_LIST[device][LEV2[5]]): #['channel_names']
            muse_smpl = sm             #unpack list of ['samples'] or MUSE_LIST[device][LEV2[4]]
            muse_ch_nm = cn            #unpack list of ['channel_names']
            ROWS.append([museName, muse_fs, muse_emp_fs, muse_tmstp, muse_smpl, muse_ch_nm])
M_DF = pd.DataFrame(ROWS, columns=LEV2)        #create dataframe from ROWS
M_DF['timestamps'] = pd.to_datetime(M_DF['timestamps'], unit='s') #format the timestamps as datetime
M_DF = M_DF.set_index(['name', 'fs', 'emp_fs', 'timestamps', 'samples']) #set multiIndex
