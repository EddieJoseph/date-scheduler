import pandas as pd

def convert_input():
    df = load_config("input/ex_config.xlsx")
    df = convert_config(df)
    save_initialization(df, "input/ex_init.xlsx")

def load_config(config_path: str):
    return pd.read_excel(config_path)

def convert_config(df):
    result_df = pd.DataFrame()
    result_df['date'] = pd.Series([None] * len(df.loc[:, 'bezeichnung']))
    result_df['name'] = df['bezeichnung']
    result_df['type'] = df['art']
    result_df['as'] = convert_to_boolean(df['atemschutz'])
    result_df['rb'] = convert_to_boolean(df['riehen'])
    result_df['kb'] = convert_to_boolean(df['kleinbasel'])
    result_df['gb'] = convert_to_boolean(df['grosbasel'])
    result_df['mot'] = convert_to_boolean(df['mot'])
    result_df['asi'] = convert_to_boolean(df['assi'])
    result_df['kad'] = convert_to_boolean(df['kader'])
    result_df['off'] = convert_to_boolean(df['offiziere'])
    result_df['sat'] = convert_to_boolean(df['samstag'])
    result_df['month'] = df['monat']
    return result_df

def convert_to_boolean(series):
    return series.map(lambda x: x == "x")

def save_initialization(df, init_path: str):
    df.to_excel(init_path, index=False)

if __name__ == '__main__':
    convert_input()
