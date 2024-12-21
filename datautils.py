import pandas as pd
import json
from scipy.stats import pearsonr, spearmanr, kendalltau

eurozone_capitals = {
    "Paris": {
        "country": "France",
        "sw_lat": 48.815573, 
        "sw_long": 2.224199,
        "ne_lat": 48.902145, 
        "ne_long": 2.469920
    },
    "Berlin": {
        "country": "Germany",
        "sw_lat": 52.339784, 
        "sw_long": 13.088309,
        "ne_lat": 52.675454, 
        "ne_long": 13.761161
    },
    "Madrid": {
        "country": "Spain",
        "sw_lat": 40.312825, 
        "sw_long": -3.88912,
        "ne_lat": 40.643729, 
        "ne_long": -3.561463
    },
    "Rome": {
        "country": "Italy",
        "sw_lat": 41.799544, 
        "sw_long": 12.248678,
        "ne_lat": 42.020923, 
        "ne_long": 12.691870
    },
    "Amsterdam": {
        "country": "Netherlands",
        "sw_lat": 52.278174, 
        "sw_long": 4.728098,
        "ne_lat": 52.431157, 
        "ne_long": 5.079207
    },
    "Vienna": {
        "country": "Austria",
        "sw_lat": 48.166086, 
        "sw_long": 16.179051,
        "ne_lat": 48.323254, 
        "ne_long": 16.577574
    },
    "Lisbon": {
        "country": "Portugal",
        "sw_lat": 38.691399, 
        "sw_long": -9.229064,
        "ne_lat": 38.788765, 
        "ne_long": -9.092600
    },
    "Brussels": {
        "country": "Belgium",
        "sw_lat": 50.779517, 
        "sw_long": 4.243715,
        "ne_lat": 50.913706, 
        "ne_long": 4.469936
    },
    "Athens": {
        "country": "Greece",
        "sw_lat": 37.885082, 
        "sw_long": 23.599058,
        "ne_lat": 38.056439, 
        "ne_long": 23.818654
    },
    "Dublin": {
        "country": "Ireland",
        "sw_lat": 53.298439, 
        "sw_long": -6.387438,
        "ne_lat": 53.410082, 
        "ne_long": -6.114448
    }
}

def get_airbnb_data():
    """
    Load Airbnb data from JSON files for each city in eurozone_capitals
    
    Parameters
    ----------
    None
    
    Returns
    -------
    airbnb_df : pandas.DataFrame
        A DataFrame containing Airbnb data for all cities in eurozone_capitals
    """
    
    df = pd.read_json('data/bnb/Lisbon.json')
    bnbcol = df.columns

    airbnb_df = pd.DataFrame(columns=bnbcol)
    for city in eurozone_capitals.keys():
        with open(f'data/bnb/{city}.json', 'r') as f:
            df = pd.read_json(f)
            df['city'] = city
            airbnb_df = pd.concat([airbnb_df, df], ignore_index=True)
            
    for i in range(len(airbnb_df)):   
        price = airbnb_df.iloc[i].price
        airbnb_df.at[i, 'price'] = price['total']['amount']
    
    for i in range(len(airbnb_df)):
        total_fee = 0
        fee = airbnb_df.iloc[i].fee
        for key in fee.keys():
            total_fee += fee[key].get('amount', 0)
        airbnb_df.at[i, 'fee'] = total_fee
            
    for i in range(len(airbnb_df)):
        rating = airbnb_df.iloc[i].rating
        airbnb_df.at[i, 'stars'] = rating['value']
        airbnb_df.at[i, 'review_count'] = rating['reviewCount']
        
    for i in range(len(airbnb_df)):
        badges = airbnb_df.iloc[i].badges
        if len(badges) > 0:
            airbnb_df.at[i, 'badges'] = badges[0]
        else :
            airbnb_df.at[i, 'badges'] = 'None'
            
    airbnb_df.drop('coordinates', axis=1, inplace=True)
    airbnb_df.drop('long_stay_discount', axis=1, inplace=True)
    airbnb_df.drop('kind', axis=1, inplace=True)
    airbnb_df.drop('images', axis=1, inplace=True)
    airbnb_df.drop('rating', axis=1, inplace=True)
    
    airbnb_df.drop_duplicates(subset=['room_id'], inplace=True)
    
    return airbnb_df

