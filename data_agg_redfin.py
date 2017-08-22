# Alec Myres
# August 2017
# Aggregate and clean Redfin data downloads

import sys, os
import pandas as pd
import numpy as np

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

# Save results
results.to_csv('combined_results.csv')

# TODO:
# Data summary
# Distribution of variables
# Split train/test
# - Time ordered? (last obs as test set)
# Basic models:
# - Guess avg.
# - Linear on size
# - Linear on size + lot
# - Decision Trees/forest
# - Other monotonic/isotonic techniques
