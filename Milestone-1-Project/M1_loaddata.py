import pandas as pd
import os.path
from os import path

# Downloading dataset
if path.exists("online_retail_II.xlsx"):
    print("Primary Dataset exists, Let's go!")
else: 
    print("Downloading Primary Dataset.....")   
    import wget
    url = 'https://archive.ics.uci.edu/ml/machine-learning-databases/00502/online_retail_II.xlsx'
    path = os.getcwd()
    wget.download(url, out=path)
    print("Dataset download finished, Let's go!")

# Load Primary Dataset
primary_dataset = 'online_retail_II.xlsx'
file_name = 'm1_primary_data.csv'
try:
    # Check if CSV of the primary_dataset exists
    df = pd.read_csv(file_name)
except:
    df = pd.concat(pd.read_excel(primary_dataset,
                   sheet_name=None), ignore_index=True)
    # Save as a CSV file for faster loading of data
    df.to_csv(file_name, encoding='utf-8', index=False)
    
#__________________________________________________________________________________
print("Loading datasets into dataframes......")
#Dataframe Cleanup
#Stockcode which contains only digits signifies sale entry
#Hence we will filter out enteries with digit only stockcode

clean_df = df[df.StockCode.str.contains('^\d', regex=True, na=False)]

# Drop quantities which are negative
clean_df = clean_df[clean_df["Quantity"] >= 0]

# Drop NA values which indicate missing data which can't be salvaged
clean_df.dropna(inplace=True)

#Adding SalesValue column to the Dataframe
clean_df["SalesValue"] = clean_df["Quantity"]*clean_df["Price"]

#UK Dataframe
uk_df = clean_df[clean_df['Country'] == 'United Kingdom']

#Rest of the World Dataframe
row_df = clean_df.drop(clean_df[clean_df['Country'] == 'United Kingdom'].index)

#__________________________________________________________________________________

# Load Secondary Datasets
# Importing Secondary Datasets - Records for year range 2007 to 2011


#Purchasing power parity GDP, PPP (constant 2017 international $) | Data (worldbank.org)
gdp_df = pd.read_excel('API_NY.GDP.MKTP.PP.KD_DS2_en_excel_v2_2764839.xls',
                       sheet_name=0, header=3, usecols="A,B,D,AZ:BD")

#Inflation CPI Consumer price index (2010 = 100) | Data (worldbank.org)
cpi_df = pd.read_excel("API_FP.CPI.TOTL_DS2_en_excel_v2_2765329.xls",
                       sheet_name=0, header=3, usecols="A,B,D,AZ:BD")

#Debt % versus GDP External debt stocks, long-term (DOD, current US$) | Data (worldbank.org)
#extdebt_df = pd.read_excel("API_DT.DOD.DLXF.CD_DS2_en_excel_v2_2823747.xls",
#                           sheet_name=0, header=3, usecols="A,B,D,AZ:BD")

#Individuals using the Internet (% of population)

internet_df = pd.read_excel("API_IT.NET.USER.ZS_DS2_en_excel_v2_2764008.xls",
                            sheet_name=0, header=3, usecols="A,B,D,AZ:BD")

#Exchange rate fluctuation (L5Y) Official exchange rate (LCU per US$, period average) | Data (worldbank.org)
exchrate_df = pd.read_excel("API_PA.NUS.FCRF_DS2_en_excel_v2_2764464.xls",
                            sheet_name=0, header=3, usecols="A,B,D,AZ:BD")

#Population Population, total | Data (worldbank.org)
pop_df = pd.read_excel("API_SP.POP.TOTL_DS2_en_excel_v2_2764317.xls",
                       sheet_name=0, header=3, usecols="A,B,D,AZ:BD")

#Merchandise imports Merchandise imports (current US$) | Data (worldbank.org)
merch_df = pd.read_excel("API_TM.VAL.MRCH.CD.WT_DS2_en_excel_v2_2766285.xls",
                         sheet_name=0, header=3, usecols="A,B,D,AZ:BD")
## new dataset
expendHealth_df = pd.read_excel("Expenditure_on_health.xls",
                                sheet_name=0, header=3, usecols="A,B,D,AZ:BD")
## new dataset
lifeExpect_df = pd.read_excel("Life_expectancy.xls",
                              sheet_name=0, header=3, usecols="A,B,D,AZ:BD")

## new dataset
PPP_per_capita_df = pd.read_excel("PPP_per_capita.xls",
                                  sheet_name=0, header=3, usecols="A,B,D,AZ:BD")
# Country properties such as income group and region
prop_df = pd.read_excel("API_SP.POP.TOTL_DS2_en_excel_v2_2764317.xls",
                        sheet_name='Metadata - Countries', header=0, usecols="A,B,C")

#CERDI Sea Distance Dataset
seadist_df = pd.read_excel("CERDI-seadistance.xlsx", usecols="A,B,C")
# Cleaning Sea Distance DF to only include entries with UK as the origin
seadist_df = seadist_df[seadist_df["iso1"] == "GBR"]

print("Finished loading all datasets and creating respective dataframes")
#_____________________________________________________________________________________

# Function to normalize country names to code that will be used as a key to combine all datasets
def valeurs(k,value=True):
    filtered={'United Kingdom': 'GBR',
    'France': 'FRA',
    'USA': 'USA',
    'Belgium': 'BEL',
    'Australia': 'AUS',
    'EIRE': 'IRL',
    'Germany': 'DEU',
    'Portugal': 'PRT',
    'Japan': 'JPN',
    'Denmark': 'DNK',
    'Nigeria': 'NGA',
    'Netherlands': 'NLD',
    'Poland': 'POL',
    'Spain': 'ESP',
    'Channel Islands': 'CHI',
    'Italy': 'ITA',
    'Cyprus': 'CYP',
    'Greece': 'GRC',
    'Norway': 'NOR',
    'Austria': 'AUT',
    'Sweden': 'SWE',
    'United Arab Emirates': 'ARE',
    'Finland': 'FIN',
    'Switzerland': 'CHE',
    'Malta': 'MLT',
    'Bahrain': 'BHR',
    'Bermuda': 'BMU',
    'Hong Kong': 'HKG',
    'Singapore': 'SGP',
    'Thailand': 'THA',
    'Israel': 'ISR',
    'Lithuania': 'LTU',
    'Lebanon': 'LBN',
    'Korea': 'KOR',
    'Brazil': 'BRA',
    'Canada': 'CAN',
    'Iceland': 'ISL',
    'Saudi Arabia' : 'SAU',
    'Czech Republic': 'CZE',
    'RSA' : 'ZAF'}
    ## returns country value based on key

    if value:
        try:
            value=filtered[k]
        except:
            vale=None
        return value

## returns country key based on value (code)    
    else:
        try:
            for key, value in filtered.items():
                if k == value:
                    return key
        except:
            key=None
        return key