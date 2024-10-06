import math
import os
import shutil
from datetime import date

from convert_output import convert_output
from date_utils import convert_to_date, get_weekday_name, get_saturdays_of_year
from new_enumerator import NewEnumerator
from row_names import RowNames, Groups
from scheduler_config import SchedulerData


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


def generate_group(series, current_group):
    rb = series[RowNames.RB.value]
    kb = series[RowNames.KB.value]
    gb = series[RowNames.GB.value]
    jf = series[RowNames.TYPE.value] == 'J'
    mot = series[RowNames.MOT.value]
    asi = series[RowNames.ASI.value]
    kad = series[RowNames.KADER.value]
    off = series[RowNames.OFF.value]
    type = series[RowNames.TYPE.value]

    if type == 'KP' or type == 'ST':
        return 'ganze KP' + ((' mit RB' if current_group != 'rb' and rb else '') + (
            ' mit KB' if current_group != 'kb' and kb else '') + (' mit GB' if current_group != 'gb' and gb else ''))
    if jf:
        return 'Jugendfeuerwehr'
    if kad:
        return 'Kader'
    if off:
        return 'Off / Wm'
    if asi:
        return 'ASSI' + ((' mit RB' if current_group != 'rb' and rb else '') + (
            ' mit KB' if current_group != 'kb' and kb else '') + (' mit GB' if current_group != 'gb' and gb else ''))
    if type == 'ASIKVK':
        return 'ASSI-Ausbildner'
    if mot:
        return 'Fahrer'
    return 'spez. Aufgebot'


def get_time(series):
    if series[RowNames.TYPE.value] == 'KS':
        return '08:00 - 17:00'
    if series[RowNames.TYPE.value] == 'J':
        return '08:00 - 12:00'
    if series[RowNames.TYPE.value] == 'MS':
        return '08:00 - 17:00'
    if series[RowNames.DATE.value] in get_saturdays_of_year(2025):
        return '08:00 - 12:00'
    if series[RowNames.TYPE.value] == 'IFA':
        return '07:00 - 18:00'
    if series[RowNames.TYPE.value] == 'SAN':
        return '17:00 - 20:00'
    if series[RowNames.TYPE.value] == 'ASI':
        return '19:00 - 22:00'
    if series[RowNames.TYPE.value] == 'ASIKONT':
        return '08:00 - 12:00'
    if series[RowNames.TYPE.value] == 'ASSITST':
        return '19:00 - 22:00'
    if series[RowNames.TYPE.value] == 'ASIKVK':
        return '19:00 - 22:00'
    if series[RowNames.TYPE.value] == 'ST':
        return '19:00 - 20:00'
    if series[RowNames.TYPE.value] == 'B':
        return '19:00 - 22:00'

    if (series[RowNames.KB.value] or series[RowNames.GB.value]) and not series[RowNames.RB.value]:
        return '18:30 - 21:30'

    return '19:00 - 22:00'


def generate_row(series, index):
    # read file row_templ.tex
    with open('pdf/row_tmpl.tex', 'r') as file:
        row = file.read()
        date = convert_to_date(series[RowNames.DATE.value], 2025)
        date.weekday()
        row = row.replace('$nr', str(index))
        row = row.replace('$date', date.strftime('%d.%m.%Y'))
        row = row.replace('$time', translate_umlauts(series[RowNames.TIME.value]))
        row = row.replace('$day', str(get_weekday_name(date.weekday())))
        row = row.replace('$name', translate_umlauts(series[RowNames.NAME.value]))
        row = row.replace('$group', translate_umlauts(series[RowNames.CALLED_UP.value]))
        row = row.replace('$theme', translate_umlauts(series[RowNames.THEME.value]))
        row = row.replace('$responsible', translate_umlauts(series[RowNames.RESPONSIBLE.value]))

        return row


