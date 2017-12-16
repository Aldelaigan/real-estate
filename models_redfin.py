# Alec Myres
# August 2017
# First pass at modeling sales data

import sys, os
import pandas as pd
import numpy as np
import datetime as dt
from sklearn.linear_model import LinearRegression
from sklearn.kernel_ridge import KernelRidge
from sklearn.svm import SVR
sys.path.append('/usr/local/lib/python2.7/site-packages')
import geopy.distance as gd

results = pd.read_csv('combined_results.csv', index_col = 0)

# Conversions and new variables
results['lPRICE'] = np.log(results['PRICE'])
results['Sold'] = map(lambda x: dt.datetime.strptime(x, '%B-%d-%Y'), results['SOLD'])
results['HOA'].fillna(0, inplace = True)
results['YearSold'] = map(lambda x: int(x[-4:]), results['SOLD'])
results['Age'] = results['YearSold'] - results['YEAR']
results.query('Age >= -1', inplace = True)

# Build test/train framework
df = results.query('TYPE == "Single Family Residential"')
df = df[~df[['lPRICE','SQFT','LTSZ','BEDS','BATHS']].isnull().any(axis = 1)]
df = df[~df['MLS'].duplicated()]
dl = len(df.index)
df.sort_values('Sold', inplace = True)
df.reset_index(drop = True, inplace = True)

actual = []
model1 = []
model2 = []
model3 = []
model4 = []
pcols = ['SQFT','LTSZ','BEDS','BATHS','Age','HOA']
test_dates = sorted(df['Sold'].unique())[-45:]
for d in test_dates[1:5]:
    print d
    df['SaleAge'] = d - df['Sold']    
    df['SaleAge'] = map(lambda x: x.days, df['SaleAge'])
    df['tWgt'] = 1 - df['SaleAge'] / 1000.0
    train = df.query('Sold  < @d')
    test  = df.query('Sold == @d')
    actual += list(test['PRICE'])
    # Model 1 : Full Variance
    ybar = train['lPRICE'].mean()
    model1 += [ybar]*len(test.index)
    # Model 2 : Simple OLS
    m2 = LinearRegression()
    m2.fit(train[pcols],train[['lPRICE']])
    ypred = m2.predict(test[pcols])
    model2 += list(ypred.ravel())
    for i in list(test.index):
        tgt_lat = test['LATITUDE'][i]
        tgt_lon = test['LONGITUDE'][i]
        c1 = (tgt_lat, tgt_lon)
        train['Dist'] = map(lambda x,y: gd.VincentyDistance(c1,(x,y)).miles,
                            train['LATITUDE'], train['LONGITUDE'])
        train['dWgt'] = 1/train['Dist']
        train['dWgt'] = np.where(train['dWgt'] > 25, 25, train['dWgt'])
        train['Wgt' ] = train['tWgt'] * train['dWgt']
        # Model 3 : Weighted OLS
        m3 = LinearRegression()
        m3.fit(train[pcols], train[['lPRICE']], np.array(train['Wgt']))
        ypred = m3.predict(test[pcols].query('index == @i'))
        model3 += list(ypred.ravel())
        # Model 4 : Weighted SVR
        # TODO: need to standardize the data, then use SVR
        
        m4 = SVR(C = 0.1)
        m4.fit(train[pcols], train[['lPRICE']], np.array(train['Wgt']))
        ypred = m4.predict(test[pcols].query('index == @i'))
        model4 += list(ypred.ravel())


# Predctions, errors
r = pd.DataFrame()
r['actual'] = actual
r['model1'] = model1
r['model2'] = model2
r['model3'] = model3
r['model4'] = model4
r['model1'] = np.exp(r['model1'])
r['model2'] = np.exp(r['model2'])
r['model3'] = np.exp(r['model3'])
r['model4'] = np.exp(r['model4'])
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
sigs = pd.DataFrame()
for i in ['1','2','3','4']:
    sigs['Model' + i] = map(lambda x: np.percentile(r['m' + i + 'errp'].abs(), x), percs)

# Find big errors
r['abs_m4errp'] = r['m4errp'].abs()
big_errors = list(r.sort_values('abs_m4errp', ascending = False).index[:10])


# TODO:
# Data summary
# Distribution of variables
# Add more data
# Log price
# Pairwise data plots

# Models:
#  #1: Guess avg (full variance)
#  #2: Linear on size, unweighted
#  #3: Linear on size, etc., unweighted
#  #4: Linear, weighted by distance and time

# - Decision Trees/forest
# - Other monotonic/isotonic techniques
# - Kernel local regression
# - geographically weighted regression
