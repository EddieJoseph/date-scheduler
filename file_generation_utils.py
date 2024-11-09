import math

from new_enumerator import NewEnumerator
from row_names import RowNames, Groups


def translate_umlauts(text):
    if text == None:
        return ""
    if isinstance(text, float):
        if math.isnan(text):
            return ""
        text = str(text)

    if isinstance(text, int):
        text = str(text)
    text = text.replace('ä', '\\"a')
    text = text.replace('ö', '\\"o')
    text = text.replace('ü', '\\"u')
    text = text.replace('Ä', '\\"A')
    text = text.replace('Ö', '\\"O')
    text = text.replace('Ü', '\\"U')
    return text


def filter_rb(dates):
    return dates[
        (dates[RowNames.RB.value]) | (dates[RowNames.TYPE.value] == 'ST') | (dates[RowNames.TYPE.value] == 'MS') | (
                dates[RowNames.TYPE.value] == 'ASIKVK') | (dates[RowNames.TYPE.value] == 'ASSITST') | (
                dates[RowNames.TYPE.value] == 'ASIKONT') | (dates[RowNames.TYPE.value] == 'KS') | (
                dates[RowNames.TYPE.value] == 'B') | (dates[RowNames.TYPE.value] == 'IFA')]


def filter_kb(dates):
    return dates[
        (dates[RowNames.KB.value]) | (dates[RowNames.TYPE.value] == 'ST') | (dates[RowNames.TYPE.value] == 'MS') | (
                dates[RowNames.TYPE.value] == 'ASIKVK') | (dates[RowNames.TYPE.value] == 'ASSITST') | (
                dates[RowNames.TYPE.value] == 'ASIKONT') | (dates[RowNames.TYPE.value] == 'KS') | (
                dates[RowNames.TYPE.value] == 'B') | (dates[RowNames.TYPE.value] == 'IFA')]


def filter_gb(dates):
    return dates[
        (dates[RowNames.GB.value]) | (dates[RowNames.TYPE.value] == 'ST') | (dates[RowNames.TYPE.value] == 'MS') | (
                dates[RowNames.TYPE.value] == 'ASIKVK') | (dates[RowNames.TYPE.value] == 'ASSITST') | (
                dates[RowNames.TYPE.value] == 'ASIKONT') | (dates[RowNames.TYPE.value] == 'KS') | (
                dates[RowNames.TYPE.value] == 'B') | (dates[RowNames.TYPE.value] == 'IFA')]


def filter_jf(dates):
    return dates[(dates[RowNames.TYPE.value] == 'J')]


def filter_dates(current_group, data):
    dates_kp = {}
    if current_group == Groups.RB:
        dates_kp = filter_rb(data)
    if current_group == Groups.KB:
        dates_kp = filter_kb(data)
    if current_group == Groups.GB:
        dates_kp = filter_gb(data)
    if current_group == Groups.JF:
        dates_kp = filter_jf(data)
    return dates_kp


def enumerate_names(data):
    enumerators = NewEnumerator()
    names = data[RowNames.NAME.value].value_counts()
    unique_names = names[names == 1].keys().to_list()

    for index, row in data.iterrows():
        if not row[RowNames.NAME.value] in unique_names:
            nr = enumerators.get_nr_extract_group(row[RowNames.NAME.value], row[RowNames.TYPE.value],
                                                  row[RowNames.GB.value], row[RowNames.KB.value],
                                                  row[RowNames.RB.value], row[RowNames.TYPE.value] == 'J')
            data.at[index, RowNames.NAME.value] = row[RowNames.NAME.value] + ' ' + str(nr)
