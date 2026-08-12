import pandas as pd
def load_data(csv_file):
    """
    Load data from a CSV file.

    Args:
        csv_file (str): Path to the CSV file.

    Returns:
        pandas.DataFrame: Loaded data.
    """
    return pd.read_csv(csv_file)

def drop_columns(df : pd.DataFrame, columns_to_drop : list):
    
     return df.drop(columns=columns_to_drop)

def creat_hours(df : pd.DataFrame, column_name : str):
    df[column_name] = pd.to_datetime(df[column_name])
    df['hour'] = df[column_name].dt.hour
    df.drop(columns=[column_name], inplace=True)
    return df

def calculate_rate(df : pd.DataFrame, group_col : str, target_col : str):

    merch_rate = df.groupby(group_col)[target_col].mean()
    df[f"{group_col}_rate"] = df[group_col].map(merch_rate)
    df.drop(columns=[group_col], inplace=True)
    return df

def claculate_age (df : pd.DataFrame, col_name : str):
    df[col_name] = pd.to_datetime(df[col_name])
    df['age'] = (pd.Timestamp.now() - df['dob']).dt.days // 365
    df.drop(columns=[col_name])
    return df
import numpy as np
def haversine_np(lon1, lat1, lon2, lat2):
    """
    Coordinates se kilometers me distance nikalne ka fast function
    """
    lon1, lat1, lon2, lat2 = map(np.radians, [lon1, lat1, lon2, lat2])
    
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    
    a = np.sin(dlat/2.0)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2.0)**2
    c = 2 * np.arcsin(np.sqrt(a))
    km = 6367 * c 
    return km

def claculate_distance(df : pd.DataFrame ):
    df['distance_km'] = haversine_np(df['long'], df['lat'], df['merch_long'], df['merch_lat'])
    geo_columns = ['lat', 'long', 'merch_lat', 'merch_long']
    df = df.drop(columns=geo_columns)

    return df 

def feature_engineering(df):
    col_to_drop = ['Unnamed: 0', 'city', 'state', 'cc_num','zip', 'first', 'last', 'street', 'trans_num']
    drop_columns(df=df, columns_to_drop=col_to_drop)
    creat_hours(df=df,column_name='trans_date_trans_time')
    calculate_rate(df=df,group_col='merchant',target_col='is_fraud')
    claculate_age(df=df,col_name='dob')
    claculate_distance(df=df)
    calculate_rate(df=df,group_col='category',target_col='is_fraud')

    return df 


    

