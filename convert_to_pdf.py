import codecs
import math
import os
import shutil
from datetime import date, datetime, timedelta

import pandas as pd
from ics import Calendar, Event

from convert_output import convert_output
from date_utils import convert_to_date, get_weekday_name, get_saturdays_of_year, convert_to_day_of_year
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


def generate_tex(data):
    with open('pdf/outputrows.tex', 'w') as output_file:
        i = 1
        for index, row in data.iterrows():
            tmp = generate_row(row, i)
            output_file.writelines(translate_umlauts(tmp))
            i += 1


def generate_pdf(title, displaytitle, version, date, filename, data):
    print('Generating {}'.format(title))
    generate_tex(data)
    with open('pdf/Jahresprogramm_tmpl.tex', 'r') as template:
        with open('pdf/Jahresprogramm.tex', 'w') as output:
            for line in template:
                line = line.replace('$title', title)
                line = line.replace('$displaytitle', displaytitle)
                line = line.replace('$version', version)
                line = line.replace('$date', date)
                output.write(line)

    cline = 'cd pdf && lualatex.exe -synctex=1 -interaction=nonstopmode Jahresprogramm.tex >> Jahresprogramm.gen.log'
    if os.system(str(cline)):
        raise RuntimeError('program {} failed!'.format(str(cline)))

    shutil.move('pdf/Jahresprogramm.pdf', 'pdf/' + filename)
    print('saved to pdf/{}'.format(filename))


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


def load_cal_head():
    with open('pdf/cal_head.tex', 'r') as file:
        return file.read()


def load_cal_tmpl():
    with open('pdf/cal_tmpl.tex', 'r') as file:
        return file.read()


def load_cal_subhead():
    with open('pdf/cal_subhead.tex', 'r') as file:
        return file.read()


def load_cal_row():
    with open('pdf/cal_row.tex', 'r') as file:
        return file.read()


def set_cal_day(row, day_index, day_nr, day_info, line_1, line_2, line_3):
    row = row.replace('$' + str(day_index) + 'dayNr', str(day_nr))
    row = row.replace('$' + str(day_index) + 'dayInfo', translate_umlauts(day_info))
    row = row.replace('$' + str(day_index) + 'line1', translate_umlauts(line_1))
    row = row.replace('$' + str(day_index) + 'line2', translate_umlauts(line_2))
    row = row.replace('$' + str(day_index) + 'line3', translate_umlauts(line_3))
    return row


def get_day_description(date, holidays, additional_days):
    additional_day = additional_days.loc[(additional_days['start'] <= date) & (additional_days['end'] >= date)]
    if len(additional_day)>0:
        return additional_day.iloc[0]['name']

    holiday = holidays.loc[(holidays['start'] < date) & (holidays['end'] >= date) ]
    if len(holiday) > 0:
        return holiday.iloc[0]['name']

    return ''


