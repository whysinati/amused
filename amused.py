#Read a JSON file into Python/Pandas
#Original dataset for IoT gadget providing sensor data
#Here's my partial solution, which leave the timestamps, samples and channel names as lists within cells. I'm betting I can extract those further, but wanted to share the interim in case you had thoughts. This could also be expanded to put the "metadata" and the "annotations" in separate dataframes.

import json
import pandas as pd
import numpy as np

fname = 'Muse-85D0_2018-06-12--13-11-39_1528830859605.json'
fhand = open(fname) #open the file and save the handle into a variable
data = fhand.read() #read into the 'data' variable
js = json.loads(data) #read the 'data' into a format that python can process (using the import JSON library)
# print(json.dumps(js, indent=4)) # DEBUGGER print the list

lev0 = [] #becomes a list of the top level item names
for lst in js:
    lev0.append(lst)

museList  = js[lev0[0]] #creates a sub list of the first top level item ("timeseries")
table = [] #becomes nested lists

good_columns = [
    "name",
    "fs",
    "emp_fs",
    "timestamps",
    "samples",
    "channel_names"
    ]

for itm in museList:    #extract the rows as lists within a list
    museName = museList[itm]["name"]
    muse_fs = museList[itm]["fs"]
    muse_emp_fs = museList[itm]["emp_fs"]
    muse_tmstp = museList[itm]["timestamps"]
    muse_smpl = museList[itm]["samples"]
    muse_ch_nm = museList[itm]["channel_names"]
    table.append([museName, muse_fs, muse_emp_fs, muse_tmstp, muse_smpl, muse_ch_nm])
m_df = pd.DataFrame(table, columns=good_columns) #create the dataframe
