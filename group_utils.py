# enum of companys
import pandas as pd


def get_company(df: pd.DataFrame, *company:str):
    # return elements where df['company'] is in company
    return df[df['company'].isin(company)]

def get_drivers(df: pd.DataFrame):
    return df[df['mot'] == True]

def get_drivers_company(df: pd.DataFrame, *company:str):
    return get_company(df, *company)[df['mot'] == True]

def get_asi(df: pd.DataFrame):
    return df[df['asi'] == True]

def get_asi_company(df: pd.DataFrame, *company:str):
    return get_company(df, *company)[df['mot'] == True]