def translate_name(name, enumerator, current_group):
    if name == 'Kompanieübung' or name == 'Gemeinsame Übung':
        if current_group == RowNames.RB.value:
            return 'Kompanieübung' + enumerator.get_kp(current_group)
        else:
            return 'Zugsübung' + enumerator.get_kp(current_group)
    if name == 'Materialdienst':
        return 'Materialdienst' + enumerator.get_mat(current_group)
    if name == 'Jugendfeuerwehr':
        return 'Jugendfeuerwehrübung' + enumerator.get_jf(current_group)
    if name == 'ASSI KVK':
        return 'ASSI KVK' + enumerator.get_akvk(current_group)
    if name == 'ASSI Übung':
        return 'ASSI Übung' + enumerator.get_asi(current_group)
    if name == 'Motorsäge':
        return 'Motorsägen Kurs'
    if name == 'Fahrer WBK':
        return 'Fahrer WBK'
    if name == 'Of Übung':
        return 'Of Übung' + enumerator.get_of(current_group)
    if name == 'Fahrzeugunterhalt':
        return 'Fahrzeugunterhalt' + enumerator.get_fu(current_group)
    if name == 'Kaderübung':
        return 'Kaderübung' + enumerator.get_kad(current_group)
    if name == 'Fahrer':
        return 'Fahrer' + enumerator.get_f(current_group)
    if name == 'BF Übung':
        return 'BF-Übung'
    if name == 'Sanhist':
        return 'Sanhist'
    if name == 'WTA':
        return 'WTA'
    if name == 'Sporttest':
        return 'Sporttest' + enumerator.get_sp(current_group)
    if name == 'Hydrosub':
        return 'Hydrosub'
    if name == 'Basisausbildung KVK':
        return 'Basisausbildung KVK'
    if name == 'Basisausbildung':
        return 'Basisausbildung' + enumerator.get_b(current_group)
    if name == 'MS Modul':
        return 'MS Modul'
    if name == 'Schlauchprüfung':
        return 'Schlauchprüfung'
    if name == 'ASSI Eignungstest':
        return 'ASSI Eignungstest'
    if name == 'IFA':
        return 'Heissausbildung'
    if name == 'ASSI Materialkontrolle':
        return 'ASSI Materialkontrolle'
    if name == 'Hauptübung':
        return 'Hauptübung'


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


def generate_tex(current_group, data):
    dates_kp = {}
    if current_group == Groups.RB.value:
        dates_kp = filter_rb(data)
    if current_group == Groups.KB.value:
        dates_kp = filter_kb(data)
    if current_group == Groups.GB.value:
        dates_kp = filter_gb(data)
    if current_group == Groups.JF.value:
        dates_kp = filter_jf(data)

    with open('pdf/outputrows.tex', 'w') as output_file:
        i = 1
        for index, row in dates_kp.iterrows():
            tmp = generate_row(row, i)
            output_file.writelines(translate_umlauts(tmp))
            i += 1


def generate_pdf(group, title, displaytitle, version, date, filename, data):
    generate_tex(group, data)
    with open('pdf/Jahresprogramm_tmpl.tex', 'r') as template:
        with open('pdf/Jahresprogramm.tex', 'w') as output:
            for line in template:
                line = line.replace('$title', title)
                line = line.replace('$displaytitle', displaytitle)
                line = line.replace('$version', version)
                line = line.replace('$date', date)
                output.write(line)

    cline = 'cd pdf && lualatex.exe -synctex=1 -interaction=nonstopmode Jahresprogramm.tex'
    if os.system(str(cline)):
        raise RuntimeError('program {} failed!'.format(str(cline)))

    shutil.copy('pdf/Jahresprogramm.pdf', 'pdf/' + filename + '.pdf')
    print('pdf/' + filename + ".pdf")


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


if __name__ == '__main__':
    version = '0.3'
    data = SchedulerData.create_from('input/dates_combined_u.xlsx').dates
    data.sort_values(by=RowNames.DATE.value, inplace=True)
    data = data[data[RowNames.INCLUDE.value] == True]

    enumerate_names(data)

    convert_output(data, 'pdf/Jahresprogramm_komplett_' + version + '.xlsx', 2025)

    currentdate = date.today().strftime('%d.%m.%Y')

    generate_pdf(Groups.JF.value, 'Jahresprogramm JF', 'Jugendfeuerwehr', '0.3', currentdate,
                 'Jahresprogramm_JF_' + version, data)
    generate_pdf(Groups.RB.value, 'Jahresprogramm RB', 'Feuerwehr Riehen-Bettingen', '0.3', currentdate,
                 'Jahresprogramm_RB_' + version, data)
    generate_pdf(Groups.KB.value, 'Jahresprogramm KB', 'Feuerwehr Kleinbasel', '0.3', currentdate,
                 'Jahresprogramm_KB_' + version, data)
    generate_pdf(Groups.GB.value, 'Jahresprogramm GB', 'Feuerwehr Grossbasel', '0.3', currentdate,
                 'Jahresprogramm_GB_' + version, data)
