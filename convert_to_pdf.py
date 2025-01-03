import os
import shutil
from datetime import date

import pandas as pd

from calendar_pdf_generation import generate_cal
from change_table_generation import generate_change_file
from convert_output import convert_output
from date_utils import get_saturdays_of_year
from file_generation_utils import filter_dates, enumerate_names
from ics_generation import generate_ics
from programm_pdf_generation import generate_pdf
from row_names import RowNames, Groups
from scheduler_config import SchedulerData


if __name__ == '__main__':
    version = '1.1'
    old_versions = ['1.0.1','1.0']

    data = SchedulerData.create_from('input/dates_combined_'+version+'.xlsx').dates
    data.sort_values(by=RowNames.DATE.value, inplace=True)
    data = data[data[RowNames.INCLUDE.value] == True]

    old_data = list(
        map(lambda old_version: SchedulerData.create_from('input/dates_combined_' + old_version + '.xlsx').dates,
            old_versions))
    for index, old in enumerate(old_data):
        old_data[index] = old[old[RowNames.INCLUDE.value] == True]


    enumerate_names(data)

    currentdate = date.today().strftime('%d.%m.%Y')

    holidays = pd.read_excel('input/holidays.xlsx')
    additional_days = pd.read_excel('input/additional_days.xlsx')
    outputfiles = []

    outputfiles.append('Jahresprogramm_komplett_' + version + '.xlsx')
    convert_output(data, 'pdf/'+outputfiles[-1], 2025)

    outputfiles.append('Jahreskalender_komplett_'+ version + '.pdf')
    generate_cal(data, 2025, outputfiles[-1], 'Milizfeuerwehr Basel-Stadt Jahreskalender 2025',
                 'Milizfeuerwehr Basel-Stadt', currentdate, version, holidays, additional_days)

    outputfiles.append('Jahresprogramm_komplett_' + version + '.ics')
    generate_ics(data, 2025, outputfiles[-1], version)

    data_kp = filter_dates(Groups.JF, data)
    old_data_kp = list(map(lambda old_version: filter_dates(Groups.JF, old_version), old_data))
    outputfiles.append('Jahresprogramm_JF_' + version + '.pdf')
    generate_pdf('Jahresprogramm JF', 'Jugendfeuerwehr', version, currentdate,
                 outputfiles[-1], data_kp, old_data_kp, old_versions)
    outputfiles.append('Jahreskalender_JF_' + version + '.pdf')
    generate_cal(data_kp, 2025, outputfiles[-1], 'Jugendfeuerwehr Jahreskalender 2025',
                 'Jugendfeuerwehr', currentdate, version, holidays, additional_days)
    outputfiles.append('Jahresprogramm_JF_' + version + '.ics')
    generate_ics(data_kp, 2025, outputfiles[-1], version)

    data_kp = filter_dates(Groups.RB, data)
    old_data_kp = list(map(lambda old_version: filter_dates(Groups.RB, old_version), old_data))
    outputfiles.append('Jahresprogramm_RB_' + version + '.pdf')
    generate_pdf('Jahresprogramm RB', 'Feuerwehr Riehen-Bettingen', version, currentdate,
                 outputfiles[-1], data_kp, old_data_kp, old_versions)
    outputfiles.append('Jahreskalender_RB_' + version + '.pdf')
    generate_cal(data_kp, 2025, outputfiles[-1], 'Feuerwehr Riehen-Bettingen Jahreskalender 2025',
                 'Feuerwehr Riehen-Bettingen', currentdate, version, holidays, additional_days)
    outputfiles.append('Jahresprogramm_RB_' + version + '.ics')
    generate_ics(data_kp, 2025, outputfiles[-1], version)

    data_kp = filter_dates(Groups.KB, data)
    old_data_kp = list(map(lambda old_version: filter_dates(Groups.KB, old_version), old_data))
    outputfiles.append('Jahresprogramm_KB_' + version + '.pdf')
    generate_pdf('Jahresprogramm KB', 'Feuerwehr Kleinbasel', version, currentdate,
                 outputfiles[-1], data_kp, old_data_kp, old_versions)
    outputfiles.append('Jahreskalender_KB_' + version + '.pdf')
    generate_cal(data_kp, 2025, outputfiles[-1], 'Feuerwehr Kleinbasel Jahreskalender 2025',
                 'Feuerwehr Kleinbasel', currentdate, version, holidays, additional_days)
    outputfiles.append('Jahresprogramm_KB_' + version + '.ics')
    generate_ics(data_kp, 2025, outputfiles[-1], version)

    data_kp = filter_dates(Groups.GB, data)
    old_data_kp = list(map(lambda old_version: filter_dates(Groups.GB, old_version), old_data))
    outputfiles.append('Jahresprogramm_GB_' + version + '.pdf')
    generate_pdf('Jahresprogramm GB', 'Feuerwehr Grossbasel', version, currentdate,
                 outputfiles[-1], data_kp, old_data_kp, old_versions)
    outputfiles.append('Jahreskalender_GB_' + version + '.pdf')
    generate_cal(data_kp, 2025, outputfiles[-1], 'Feuerwehr Grossbasel Jahreskalender 2025',
                 'Feuerwehr Grossbasel', currentdate, version, holidays, additional_days)
    outputfiles.append('Jahresprogramm_GB_' + version + '.ics')
    generate_ics(data_kp, 2025, outputfiles[-1], version)

    outputfiles.append('Änderungen_Jahresprogramm_' + version + '.pdf')
    generate_change_file(outputfiles[-1], data, version, old_data, old_versions, currentdate)

    shutil.rmtree('pdf/Jahresprogramm/', ignore_errors=True)
    shutil.rmtree('output/Jahresprogramm/', ignore_errors=True)
    os.mkdir('pdf/Jahresprogramm')
    for f in outputfiles:
        shutil.move('pdf/' + f, 'pdf/Jahresprogramm/')
    shutil.move('pdf/Jahresprogramm/', 'output/')

    tmp_files = ['outputrows.aux', 'outputrows.tex', 'outputrows.gen.log', 'outputrows.log', 'outputrows.out', 'outputrows.synctex.gz', 'addition.aux', 'addition.tex', 'addition.gen.log', 'addition.log', 'addition.out', 'addition.synctex.gz', 'Jahreskalender.aux', 'Jahreskalender.tex', 'Jahreskalender.gen.log', 'Jahreskalender.log', 'Jahreskalender.out', 'Jahreskalender.synctex.gz', 'Jahresprogramm.aux', 'Jahresprogramm.tex', 'Jahresprogramm.gen.log', 'Jahresprogramm.log', 'Jahresprogramm.out', 'Jahresprogramm.synctex.gz', 'Änderungen_Jahresprogramm.aux', 'Änderungen_Jahresprogramm.tex', 'Änderungen_Jahresprogramm.gen.log', 'Änderungen_Jahresprogramm.log', 'Änderungen_Jahresprogramm.out', 'Änderungen_Jahresprogramm.synctex.gz']

    for f in tmp_files:
        try:
            os.remove('pdf/' + f)
        except:
            pass