def generate_cal(data, year, filename, title, displaytitle, date, version, holidays, additional_days):
    print('Generating {}'.format(title))

    month_names = ['Januar', 'Februar', 'März', 'April', 'Mai', 'Juni', 'Juli', 'August', 'September', 'Oktober',
                   'November', 'Dezember']
    tmp_date = datetime(year, 1, 1)
    day_index = tmp_date.weekday() + 1
    month = 0
    month_indexes = []
    output = ''
    row_index = 2

    row = load_cal_row()
    for i in range(1, day_index):
        row = set_cal_day(row, i, ' ', ' ', ' ', ' ', ' ')

    for i in range(0, 365):
        events_on_day = data[data[RowNames.DATE.value] == convert_to_day_of_year(tmp_date)]
        event_names = []
        for j in range(0, 3):
            if j < len(events_on_day):
                base_name = events_on_day.iloc[j]['name']
                gb = events_on_day.iloc[j]['gb']
                kb = events_on_day.iloc[j]['kb']
                rb = events_on_day.iloc[j]['rb']
                jf = events_on_day.iloc[j]['type'] == 'J'
                if gb or kb or rb or jf:
                    base_name = base_name + ' ['
                    name_addition = ''
                    if gb:
                        name_addition = name_addition + 'GB'
                    if gb and (kb or rb or jf):
                        name_addition = name_addition + ', '
                    if kb:
                        name_addition = name_addition + 'KB'
                    if kb and (rb or jf):
                        name_addition = name_addition + ', '
                    if rb:
                        name_addition = name_addition + 'RB'
                    if rb and jf:
                        name_addition = name_addition + ', '
                    if jf:
                        name_addition = name_addition + 'JF'
                    name_addition = name_addition + ']'
                    base_name = base_name + name_addition
                event_names.append(base_name)
            else:
                event_names.append(' ')
        row = set_cal_day(row, day_index, tmp_date.day, get_day_description(tmp_date,holidays,additional_days), event_names[0], event_names[1], event_names[2])

        if day_index == 7:
            if tmp_date.month != month:
                month = tmp_date.month
                output = output + load_cal_subhead().replace('$month', translate_umlauts(month_names[month - 1]))
                month_indexes.append(row_index)
                row_index = row_index + 1

            output = output + row
            row_index = row_index + 1
            row = load_cal_row()
            day_index = 0

        day_index = day_index + 1
        tmp_date = tmp_date + timedelta(days=1)

    for i in range(day_index, 8):
        row = set_cal_day(row, i, ' ', ' ', ' ', ' ', ' ')
    output = output + row
    row_index = row_index + 1

    head = load_cal_head().replace('$head_nr', ','.join(map(str, month_indexes)))
    output = head + output

    output = load_cal_tmpl().replace('$cal_data', output)
    output = output.replace('$title', translate_umlauts(title))
    output = output.replace('$displaytitle', translate_umlauts(displaytitle))
    output = output.replace('$version', version)
    output = output.replace('$date', translate_umlauts(date))

    with open('pdf/Jahreskalender.tex', 'w') as cal_out:
        cal_out.write(output)
    cline = 'cd pdf && lualatex.exe -synctex=1 -interaction=nonstopmode Jahreskalender.tex >> Jahreskalender.gen.log'
    if os.system(str(cline)):
        raise RuntimeError('program {} failed!'.format(str(cline)))

    shutil.move('pdf/Jahreskalender.pdf', 'pdf/' + filename)
    print('saved to pdf/{}'.format(filename))



def get_string(text):
    if text == None:
        return ""
    if isinstance(text, float):
        if math.isnan(text):
            return ""
        text = str(text)
    if isinstance(text, int):
        text = str(text)
    return text



def generate_description(row, version):
    description = ''
    called_up = get_string(row[RowNames.CALLED_UP.value])
    if called_up != '':
        description += 'Aufgebot: ' + called_up + '\n'

    responsible = get_string(row[RowNames.RESPONSIBLE.value])
    if responsible != '':
        description += 'Verantwortlich: ' + responsible + '\n'

    if get_string(row[RowNames.THEME.value]) != '':
        description += 'Thema: ' + get_string(row[RowNames.THEME.value]) + '\n'

    if get_string(row[RowNames.DETAILS.value]) != '':
        description += 'Beschreibung: ' + get_string(row[RowNames.DETAILS.value]) + '\n'

    description += 'Version: ' + version
    return description


def generate_ics(data, year, filename, version):
    calendar = Calendar()

    for index, row in data.iterrows():
        event = Event()
        event.name = row[RowNames.NAME.value]
        event.description = generate_description(row, version)
        event.uid = row[RowNames.ID.value]
        times = row[RowNames.TIME.value].split('-')
        times = [x.strip() for x in times]

        if(len(times) == 2):
            convert_to_date(row[RowNames.DATE.value],year)
            event.begin = convert_to_date(row[RowNames.DATE.value], year).strftime('%Y-%m-%d ') + times[0] + ':00+01:00'
            event.end = convert_to_date(row[RowNames.DATE.value], year).strftime('%Y-%m-%d ') + times[1] + ':00+01:00'
        else:
            event.begin = (convert_to_date(row[RowNames.DATE.value], year)).strftime('%Y-%m-%d')
            event.make_all_day()
        calendar.events.add(event)

    with codecs.open('pdf/'+filename, 'w','utf-8') as file:
        file.writelines(calendar.serialize_iter())


