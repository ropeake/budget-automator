# -*- coding: utf-8 -*-
"""
Created on Sat Jan 20 14:18:07 2018

@author: Ro
"""

import pandas as pd
import win32ui
import win32con
o=win32ui.CreateFileDialog(1)
if o.DoModal()==1:
    filename=o.GetPathName()
#%%
    df=pd.read_csv(filename,skiprows=5,header=0,
                   names=['transaction_date','posted_date','type','description','b1','credit','debit','balance','b2','b3'],
                   )
    df.transaction_date=df.description.str.split(' ON ',expand=True)[1]
    df.loc[pd.isnull(df.transaction_date),'transaction_date']=df.loc[pd.isnull(df.transaction_date),'posted_date']
    df['sort_code']="'09-01-28"
    df['ac_number']=95349265
    df=df[['transaction_date','posted_date','sort_code','ac_number','type','description','credit','debit','balance']]
    df.to_clipboard(excel=True,index=False,header=False)
#%%   

#here's my new code to find duplicates but it's shit and broken
    win32ui.MessageBox('Success! Paste away!','Transaction Formatter 2000')
else:
    win32ui.MessageBox('Well ok then, bye I guess','Transaction Formatter 2000',win32con.MB_ICONSTOP)
