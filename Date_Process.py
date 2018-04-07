# -*- coding: utf-8 -*-
"""
Created on Sat Jan 20 14:18:07 2018

@author: Ro
"""

import pandas as pd
import win32ui
import win32con
import os.path
o=win32ui.CreateFileDialog(1)
if o.DoModal()==1:
    selected_path=o.GetPathName()
    #renamed from filename for clarity
    
#%%
    folder_name=os.path.dirname(selected_path)
    list_of_files=os.listdir(folder_name)
    selected_file=os.path.basename(selected_path)    
    sf_index=list_of_files.index(selected_file)
    previous_file=list_of_files[sf_index-1]
    previous_path=os.path.join(folder_name,previous_file)
#%%
def open_and_column_fix(csv_path):
    df=pd.read_csv(csv_path,skiprows=5,header=0,
                   names=['transaction_date','posted_date','type','description','b1','credit','debit','balance','b2','b3'],
                   )
    df.transaction_date=df.description.str.split(' ON ',expand=True)[1]
    df.loc[pd.isnull(df.transaction_date),'transaction_date']=df.loc[pd.isnull(df.transaction_date),'posted_date']
    df['sort_code']="'09-01-28"
    df['ac_number']=95349265
    df=df[['transaction_date','posted_date','sort_code','ac_number','type','description','credit','debit','balance']]
    return df

#   df.to_clipboard(excel=True,index=False,header=False)
#here's my new code to find duplicates but it's shit and broken    
    
#%%   
    df_now=open_and_column_fix(selected_path)
    df_old=open_and_column_fix(previous_path)
    df=pd.concat([df_now, df_old])
    df=df.drop_duplicates(keep='first')
    len(df)
    
#%%
    win32ui.MessageBox('Success! Paste away!','Transaction Formatter 2000')
else:
    win32ui.MessageBox('Bye bye','Transaction Formatter 2000',win32con.MB_ICONSTOP)