if __name__ == '__main__':
    version = '1.1'
    old_versions = ['1.0']
    data = SchedulerData.create_from('input/dates_combined_'+version+'.xlsx').dates
    data.sort_values(by=RowNames.DATE.value, inplace=True)
    data = data[data[RowNames.INCLUDE.value] == True]

    enumerate_names(data)

    currentdate = date.today().strftime('%d.%m.%Y')

    holidays = pd.read_excel('input/holidays.xlsx')
    additional_days = pd.read_excel('input/additional_days.xlsx')

    outputfiles = ['Jahresprogramm_komplett_' + version + '.xlsx']
    convert_output(data, 'pdf/'+outputfiles[-1], 2025)

    outputfiles.append('Jahreskalender_komplett_'+ version + '.pdf')
    generate_cal(data, 2025, outputfiles[-1], 'Milizfeuerwehr Basel-Stadt Jahreskalender 2025',
                 'Milizfeuerwehr Basel-Stadt', currentdate, version,holidays,additional_days)

    outputfiles.append('Jahresprogramm_komplett_' + version + '.ics')
    generate_ics(data, 2025, outputfiles[-1], version)

    data_kp = filter_dates(Groups.JF, data)
    outputfiles.append('Jahresprogramm_JF_' + version + '.pdf')
    generate_pdf('Jahresprogramm JF', 'Jugendfeuerwehr', version, currentdate,
                 outputfiles[-1], data_kp)
    outputfiles.append('Jahreskalender_JF_' + version + '.pdf')
    generate_cal(data_kp, 2025, outputfiles[-1], 'Jugendfeuerwehr Jahreskalender 2025',
                 'Jugendfeuerwehr', currentdate, version,holidays,additional_days)
    outputfiles.append('Jahresprogramm_JF_' + version + '.ics')
    generate_ics(data_kp, 2025, outputfiles[-1], version)

    data_kp = filter_dates(Groups.RB, data)
    outputfiles.append('Jahresprogramm_RB_' + version + '.pdf')
    generate_pdf('Jahresprogramm RB', 'Feuerwehr Riehen-Bettingen', version, currentdate,
                 outputfiles[-1], data_kp)
    outputfiles.append('Jahreskalender_RB_' + version + '.pdf')
    generate_cal(data_kp, 2025, outputfiles[-1], 'Feuerwehr Riehen-Bettingen Jahreskalender 2025',
                 'Feuerwehr Riehen-Bettingen', currentdate, version,holidays,additional_days)
    outputfiles.append('Jahresprogramm_RB_' + version + '.ics')
    generate_ics(data_kp, 2025, outputfiles[-1], version)

    data_kp = filter_dates(Groups.KB, data)
    outputfiles.append('Jahresprogramm_KB_' + version + '.pdf')
    generate_pdf('Jahresprogramm KB', 'Feuerwehr Kleinbasel', version, currentdate,
                 outputfiles[-1], data_kp)
    outputfiles.append('Jahreskalender_KB_' + version + '.pdf')
    generate_cal(data_kp, 2025, outputfiles[-1], 'Feuerwehr Kleinbasel Jahreskalender 2025',
                 'Feuerwehr Kleinbasel', currentdate, version,holidays,additional_days)
    outputfiles.append('Jahresprogramm_KB_' + version + '.ics')
    generate_ics(data_kp, 2025, outputfiles[-1], version)

    data_kp = filter_dates(Groups.GB, data)
    outputfiles.append('Jahresprogramm_GB_' + version + '.pdf')
    generate_pdf('Jahresprogramm GB', 'Feuerwehr Grossbasel', version, currentdate,
                 outputfiles[-1], data_kp)
    outputfiles.append('Jahreskalender_GB_' + version + '.pdf')
    generate_cal(data_kp, 2025, outputfiles[-1], 'Feuerwehr Grossbasel Jahreskalender 2025',
                 'Feuerwehr Grossbasel', currentdate, version,holidays,additional_days)
    outputfiles.append('Jahresprogramm_GB_' + version + '.ics')
    generate_ics(data_kp, 2025, outputfiles[-1], version)

    shutil.rmtree('pdf/Jahresprogramm/', ignore_errors=True)
    shutil.rmtree('output/Jahresprogramm/', ignore_errors=True)
    os.mkdir('pdf/Jahresprogramm')
    for f in outputfiles:
        shutil.move('pdf/' + f, 'pdf/Jahresprogramm/')
    shutil.move('pdf/Jahresprogramm/', 'output/')

    tmp_files = ['outputrows.tex', 'Jahreskalender.aux', 'Jahreskalender.gen.log', 'Jahreskalender.log', 'Jahreskalender.synctex.gz', 'Jahreskalender.tex', 'Jahresprogramm.aux', 'Jahresprogramm.gen.log', 'Jahresprogramm.log', 'Jahresprogramm.synctex.gz', 'Jahresprogramm.tex']

    for f in tmp_files:
        try:
            os.remove('pdf/' + f)
        except:
            pass