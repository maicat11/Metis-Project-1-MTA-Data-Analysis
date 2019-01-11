import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def get_color(station):
    '''A color dictionary that returns a chosen color 
    corresponding to the station called station. 
    '''

    color_scheme = {'23 ST': 'crimson',
                    '14 ST': 'maroon',
                    '14 ST-UNION SQ': 'plum',
                    'LEXINGTON AV/63': 'gold',
                    '53 ST': 'orange',
                    'BEDFORD AV': 'silver',
                    '7 AV': 'yellow',
                    '57 ST': 'azure',
                    'GRD CNTRL-42 ST': 'black',
                    '8 ST-NYU': 'red',
                    'W 4 ST-WASH SQ': 'navy',
                    '51 ST': 'sienna',
                    'WALL ST': 'salmon',
                    'BROAD ST': 'aqua',
                    'CHAMBERS ST': 'blue',
                    '18 ST': 'olive',
                    'HOUSTON ST': 'indigo',
                    '28 ST': 'coral',
                    'FULTON ST': 'darkgreen',
                    '34 ST-PENN STA': 'green',
                    'ASTOR PL': 'lightblue',
                    '42 ST-BRYANT PK': 'lime',
                    '9TH STREET': 'pink',
                    '5 AVE': 'lightblue'}
    return color_scheme[station]


def pretty_station(station):
    '''A dictionary that returns the station name prettified 
    for simplistic printing/labeling.
    '''
    station_titles = {'23 ST': '23rd Street',
                      '14 ST': '14th Street',
                      '14 ST-UNION SQ': '14th Street-Union Square',
                      'LEXINGTON AV/63': 'Lexington Ave/63rd Street',
                      '53 ST': '53rd Street',
                      'BEDFORD AV': 'Bedford Ave',
                      '7 AV': '7th Ave',
                      '57 ST': '57th Street',
                      'GRD CNTRL-42 ST': 'Grand Central Station',
                      '8 ST-NYU': '8th Street-NYU',
                      'W 4 ST-WASH SQ': 'West 4th Street-Washington Square',
                      '51 ST': '51st Street',
                      'WALL ST': 'Wall Street',
                      'BROAD ST': 'Broad Street',
                      'CHAMBERS ST': 'Chambers Street',
                      '18 ST': '18th Street',
                      'HOUSTON ST': 'Houston Street',
                      '28 ST': '28th Street',
                      'FULTON ST': 'Fulton Street',
                      '34 ST-PENN STA': '34th Street-Penn Station',
                      'ASTOR PL': 'Astor Place',
                      '42 ST-BRYANT PK': '42nd Street-Bryant Park',
                      '9TH STREET': '9th Street',
                      '5 AVE': '5th Ave'}
    return station_titles[station]


def graph_entries(df):
    '''Graph all the target stations on total entries for each day.'''
    
    target_stations = pd.read_csv("station_targets.csv")
    target_stations = target_stations.Station.str.upper()

    plt.figure(figsize=(18,10))

    for station in target_stations:
        station_agg = df[(df['Station'] == station)][['date_time','entry_delta']].set_index('date_time')
        station_resample = station_agg.resample('D').sum()  
        plt.plot(station_resample, c = get_color(station), label = station);

    plt.title('Entries Per Day by Stations', size=25)
    plt.xlabel('Days', size=15)
    plt.ylabel('Entries', size=15)
    plt.legend(loc='right');


def heatmap_entries(df, station=None):
    '''Graph a heatmap of the day of week per week'''
    
    all_entries = df[['date_time','entry_delta']].set_index('date_time')   
    daily_entries = all_entries.resample('D').sum()
    new_val1 = pd.DataFrame({'entry_delta': np.nan}, index=pd.to_datetime(['2018-06-22']))
    new_val2 = pd.DataFrame({'entry_delta': np.nan}, index=pd.to_datetime(['2018-06-23']))
    daily_entries = daily_entries.append(new_val1)
    daily_entries = daily_entries.append(new_val2) 

    data_by_week_dict = {}
    i = 0
    for k, j in enumerate(range(7, len(daily_entries)+7, 7)):
        data_by_week_dict[f'Week{k+1}'] = list(daily_entries[i:j]['entry_delta'])
        i = j

    days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    data_by_week = pd.DataFrame(data_by_week_dict, index = days)
    
    fig, ax = plt.subplots(figsize=(15,4))
    sns.heatmap(data_by_week, ax=ax, cmap='Reds', linewidths=1, linecolor='ivory');
   
    
    if station:
        plt.title(pretty_station(station), size = 25)
    else:
        plt.title('Total Entries Per Day Each Week', size = 25)

        
