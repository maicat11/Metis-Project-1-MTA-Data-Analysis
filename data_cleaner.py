import pandas as pd
import numpy as np

def read_mta_file(path):
    raw_data = pd.read_csv(path)
    
    # trim by date first so that it's easier to hack on
    our_rows = raw_data[(raw_data.Date >= '04/01/2018') & 
                     (raw_data.Date < '06/22/2018')]
    spring = our_rows.copy()
    
    assert(spring.shape[0] == 2307938)
    
    # strip the Exists column name
    spring.columns = spring.columns.str.strip()
    
    # make turnstile ids
    spring['ts_id'] = spring.Unit + '_' + spring.SCP
        
    spring['date_time'] = pd.to_datetime(spring.Date + ' ' + spring.Time, format="%m/%d/%Y %X")
     
    spring = spring.drop(columns=['Date', 'Time', 'Division', 'Line Name'])    
    return spring
