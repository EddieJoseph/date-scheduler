from date_scheduler import DateScheduler
from date_utils import convert_to_date, get_weekday_name
from enumerator import GroupesEnumerator


def translate_umlauts(text):
    text = text.replace('ä', '\\"a')
    text = text.replace('ö', '\\"o')
    text = text.replace('ü', '\\"u')
    text = text.replace('Ä', '\\"A')
    text = text.replace('Ö', '\\"O')
    text = text.replace('Ü', '\\"U')
    return text


def generate_group(series, current_group):
    rb = series['rb']
    kb = series['kb']
    gb = series['gb']
    jf = series['type'] == 'J'
    mot = series['mot']
    asi = series['asi']
    kad = series['kad']
    off = series['off']
    type = series['type']

    if type == 'KP' or type == 'ST':
        return 'ganze KP' +( (' mit RB' if current_group != 'rb' and rb else '') + (' mit KB' if current_group != 'kb' and kb else '') + (' mit GB' if current_group != 'gb' and gb else ''))
    if jf:
        return 'Jugendfeuerwehr'
    if kad:
        return 'Kader'
    if off:
        return 'Off / Wm'
    if asi:
        return 'ASSI'
    if type == 'ASIKVK':
        return 'ASSI-Ausbildner'
    if mot:
        return 'Fahrer'
    return 'spez. Aufgebot'


def generate_row(series, index, enumerator, current_group):
    #read file row_templ.tex
    with open('row_tmpl.tex', 'r') as file:
        row = file.read()
        date = convert_to_date(series['date'], 2025)
        date.weekday()
        row = row.replace('$nr', str(index))
        row = row.replace('$date', date.strftime('%d.%m.%Y'))
        row = row.replace('$time', str('19:00 - 22:00'))
        row = row.replace('$day', str(get_weekday_name(date.weekday())))
        row = row.replace('$name', str(translate_name(series['name'], enumerator, current_group)))
        row = row.replace('$group', generate_group(series, current_group))
        row = row.replace('$theme', '')
        row = row.replace('$responsible', '')

        return row

def translate_name(name, enumerator, current_group):
    if name == 'Kompanieübung' or name == 'Gemeinsame Übung':
        if current_group == 'rb':
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
    return dates[(dates['rb']) | (dates['type'] == 'ST')| (dates['type'] == 'MS')| (dates['type'] == 'ASIKVK')| (dates['type'] == 'ASSITST')| (dates['type'] == 'ASIKONT')| (dates['type'] == 'KS')| (dates['type'] == 'B')| (dates['type'] == 'IFA')]

def filter_kb(dates):
    return dates[(dates['kb']) | (dates['type'] == 'ST')| (dates['type'] == 'MS')| (dates['type'] == 'ASIKVK')| (dates['type'] == 'ASSITST')| (dates['type'] == 'ASIKONT')| (dates['type'] == 'KS')| (dates['type'] == 'B')| (dates['type'] == 'IFA')]

def filter_gb(dates):
    return dates[(dates['gb']) | (dates['type'] == 'ST')| (dates['type'] == 'MS')| (dates['type'] == 'ASIKVK')| (dates['type'] == 'ASSITST')| (dates['type'] == 'ASIKONT')| (dates['type'] == 'KS')| (dates['type'] == 'B')| (dates['type'] == 'IFA')]

def filter_jf(dates):
    return dates[(dates['type'] == 'J')]

if __name__ == '__main__':
    year = 2025
    scheduler = DateScheduler(year)
    scheduler.load_dates('input/dates_combined.xlsx')
    enumerator = GroupesEnumerator()

    dates = scheduler.initial_dates

    current_group = 'jf'
    dates_kp = {}
    if current_group == 'rb':
        dates_kp = filter_rb(dates)
    if current_group == 'kb':
        dates_kp = filter_kb(dates)
    if current_group == 'gb':
        dates_kp = filter_gb(dates)
    if current_group == 'jf':
        dates_kp = filter_jf(dates)


    with open('outputrows.tex', 'w') as output_file:
        i = 1
        for index, row in dates_kp.iterrows():
            tmp = generate_row(row, i, enumerator, current_group)
            output_file.writelines(translate_umlauts(tmp))
            i += 1
            print(tmp)
        #print(row, index)

    #print(scheduler.initial_dates)
