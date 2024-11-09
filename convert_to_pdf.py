import os
import shutil
from datetime import date

import pandas as pd

from calendar_pdf_generation import generate_cal
from convert_output import convert_output
from date_utils import get_saturdays_of_year
from file_generation_utils import filter_dates, enumerate_names
from ics_generation import generate_ics
from programm_pdf_generation import generate_pdf
from row_names import RowNames, Groups
from scheduler_config import SchedulerData


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
                 'Milizfeuerwehr Basel-Stadt', currentdate, version, holidays, additional_days)

    outputfiles.append('Jahresprogramm_komplett_' + version + '.ics')
    generate_ics(data, 2025, outputfiles[-1], version)

    data_kp = filter_dates(Groups.JF, data)
    outputfiles.append('Jahresprogramm_JF_' + version + '.pdf')
    generate_pdf('Jahresprogramm JF', 'Jugendfeuerwehr', version, currentdate,
                 outputfiles[-1], data_kp)
    outputfiles.append('Jahreskalender_JF_' + version + '.pdf')
    generate_cal(data_kp, 2025, outputfiles[-1], 'Jugendfeuerwehr Jahreskalender 2025',
                 'Jugendfeuerwehr', currentdate, version, holidays, additional_days)
    outputfiles.append('Jahresprogramm_JF_' + version + '.ics')
    generate_ics(data_kp, 2025, outputfiles[-1], version)

    data_kp = filter_dates(Groups.RB, data)
    outputfiles.append('Jahresprogramm_RB_' + version + '.pdf')
    generate_pdf('Jahresprogramm RB', 'Feuerwehr Riehen-Bettingen', version, currentdate,
                 outputfiles[-1], data_kp)
    outputfiles.append('Jahreskalender_RB_' + version + '.pdf')
    generate_cal(data_kp, 2025, outputfiles[-1], 'Feuerwehr Riehen-Bettingen Jahreskalender 2025',
                 'Feuerwehr Riehen-Bettingen', currentdate, version, holidays, additional_days)
    outputfiles.append('Jahresprogramm_RB_' + version + '.ics')
    generate_ics(data_kp, 2025, outputfiles[-1], version)

    data_kp = filter_dates(Groups.KB, data)
    outputfiles.append('Jahresprogramm_KB_' + version + '.pdf')
    generate_pdf('Jahresprogramm KB', 'Feuerwehr Kleinbasel', version, currentdate,
                 outputfiles[-1], data_kp)
    outputfiles.append('Jahreskalender_KB_' + version + '.pdf')
    generate_cal(data_kp, 2025, outputfiles[-1], 'Feuerwehr Kleinbasel Jahreskalender 2025',
                 'Feuerwehr Kleinbasel', currentdate, version, holidays, additional_days)
    outputfiles.append('Jahresprogramm_KB_' + version + '.ics')
    generate_ics(data_kp, 2025, outputfiles[-1], version)

    data_kp = filter_dates(Groups.GB, data)
    outputfiles.append('Jahresprogramm_GB_' + version + '.pdf')
    generate_pdf('Jahresprogramm GB', 'Feuerwehr Grossbasel', version, currentdate,
                 outputfiles[-1], data_kp)
    outputfiles.append('Jahreskalender_GB_' + version + '.pdf')
    generate_cal(data_kp, 2025, outputfiles[-1], 'Feuerwehr Grossbasel Jahreskalender 2025',
                 'Feuerwehr Grossbasel', currentdate, version, holidays, additional_days)
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