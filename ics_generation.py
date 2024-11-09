import codecs
import math

from ics import Calendar, Event

from date_utils import convert_to_date
from row_names import RowNames


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