def get_cost_data():
    """
    Read cost data from json files in data/cost directory and return
    the data as a pandas DataFrame.

    Parameters
    ----------
    None

    Returns
    -------
    cost_df : pandas.DataFrame
        DataFrame containing cost of living data for each city in the
        eurozone_capitals dictionary.
    """
    tlist = list()
    for city in eurozone_capitals.keys():
        with open(f'data/cost/{city}.json', 'r') as f:
            row = json.load(f)
            tlist.append(row)
    cost_df = pd.DataFrame(tlist)
    
    return cost_df

def remove_outliers(df,col):

    """
    Remove outliers from a pandas DataFrame column.

    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame containing the column to remove outliers from.
    col : str
        Name of the column to remove outliers from.

    Returns
    -------
    filtered_df : pandas.DataFrame
        DataFrame with outliers removed from the specified column.
    """
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)

    # Compute IQR
    IQR = Q3 - Q1

    # Define bounds
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    # Filter the dataframe
    return df[(df[col] >= lower_bound) & (df[col] <= upper_bound)]

def get_full_correlation_metrics():
    """
    Compute Pearson, Spearman, and Kendall correlation coefficients
    between Airbnb prices and multiple metrics of cost of living.

    Parameters
    ----------
    None

    Returns
    -------
    full_corr_df : pandas.DataFrame
        DataFrame containing the correlation coefficients for each
        category of cost of living metrics.
    """
    airbnb_df = get_airbnb_data()
    cost_df = get_cost_data()
    
    master_df = pd.merge(cost_df, airbnb_df, how='right', on='city')

    df = pd.DataFrame(columns=['category', 'pearson', 'spearman', 'kendall'])
    for col in cost_df.columns:
        if cost_df[col].dtype != 'object':
            pearson_corr, _ = pearsonr((master_df['price'].astype(float)), master_df[col].astype(float))
            spearman_corr, _ = spearmanr((master_df['price'].astype(float)), master_df[col].astype(float))
            kendall_corr, _ = kendalltau((master_df['price'].astype(float)), master_df[col].astype(float))
            x = len(df)
            df.at[x, 'category'] = col
            df.at[x, 'pearson'] = pearson_corr
            df.at[x, 'spearman'] = spearman_corr
            df.at[x, 'kendall'] = kendall_corr
    return df
        
def get_avg_correlation_metrics():
    """
    Compute Pearson, Spearman, and Kendall correlation coefficients
    between average Airbnb prices and multiple metrics of cost of living.

    Parameters
    ----------
    None

    Returns
    -------
    avg_corr_df : pandas.DataFrame
        DataFrame containing the correlation coefficients for each
        category of cost of living metrics.
    """
    airbnb_df = get_airbnb_data()
    cost_df = get_cost_data()
    
    for city in eurozone_capitals.keys():
        cost_df.loc[cost_df['city'] == city, 'avg_airbnb_price'] = airbnb_df[airbnb_df['city'] == city]['price'].mean()

    df = pd.DataFrame(columns=['category', 'pearson', 'spearman', 'kendall'])
    for col in cost_df.columns:
        if cost_df[col].dtype != 'object' and col != 'avg_airbnb_price':
            pearson_corr, _ = pearsonr(cost_df['avg_airbnb_price'].astype(float), cost_df[col].astype(float))
            spearman_corr, _ = spearmanr(cost_df['avg_airbnb_price'].astype(float),cost_df[col].astype(float))
            kendall_corr, _ = kendalltau(cost_df['avg_airbnb_price'].astype(float), cost_df[col].astype(float))
            x = len(df)
            df.at[x, 'category'] = col
            df.at[x, 'pearson'] = pearson_corr
            df.at[x, 'spearman'] = spearman_corr
            df.at[x, 'kendall'] = kendall_corr
    return df