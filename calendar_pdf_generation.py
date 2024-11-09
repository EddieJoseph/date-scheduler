import os
import shutil
from datetime import datetime, timedelta

from file_generation_utils import translate_umlauts
from date_utils import convert_to_day_of_year
from row_names import RowNames


def get_day_description(date, holidays, additional_days):
    additional_day = additional_days.loc[(additional_days['start'] <= date) & (additional_days['end'] >= date)]
    if len(additional_day)>0:
        return additional_day.iloc[0]['name']

    holiday = holidays.loc[(holidays['start'] < date) & (holidays['end'] >= date) ]
    if len(holiday) > 0:
        return holiday.iloc[0]['name']

    return ''


def load_cal_head():
    with open('pdf/cal_head.tex', 'r') as file:
        return file.read()


def load_cal_tmpl():
    with open('pdf/cal_tmpl.tex', 'r') as file:
        return file.read()


def load_cal_subhead():
    with open('pdf/cal_subhead.tex', 'r') as file:
        return file.read()


def set_cal_day(row, day_index, day_nr, day_info, line_1, line_2, line_3):
    row = row.replace('$' + str(day_index) + 'dayNr', str(day_nr))
    row = row.replace('$' + str(day_index) + 'dayInfo', translate_umlauts(day_info))
    row = row.replace('$' + str(day_index) + 'line1', translate_umlauts(line_1))
    row = row.replace('$' + str(day_index) + 'line2', translate_umlauts(line_2))
    row = row.replace('$' + str(day_index) + 'line3', translate_umlauts(line_3))
    return row


def load_cal_row():
    with open('pdf/cal_row.tex', 'r') as file:
        return file.read()


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
