# -*- coding: utf-8 -*-
"""
Created on Sat Jan 20 14:18:07 2018
#Changelog bug fixes and performance improvements
@author: Ro
"""



import pandas as pd
import win32ui
import win32con
import os.path
import budgetML
#%% Creating a function to import the csv and re-order the columns
def open_and_column_fix(csv_path):
    df=pd.read_csv(csv_path, encoding='latin', quotechar='"', skiprows=4,header=0,
                   names=['transaction_date','posted_date','type','description','b1','credit','debit','balance','b2','b3'],
                   )
    df.transaction_date=df.description.str.split(' ON ',expand=True)[1] #split and then return column 1 (firts column is 0)
    df.loc[pd.isnull(df.transaction_date),'transaction_date']=df.loc[pd.isnull(df.transaction_date),'posted_date']
    df['sort_code']="'09-01-28"
    df['ac_number']=95349265
    df=df[['transaction_date','posted_date','sort_code','ac_number','type','description','credit','debit','balance']]
    df=df[~pd.isnull(df.balance)]
    return df
#%% launches dialouge box to select file
o=win32ui.CreateFileDialog(1)  
if o.DoModal()==1: # if you click a file, and then ok
    selected_path=o.GetPathName() # def variable - the full path and filename of the selected file
    #renamed from filename for clarity
    
#%% Defines variables for current and previous files with and without full path
    folder_name=os.path.dirname(selected_path) 
    list_of_files=os.listdir(folder_name) 
    selected_file=os.path.basename(selected_path) 
    sf_index=list_of_files.index(selected_file) 
    previous_file=list_of_files[sf_index-1] 
    previous_path=os.path.join(folder_name,previous_file) 

#%% Concatination approach 
    df_current=open_and_column_fix(selected_path)
    df_previous=open_and_column_fix(previous_path)
    df=pd.concat([df_current, df_previous,df_previous])
    print(len(df))
    df=df.drop_duplicates(keep=False)
    print(len(df))
    
 
#%% Importing eirinn's machine learning code
    data=pd.read_excel(r"C:\Users\Ro\OneDrive\Budgets\2018 Budget.xlsx",sheet_name='London Data')
    budgetML.add_training_data(data)
    df_predicted=budgetML.build_and_predict(df)   

#%% copy to clipboard    
    df_predicted.to_clipboard(excel=True,index=False,header=False,sep='\t')
    status=f"{len(df_current)-len(df)} duplicates removed"
# here's my new code to find duplicates but it's shit and broken    


#%%
    win32ui.MessageBox(f"Success! {status}, remaining transactions pasted to clipboard",'Transaction Formatter 2000')
else:
    win32ui.MessageBox('Bye bye','Transaction Formatter 2000',win32con.MB_ICONSTOP)





    
    
#%% Remove dupliactes using isin
#    df_current=open_and_column_fix(selected_path)
#    df_previous=open_and_column_fix(previous_path)  
#    df_current.set_diff(df_previous) 