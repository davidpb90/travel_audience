#! /Users/DavidPardo/anaconda/bin/python
# Change to apprpiate local python location e.g. #! /usr/bin/python
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import sys
import csv
  
input_file = open(sys.argv[1], 'rb')
data = pd.read_csv(input_file)
data.ts = pd.to_datetime(data.ts)
data['date'] = data.ts.map(pd.Timestamp.date)
data['weekday'] = data.date.map(pd.Timestamp.weekday)
data['hour'] = data.ts.dt.hour
data['is_business_time'] = np.logical_and(data.hour>=8,np.logical_and(data.weekday<=4,data.hour<20))
data['counts'] = 0
data['min_date'] = data['ts']
data['max_date'] = data['ts']
freqs = data.groupby('uuid', as_index=False, sort=False).agg({
                                                        'date' : lambda s: s.nunique(), 
                                                        'useragent' : lambda s: s.nunique(), 
                                                        'hashed_ip' : lambda s: s.nunique(),
                                                        'is_business_time' : np.sum,
                                                        'counts' : 'count',
                                                        'min_date' : 'min',
                                                        'max_date' : 'max'})
freqs['ratio_business'] = freqs['is_business_time']/freqs['counts']
freqs.loc[freqs.counts == 1, 'average_time_btw_events'] = 0
freqs.loc[freqs.counts > 1, 'average_time_btw_events'] = ((freqs.max_date-freqs.min_date).astype('timedelta64[h]')/(freqs.counts-1)).round(0)
freqs['highly_active'] = freqs['counts'] > 3
freqs['multiple_days'] = freqs['date'] > 1
freqs['weekday_biz'] = freqs['ratio_business'] > 0.5
freqs['average_days_btw_events'] = freqs.average_time_btw_events/24
final = freqs[['uuid','highly_active','multiple_days','weekday_biz','average_days_btw_events']]
print(final.to_string())