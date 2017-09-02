# Alec Myres
# August 2017
# First pass at modeling sales data

import sys, os
import pandas as pd
import numpy as np
import datetime as dt
from sklearn.linear_model import LinearRegression
sys.path.append('/usr/local/lib/python2.7/site-packages')
import geopy.distance as gd

results = pd.read_csv('combined_results.csv', index_col = 0)

# Conversions and new variables
results['Sold'] = map(lambda x: dt.datetime.strptime(x, '%B-%d-%Y'), results['SOLD'])
results['HOA'].fillna(0, inplace = True)
results['YearSold'] = map(lambda x: int(x[-4:]), results['SOLD'])
results['Age'] = results['YearSold'] - results['YEAR']
results.query('Age >= -1', inplace = True)

# Build test/train framework
df = results.query('TYPE == "Single Family Residential"')
df = df[~df[['PRICE','SQFT','LTSZ','BEDS','BATHS']].isnull().any(axis = 1)]
dl = len(df.index)
df.sort_values('Sold', inplace = True)
df.reset_index(drop = True, inplace = True)

actual = []
model1 = []
model2 = []
model3 = []
model4 = []
test_dates = sorted(df['Sold'].unique())[-40:]
for d in test_dates:
    print d
    df['SaleAge'] = d - df['Sold']    
    df['SaleAge'] = map(lambda x: x.days, df['SaleAge'])
    df['tWgt'] = 1 - df['SaleAge'] / 1000.0
    train = df.query('Sold  < @d')
    test  = df.query('Sold == @d')
    actual += list(test['PRICE'])
    # Model 1
    ybar = train['PRICE'].mean()
    model1 += [ybar]*len(test.index)
    # Model 2
    m2 = LinearRegression()
    m2.fit(train[['SQFT']], train[['PRICE']])
    ypred = m2.predict(test[['SQFT']])
    model2 += list(ypred.ravel())
    # Model 3
    m3 = LinearRegression()
    m3.fit(train[['SQFT','LTSZ','HOA','BEDS']],train[['PRICE']])
    ypred = m3.predict(test[['SQFT','LTSZ','HOA','BEDS']])
    model3 += list(ypred.ravel())
    # Model 4
    for i in list(test.index):
        tgt_lat = test['LATITUDE'][i]
        tgt_lon = test['LONGITUDE'][i]
        c1 = (tgt_lat, tgt_lon)
        train['Dist'] = map(lambda x,y: gd.VincentyDistance(c1,(x,y)).miles,
                            train['LATITUDE'], train['LONGITUDE'])
        train['dWgt'] = 1/train['Dist']
        train['dWgt'] = np.where(train['dWgt'] > 25, 25, train['dWgt'])
        train['Wgt' ] = train['tWgt'] * train['dWgt']
        m4 = LinearRegression()
        m4_cols = ['SQFT','LTSZ','BEDS','BATHS','Age','HOA']
        m4.fit(train[m4_cols], train[['PRICE']], np.array(train['Wgt']))
        ypred = m4.predict(test[m4_cols].query('index == @i'))
        model4 += list(ypred.ravel())

# Predctions, errors
r = pd.DataFrame()
r['actual'] = actual
r['model1'] = model1
r['model2'] = model2
r['model3'] = model3
r['model4'] = model4
r['m1err' ] = r['model1'] - r['actual']
r['m2err' ] = r['model2'] - r['actual']
r['m3err' ] = r['model3'] - r['actual']
r['m4err' ] = r['model4'] - r['actual']
r['m1errp'] = r['m1err' ] / r['actual']
r['m2errp'] = r['m2err' ] / r['actual']
r['m3errp'] = r['m3err' ] / r['actual']
r['m4errp'] = r['m4err' ] / r['actual']

# Performance
percs = [50,75,90]
perf = pd.DataFrame()
for i in ['1','2','3','4']:
    sigs['Model' + i] = map(lambda x: np.percentile(r['m' + i + 'errp'].abs(), x), percs)

# TODO:
# Data summary
# Distribution of variables
# Add more data

# Models:
#  #1: Guess avg (full variance)
#  #2: Linear on size, unweighted
#  #3: Linear on size, etc., unweighted
#  #4: Linear, weighted by distance and time

# - Decision Trees/forest
# - Other monotonic/isotonic techniques
# - Kernel local regression
# - geographically weighted regression
