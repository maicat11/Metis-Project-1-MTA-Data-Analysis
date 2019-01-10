import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from data_cleaner import read_mta_file


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

    # drop time intervals that are too small (3 minutes or less, based on inspection)
    too_small = pd.Timedelta(minutes=3)
    too_small_data = data[data.time_delta < too_small]
    data = data.drop(axis='index', labels=too_small_data.index)


    # NaN out time intervals that are too long (the bulk of the data wants to be 
    # plotted in four hour intervals. Averaging over 8 to 20 hours due to missing
    # data will not be helpful
    too_long = pd.Timedelta(hours=5, minutes=30)
    too_long_data = data[data.time_delta > too_long]
    data.loc[too_long_data.index, ['entry_delta', 'exit_delta']] = np.nan


    # I was using hour of day as a bin for plots 
    # some time periods end in :57 minutes --> round those to the next hour
    data['hour'] = data.date_time.dt.hour
    data.loc[data.date_time.dt.minute > 45, 'hour'] += 1
    data.loc[data.date_time.dt.hour == 24, 'hour'] = 0
    
    # Found my outliers by playing with the quantile function until the 
    # numbers were clearly bogus, then rounded up generously 
    # data.entry_delta.quantile(q=.00009)
    # data.entry_delta.quantile(q=.99995)
    bogus_entry = data.query('(entry_delta < -5000) or (entry_delta > 5000)')
    bogus_exit = data.query('(exit_delta < -5000) or (exit_delta > 5000)')

    data.loc[bogus_entry.index, 'entry_delta'] = np.nan
    data.loc[bogus_exit.index, 'exit_delta'] = np.nan

    # Some turnstiles count backwards
    neg_entry = data.query('entry_delta < 0')
    neg_exit = data.query('exit_delta < 0')

    data.loc[neg_entry.index, 
            'entry_delta'] = data.loc[neg_entry.index, 
                                        'entry_delta'].apply(np.abs)
    data.loc[neg_exit.index, 
            'exit_delta'] = data.loc[neg_exit.index, 
                                        'exit_delta'].apply(np.abs)

    # Finally, now that we trust the deltas a litte more, let's calculate people per 
    # hour for the remaining data
    data['people_ph'] = (data.eval('entry_delta + exit_delta') /
                     (data['time_delta'].apply(get_hours)))
   
    data.to_pickle("delta.pickle")

    return data
