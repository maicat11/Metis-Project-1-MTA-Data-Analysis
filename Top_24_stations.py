
# coding: utf-8

# In[43]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from delta_data import read_delta_data

data = read_delta_data("./data/Turnstile_Usage_Data__2018.csv")


# In[44]:


target_stations = pd.read_csv("station_targets.csv")


# In[46]:



target_data = data[data.Station.isin(target_stations)]


# In[50]:


station_groups = target_data.groupby(['Station','hour'])
PPHPS = people_per_hour_per_station = station_groups.people_ph.sum().reset_index()

for t in target_stations:
    sta_data = PPHPS.query("Station == '{}'".format(t))
    plt.plot(sta_data.hour, sta_data.people_ph)
    plt.title(t)
    plt.show()
        


# In[42]:




