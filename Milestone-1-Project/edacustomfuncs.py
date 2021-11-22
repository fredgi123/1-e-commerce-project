from datetime import datetime
from statistics import mean
import pandas as pd

def datetowk(l):
    DATE = [datetime.strptime(x, '%Y-%m-%d %H:%M:%S') for x in l]
    ans = []
    for x in DATE:
        if int(x.strftime('%Y')) == 2010:
            ans.append(int(x.strftime('%W')))
        elif int(x.strftime('%Y')) == 2011:
            ans.append(int(x.strftime('%W'))+52)
    return list(set(ans))

def datetomt(l):
    DATE = [datetime.strptime(x, '%Y-%m-%d %H:%M:%S') for x in l]
    ans = []
    for x in DATE:
        if int(x.strftime('%Y')) == 2010:
            ans.append(int(x.strftime('%m')))
        elif int(x.strftime('%Y')) == 2011:
            ans.append(int(x.strftime('%m'))+12)
    return list(set(ans))


def datetoyr(l):
    DATE = [datetime.strptime(x, '%Y-%m-%d %H:%M:%S') for x in l]
    ans = [int(x.strftime('%Y')) for x in DATE]
    return list(set(ans))


def orderfreq(l):
    if len(datetowk(l))>104*0.8:
        return '1.Every Week'
    elif len(datetomt(l)) > 24*0.8:
        return '2.Every Month'
    elif len(datetoyr(l)) == 2:
        return '3.Every Year'
    else:
        return '4.No Pattern'
    

def orderrecency(l):
    try:
        if max(datetowk(l)) == 101:
            return '1.This Week'
        elif max(datetomt(l)) == 24:
            return '2.This Month'
        elif max(datetomt(l)) > 21:
            return '3.This Quarter'
        elif max(datetoyr(l)) == 2011:
            return '4.This Year'
        else:
            return '5.Last Year'
    except:
        return '6.Lost Customer'
    
def aov(l):
    if l < 10:
        return "a.1-10"
    elif l >= 10 and l < 100:
        return "b.10-100"
    elif l >= 100 and l < 250:
        return "c.100-250"
    else:
        return "d. >250"

def retention(l):
    if {2010, 2011}.issubset(set(l)):
        return 'Retained'
    elif {2011}.issubset(set(l)):
        return 'New'
    else:
        return 'Lost'

def cntsummarydf(idf, colname, perc=False):
    sumdf = idf.groupby(by=colname)[colname].count()
    if perc==False:
        return sumdf.copy()
    else:
        return sumdf.apply(lambda x: 100*x/sumdf.sum()).copy()


# Customers Exploratory Data Analysis
def eda_df(idf, col_name='Customer ID'):
    idate_df = idf.groupby(by=col_name, dropna=True)[
        'InvoiceDate'].unique()
    isku_df = idf.groupby(by=col_name, dropna=True)[
        'StockCode'].unique()
    icust_df = idf.groupby(by=col_name, dropna=True)[
        'Customer ID'].unique()
    isale_df = idf.groupby(by=col_name, dropna=True)[
        'SalesValue'].apply(list)
    if col_name == 'Country':
        odf = pd.concat([idate_df, isku_df, isale_df, icust_df],
                        axis=1).reset_index()
    else:
        odf = pd.concat([idate_df, isku_df, isale_df],
                        axis=1).reset_index()

    #
    odf['TransactCount'] = odf['SalesValue'].apply(lambda x: len(x))
    odf['UniqueStockCount'] = odf['StockCode'].apply(lambda x: len(x))
    odf['TransactAvg'] = odf['SalesValue'].apply(lambda x: mean(x))
    odf['AOV'] = odf['TransactAvg'].apply(aov)
    odf['TransactFreq'] = odf['InvoiceDate'].apply(orderfreq)
    odf['TransactRecency'] = odf['InvoiceDate'].apply(orderrecency)
    odf['TransactYears'] = odf['InvoiceDate'].apply(datetoyr)
    odf['Retaintion'] = odf['TransactYears'].apply(retention)

    if col_name == 'Country':
        odf['UniqueCustomerCount'] = odf['Customer ID'].apply(lambda x: len(x))
        odf = odf[[col_name, 'TransactCount', 'UniqueCustomerCount', 'TransactAvg', 'AOV',
                  'TransactFreq', 'TransactRecency', 'TransactYears', 'Retaintion']]
    else:
        odf = odf[[col_name, 'TransactCount', 'UniqueStockCount', 'TransactAvg', 'AOV',
                    'TransactFreq', 'TransactRecency', 'TransactYears', 'Retaintion']]
    print('Created dataframe containing EDA by grouping on - ', col_name)
    return odf.copy()
