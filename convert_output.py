import pandas as pd
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl.workbook import Workbook
from openpyxl.worksheet.table import Table, TableStyleInfo

from date_utils import convert_to_datetime
from row_names import RowNames


def convert_output(dates, output_path, year):
    df = convert_process_result(dates, year)
    save_converted_output(df, output_path)


def load_output(config_path: str):
    return pd.read_excel(config_path)


def convert_process_result(df, year):
    result_df = pd.DataFrame()
    result_df['datum'] = convert_timestamp_to_date(df[RowNames.DATE.value].map(lambda x: convert_to_datetime(x, year)))
    result_df['bezeichnung'] = df[RowNames.NAME.value]
    result_df['art'] = df[RowNames.TYPE.value]
    result_df['atemschutz'] = convert_to_boolean(df[RowNames.AS.value])
    result_df['riehen'] = convert_to_boolean(df[RowNames.RB.value])
    result_df['kleinbasel'] = convert_to_boolean(df[RowNames.KB.value])
    result_df['grosbasel'] = convert_to_boolean(df[RowNames.GB.value])
    result_df['mot'] = convert_to_boolean(df[RowNames.MOT.value])
    result_df['assi'] = convert_to_boolean(df[RowNames.ASI.value])
    result_df['kader'] = convert_to_boolean(df[RowNames.KADER.value])
    result_df['offiziere'] = convert_to_boolean(df[RowNames.OFF.value])
    result_df['samstag'] = convert_to_boolean(df[RowNames.SAT.value])
    return result_df


def convert_to_boolean(series):
    return series.map(lambda x: "x" if x else "")


def convert_timestamp_to_date(series):
    return series.map(lambda x: x.date())


def get_last_cell(df):
    cols = chr(65 + df.shape[1] - 1)
    rows = df.shape[0] + 1
    return cols + str(rows)


def save_converted_output(df, init_path: str):
    get_last_cell(df)

    # Create a workbook and select the active worksheet
    wb = Workbook()
    ws = wb.active

    # Append DataFrame rows to the worksheet
    for r in dataframe_to_rows(df, index=False, header=True):
        ws.append(r)

    # Create a table
    tab = Table(displayName="Übungsdaten", ref="A1:" + get_last_cell(df))

    # Add a default style with striped rows and banded columns
    style = TableStyleInfo(name="TableStyleMedium9", showFirstColumn=False,
                           showLastColumn=False, showRowStripes=True, showColumnStripes=True)
    tab.tableStyleInfo = style
    ws.add_table(tab)

    # Save to an Excel file
    wb.save(init_path)


if __name__ == '__main__':
    convert_output()
