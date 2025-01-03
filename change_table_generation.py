import os
import shutil

import pandas as pd

from date_utils import convert_to_date
from file_generation_utils import translate_umlauts, remove_numbers_at_end

from row_names import RowNames


def has_changed(date_1,date_2): #TODO add tex safe comparison of Theme and Responsible
    return not equals(date_1, date_2, RowNames.DATE) or not equals(date_1, date_2, RowNames.TIME) or not equals(date_1, date_2, RowNames.CALLED_UP) #or not equals(date_1, date_2, RowNames.THEME) or not equals(date_1, date_2, RowNames.RESPONSIBLE)


def equals(date_1, date_2, row):
    if pd.isna(date_1[row.value]) and pd.isna(date_2[row.value]):
        return True
    return date_1[row.value] == date_2[row.value]


def new_text_style(text):
    return '\color{OliveGreen}' + text


def old_text_style(text):
    return '\color{BrickRed}\sout{' + text+'}'


def load_change_table_start():
    with open('pdf/templates/change_table_start_tmpl.tex', 'r') as file:
        return file.read()


def load_change_table_end():
    with open('pdf/templates/change_table_end_tmpl.tex', 'r') as file:
        return file.read()


def load_change_table_row():
    with open('pdf/templates/change_table_row_tmpl.tex', 'r') as file:
        return file.read()


def generate_change_table_row(date, time, name, group, theme, responsible):
    row = load_change_table_row()
    row = row.replace('$date', date)
    row = row.replace('$time', time)
    row = row.replace('$name', name)
    row = row.replace('$group', group)
    row = row.replace('$theme', theme)
    row = row.replace('$responsible', responsible)
    return row


