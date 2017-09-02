# Alec Myres
# August 2017
# Aggregate and clean Redfin data downloads

import sys, os
import pandas as pd
import numpy as np
import datetime as dt

files = os.listdir('redfin-data/')

# Read/build data frame
results = pd.DataFrame()
for f in files:
    r = pd.read_csv('redfin-data/' + f)
    results = pd.concat([results, r])

# Clean up data frame
results.reset_index(drop = True, inplace = True)
results.drop_duplicates(inplace = True)
results = results[['SOLD DATE','PROPERTY TYPE','MLS#',
                   'ADDRESS','CITY','STATE','ZIP',
                   'PRICE','BEDS','BATHS','SQUARE FEET',
                   'LOT SIZE','YEAR BUILT','DAYS ON MARKET',
                   'HOA/MONTH','LATITUDE','LONGITUDE']]
new_cols = {'SOLD DATE'      : 'SOLD',
            'PROPERTY TYPE'  : 'TYPE',
            'SQUARE FEET'    : 'SQFT',
            'LOT SIZE'       : 'LTSZ',
            'YEAR BUILT'     : 'YEAR',
            'DAYS ON MARKET' : 'DMKT',
            'HOA/MONTH'      : 'HOA'}
results.rename(columns = new_cols, inplace = True)

# Save results
results.to_csv('combined_results.csv')         
