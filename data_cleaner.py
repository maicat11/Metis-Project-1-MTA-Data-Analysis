import pandas as pd
import numpy as np

def read_mta_file(path):
    """Read the raw MTA turnstyle data and return a dataframe cleaned up as follows -
       * Dates between 04/01/2018 and 06/22/2018
       * Column names stripped
       * Column Date and Time combined into one column called date_time and 
         of the proper Numpy datetime type
       * Turnstile ID created from Unit + SCP
       * New column 'weekday' indicates whether data is from a weekday (monday-friday)
    """
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
    spring['weekday'] = spring.date_time.dt.weekday < 5
    
    spring = spring.drop(columns=['Date', 'Time', 'Division', 'Line Name'])    
    return spring