def generate_change_table_tex(data, version, old_data, old_versions):
    change_table_tex = ''
    current = data
    current_version = version

    i=0
    while i<len(old_data):
        prevoius = old_data[i]
        previous_version = old_versions[i]
        i=i+1

        change_table_tex += load_change_table_start().replace('$version_old', previous_version).replace('$version_new', current_version)

        missing = prevoius[~prevoius[RowNames.ID.value].isin(current[RowNames.ID.value])]
        new = current[~current[RowNames.ID.value].isin(prevoius[RowNames.ID.value])]
        changed_rows = []
        changed = pd.DataFrame(columns=current.columns)
        for index, row in current[current[RowNames.ID.value].isin(prevoius[RowNames.ID.value])].iterrows():
            if has_changed(row,prevoius.loc[prevoius[RowNames.ID.value] == row[RowNames.ID.value]].iloc[0]):
                changed_rows.append(row)
        if(len(changed_rows)>0):
            changed = pd.concat([pd.DataFrame([row]) for row in changed_rows], ignore_index=True)


        for j in range(0, 366):
            new_events_on_day = new[new[RowNames.DATE.value] == j]
            for event in new_events_on_day.iterrows():
                e_date = new_text_style(convert_to_date(event[1][RowNames.DATE.value], 2025).strftime('%d.%m.%Y'))
                e_time = new_text_style(translate_umlauts(event[1][RowNames.TIME.value]))
                e_name = new_text_style(remove_numbers_at_end(translate_umlauts(event[1][RowNames.NAME.value])))
                e_group = new_text_style(translate_umlauts(event[1][RowNames.CALLED_UP.value]))
                e_theme = new_text_style(translate_umlauts(event[1][RowNames.THEME.value]))
                e_responsible = new_text_style(translate_umlauts(event[1][RowNames.RESPONSIBLE.value]))
                change_table_tex += generate_change_table_row(e_date, e_time, e_name, e_group, e_theme, e_responsible)

            changed_events_on_day = changed[changed[RowNames.DATE.value] == j]
            for event in changed_events_on_day.iterrows():
                e_date = convert_to_date(event[1][RowNames.DATE.value], 2025).strftime('%d.%m.%Y')
                e_time = translate_umlauts(event[1][RowNames.TIME.value])
                e_name = remove_numbers_at_end(translate_umlauts(event[1][RowNames.NAME.value]))
                e_group = translate_umlauts(event[1][RowNames.CALLED_UP.value])
                e_theme = translate_umlauts(event[1][RowNames.THEME.value])
                e_responsible = translate_umlauts(event[1][RowNames.RESPONSIBLE.value])
                # e_date = ''
                # e_time = ''
                # e_name = ''
                # e_group = ''
                # e_theme = ''
                # e_responsible = ''
                if prevoius.loc[prevoius[RowNames.ID.value] == event[1][RowNames.ID.value]].iloc[0][RowNames.DATE.value] != event[1][RowNames.DATE.value]:
                    e_date = old_text_style(convert_to_date(prevoius.loc[prevoius[RowNames.ID.value] == event[1][RowNames.ID.value]].iloc[0][RowNames.DATE.value],2025).strftime('%d.%m.%Y'))+ ' '+new_text_style(convert_to_date(event[1][RowNames.DATE.value], 2025).strftime('%d.%m.%Y'))
                if prevoius.loc[prevoius[RowNames.ID.value] == event[1][RowNames.ID.value]].iloc[0][RowNames.TIME.value] != event[1][RowNames.TIME.value]:
                    e_time = old_text_style(translate_umlauts(prevoius.loc[prevoius[RowNames.ID.value] == event[1][RowNames.ID.value]].iloc[0][RowNames.TIME.value]))+ ' '+new_text_style(translate_umlauts(event[1][RowNames.TIME.value]))
                if prevoius.loc[prevoius[RowNames.ID.value] == event[1][RowNames.ID.value]].iloc[0][RowNames.NAME.value] != remove_numbers_at_end(event[1][RowNames.NAME.value]):
                    e_name = old_text_style(translate_umlauts(prevoius.loc[prevoius[RowNames.ID.value] == event[1][RowNames.ID.value]].iloc[0][RowNames.NAME.value]))+ ' '+new_text_style(remove_numbers_at_end(translate_umlauts(event[1][RowNames.NAME.value])))
                if prevoius.loc[prevoius[RowNames.ID.value] == event[1][RowNames.ID.value]].iloc[0][RowNames.CALLED_UP.value] != event[1][RowNames.CALLED_UP.value]:
                    e_group = old_text_style(translate_umlauts(prevoius.loc[prevoius[RowNames.ID.value] == event[1][RowNames.ID.value]].iloc[0][RowNames.CALLED_UP.value]))+ ' '+new_text_style(translate_umlauts(event[1][RowNames.CALLED_UP.value]))
                if prevoius.loc[prevoius[RowNames.ID.value] == event[1][RowNames.ID.value]].iloc[0][RowNames.THEME.value] != event[1][RowNames.THEME.value]:
                    e_theme = old_text_style(translate_umlauts(prevoius.loc[prevoius[RowNames.ID.value] == event[1][RowNames.ID.value]].iloc[0][RowNames.THEME.value]))+ ' '+new_text_style(translate_umlauts(event[1][RowNames.THEME.value]))
                if prevoius.loc[prevoius[RowNames.ID.value] == event[1][RowNames.ID.value]].iloc[0][RowNames.RESPONSIBLE.value] != event[1][RowNames.RESPONSIBLE.value]:
                    e_responsible = old_text_style(translate_umlauts(prevoius.loc[prevoius[RowNames.ID.value] == event[1][RowNames.ID.value]].iloc[0][RowNames.RESPONSIBLE.value]))+ ' '+new_text_style(translate_umlauts(event[1][RowNames.RESPONSIBLE.value]))
                change_table_tex += generate_change_table_row(e_date, e_time, e_name, e_group, e_theme, e_responsible)

            missing_events_on_day = missing[missing[RowNames.DATE.value] == j]
            for event in missing_events_on_day.iterrows():
                e_date = old_text_style(convert_to_date(event[1][RowNames.DATE.value], 2025).strftime('%d.%m.%Y'))
                e_time = old_text_style(translate_umlauts(event[1][RowNames.TIME.value]))
                e_name = old_text_style(remove_numbers_at_end(translate_umlauts(event[1][RowNames.NAME.value])))
                e_group = old_text_style(translate_umlauts(event[1][RowNames.CALLED_UP.value]))
                e_theme = old_text_style(translate_umlauts(event[1][RowNames.THEME.value]))
                e_responsible = old_text_style(translate_umlauts(event[1][RowNames.RESPONSIBLE.value]))
                change_table_tex += generate_change_table_row(e_date, e_time, e_name, e_group, e_theme, e_responsible)

        change_table_tex += load_change_table_end()
        current = prevoius
        current_version = previous_version

    return change_table_tex

def load_change_document():
    with open('pdf/templates/Anpassungen_Jahresprogramm_tmpl.tex', 'r') as file:
        return file.read()

def generate_change_file(filename, data, version, old_data, old_versions, date):
    print('Generating {}'.format(filename))
    change_table_tex = load_change_document()
    change_table_tex = change_table_tex.replace('$change_table', generate_change_table_tex(data, version, old_data, old_versions))
    change_table_tex = change_table_tex.replace('$date', date)
    change_table_tex = change_table_tex.replace('$version', version)
    with open('pdf/Änderungen_Jahresprogramm.tex', 'w') as output_file:
        output_file.write(change_table_tex)
    cline = 'cd pdf && lualatex.exe -synctex=1 -interaction=nonstopmode Änderungen_Jahresprogramm.tex >> Änderungen_Jahresprogramm.gen.log'
    if os.system(str(cline)):
        raise RuntimeError('program {} failed!'.format(str(cline)))
    shutil.move('pdf/Änderungen_Jahresprogramm.pdf', 'pdf/' + filename)
    print('saved to pdf/{}'.format(filename))

