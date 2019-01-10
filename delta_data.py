import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from data_cleaner import read_mta_file


# used for rolling deltas of entry and exit counters
def rolling_delta(window):
    """This is an internal function, do not import or call"""
    if window.size != 2:
        raise Exception("Something is wrong!")
        
    delta = window[1] - window[0]
    if delta < 0:
        delta = np.nan
    return delta

# used for people per hour column
def get_hours(x):
    """This is an internal function, do not import or call"""
    seconds = x.seconds
    hours = seconds/3600
    return hours


def read_delta_data(path, pickle_ok=True):
    """This function replaces read_mta_file to get the data with 
    deltas calculated"""

    if pickle_ok:
        try:
            data = pd.read_pickle("delta.pickle")
            return data
        except:
            pass

    data = read_mta_file(path, pickle_ok=pickle_ok)

    # We cannot roll before we sort! 
    # Sort first by station, then by turnstile, then by date
    data.sort_values(by=['C/A', 'ts_id', 'date_time'], inplace=True)


    exit_deltas = pd.Series()
    entry_deltas = pd.Series()
    time_deltas = pd.Series()
    
    all_turnstiles = data.ts_id.unique()
    turnstile_groups = data.groupby('ts_id')
    
    for t in all_turnstiles:

        one_t = turnstile_groups.get_group(t)
        t_exit_deltas = one_t['Exits'].rolling(2).apply(rolling_delta, raw=True)
        t_entry_deltas = one_t['Entries'].rolling(2).apply(rolling_delta, raw=True)
        
        exit_deltas = exit_deltas.append(t_exit_deltas)
        entry_deltas = entry_deltas.append(t_entry_deltas)
        
        # generic rolling doesn't work with datetimes!!?? UGH!!!
        t_times = one_t['date_time']
        nrow = t_times.shape[0]
        
        t_times_prev = t_times.copy().reset_index()
        t_times_next = t_times.copy(deep=True).reset_index()
        
        # skootch the index of one series down one
        t_times_prev.index = range(1, nrow+1)
        
        t_times_next['time_deltas'] = t_times_next['date_time'] - t_times_prev['date_time']
        t_times_next.index = t_times_next['index']
        time_deltas = time_deltas.append(t_times_next.time_deltas)
        
        
    data['exit_deltas'] = exit_deltas
    data['entry_deltas'] = entry_deltas
    data['time_deltas'] = time_deltas
   
    # I was using hour of day as a bin for plots 
    data['hour'] = data.date_time.dt.hour
    data['people_ph'] = (data.eval('entry_deltas + exit_deltas') /
                     (data['time_deltas'].apply(get_hours)))
   
    data.to_pickle("delta.pickle")

    return data
