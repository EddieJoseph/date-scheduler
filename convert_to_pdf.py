import os
import shutil

# from date_scheduler import DateScheduler
from date_utils import convert_to_date, get_weekday_name, get_saturdays_of_year
from enumerator import GroupesEnumerator
from datetime import date

from row_names import RowNames, Groups
from scheduler_config import SchedulerData


def translate_umlauts(text):
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
        return 'ganze KP' +( (' mit RB' if current_group != 'rb' and rb else '') + (' mit KB' if current_group != 'kb' and kb else '') + (' mit GB' if current_group != 'gb' and gb else ''))
    if jf:
        return 'Jugendfeuerwehr'
    if kad:
        return 'Kader'
    if off:
        return 'Off / Wm'
    if asi:
        return 'ASSI' +( (' mit RB' if current_group != 'rb' and rb else '') + (' mit KB' if current_group != 'kb' and kb else '') + (' mit GB' if current_group != 'gb' and gb else ''))
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

    if(series[RowNames.KB.value] or series[RowNames.GB.value]) and not series[RowNames.RB.value]:
        return '18:30 - 21:30'

    return '19:00 - 22:00'


def generate_row(series, index, enumerator, current_group):
    #read file row_templ.tex
    with open('pdf/row_tmpl.tex', 'r') as file:
        row = file.read()
        date = convert_to_date(series[RowNames.DATE.value], 2025)
        date.weekday()
        row = row.replace('$nr', str(index))
        row = row.replace('$date', date.strftime('%d.%m.%Y'))
        row = row.replace('$time', get_time(series))
        row = row.replace('$day', str(get_weekday_name(date.weekday())))
        row = row.replace('$name', str(translate_name(series[RowNames.NAME.value], enumerator, current_group)))
        row = row.replace('$group', generate_group(series, current_group))
        row = row.replace('$theme', '')
        row = row.replace('$responsible', '')

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
    return dates[(dates[RowNames.RB.value]) | (dates[RowNames.TYPE.value] == 'ST')| (dates[RowNames.TYPE.value] == 'MS')| (dates[RowNames.TYPE.value] == 'ASIKVK')| (dates[RowNames.TYPE.value] == 'ASSITST')| (dates[RowNames.TYPE.value] == 'ASIKONT')| (dates[RowNames.TYPE.value] == 'KS')| (dates[RowNames.TYPE.value] == 'B')| (dates[RowNames.TYPE.value] == 'IFA')]

def filter_kb(dates):
    return dates[(dates[RowNames.KB.value]) | (dates[RowNames.TYPE.value] == 'ST')| (dates[RowNames.TYPE.value] == 'MS')| (dates[RowNames.TYPE.value] == 'ASIKVK')| (dates[RowNames.TYPE.value] == 'ASSITST')| (dates[RowNames.TYPE.value] == 'ASIKONT')| (dates[RowNames.TYPE.value] == 'KS')| (dates[RowNames.TYPE.value] == 'B')| (dates[RowNames.TYPE.value] == 'IFA')]

def filter_gb(dates):
    return dates[(dates[RowNames.GB.value]) | (dates[RowNames.TYPE.value] == 'ST')| (dates[RowNames.TYPE.value] == 'MS')| (dates[RowNames.TYPE.value] == 'ASIKVK')| (dates[RowNames.TYPE.value] == 'ASSITST')| (dates[RowNames.TYPE.value] == 'ASIKONT')| (dates[RowNames.TYPE.value] == 'KS')| (dates[RowNames.TYPE.value] == 'B')| (dates[RowNames.TYPE.value] == 'IFA')]

def filter_jf(dates):
    return dates[(dates[RowNames.TYPE.value] == 'J')]

def generate_tex(current_group):
    year = 2025

    data = SchedulerData.create_from('input/dates_combined_u.xlsx')

    # scheduler = DateScheduler(year)
    # scheduler.load_dates('input/dates_combined.xlsx')
    enumerator = GroupesEnumerator()
    dates = data.dates
    dates_kp = {}
    if current_group == Groups.RB.value:
        dates_kp = filter_rb(dates)
    if current_group == Groups.KB.value:
        dates_kp = filter_kb(dates)
    if current_group == Groups.GB.value:
        dates_kp = filter_gb(dates)
    if current_group == Groups.JF.value:
        dates_kp = filter_jf(dates)

    with open('pdf/outputrows.tex', 'w') as output_file:
        i = 1
        for index, row in dates_kp.iterrows():
            tmp = generate_row(row, i, enumerator, current_group)
            output_file.writelines(translate_umlauts(tmp))
            i += 1
            # print(tmp)



def generate_pdf(group, title, displaytitle, version, date, filename):
    generate_tex(group)
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

    shutil.copy('pdf/Jahresprogramm.pdf', 'pdf/' + filename+'.pdf')
    print('pdf/' + filename+".pdf")


if __name__ == '__main__':
    version = '0.3'
    currentdate = date.today().strftime('%d.%m.%Y')

    generate_pdf(Groups.JF.value,'Jahresprogramm JF','Jugendfeuerwehr','0.3', currentdate, 'Jahresprogramm_JF_'+version)
    generate_pdf(Groups.RB.value, 'Jahresprogramm RB', 'Feuerwehr Riehen-Bettingen', '0.3', currentdate,
                 'Jahresprogramm_RB_'+version)
    generate_pdf(Groups.KB.value, 'Jahresprogramm KB', 'Feuerwehr Kleinbasel', '0.3', currentdate,
                 'Jahresprogramm_KB_'+version)
    generate_pdf(Groups.GB.value, 'Jahresprogramm GB', 'Feuerwehr Grossbasel', '0.3', currentdate,
                 'Jahresprogramm_GB_'+version)










