import os
import shutil
from datetime import date
from typing import List

import pandas as pd

from ej.scheduler.reporting.excel.convert_output import convert_output
from ej.scheduler.reporting.ics.ics_generation import generate_ics
from ej.scheduler.reporting.pdf.calendar_pdf_generation import generate_cal
from ej.scheduler.reporting.pdf.change_table_generation import generate_change_file
from ej.scheduler.reporting.pdf.programm_pdf_generation import generate_pdf
from ej.scheduler.util.date_utils import filter_events
from ej.scheduler.util.file_generation_utils import filter_dates, enumerate_names
from ej.scheduler.util.row_names import RowNames, Groups
from ej.scheduler.util.scheduler_config import SchedulerData

def generate_reports(version: str, old_versions: List[str], input_file_prefix: str, holiday_file_path: str,
                     additional_days_file_path: str, year, output_path:str):
    # version = '1.3'
    # old_versions = ['1.2', '1.1', '1.0']

    data = SchedulerData.create_from(input_file_prefix + version + '.xlsx').dates
    data.sort_values(by=RowNames.DATE.value, inplace=True)
    data = data[data[RowNames.INCLUDE.value] == True]

    old_data = list(
        map(lambda old_version: SchedulerData.create_from(input_file_prefix + old_version + '.xlsx').dates,
            old_versions))
    for index, old in enumerate(old_data):
        old_data[index] = old[old[RowNames.INCLUDE.value] == True]

    enumerate_names(data)

    currentdate = date.today().strftime('%d.%m.%Y')

    holidays = filter_events(pd.read_excel(holiday_file_path), year)
    additional_days = filter_events(pd.read_excel(additional_days_file_path), year)
    outputfiles = []

    outputfiles.append('Jahresprogramm_komplett_' + version + '.xlsx')
    convert_output(data, 'pdf/' + outputfiles[-1], year)

    outputfiles.append('Jahreskalender_komplett_' + version + '.pdf')
    generate_cal(data, year, outputfiles[-1], 'Milizfeuerwehr Basel-Stadt Jahreskalender ' + str(year),
                 'Milizfeuerwehr Basel-Stadt', currentdate, version, holidays, additional_days)

    outputfiles.append('Jahresprogramm_komplett_' + version + '.ics')
    generate_ics(data, year, outputfiles[-1], version)

    data_kp = filter_dates(Groups.JF, data)
    old_data_kp = list(map(lambda old_version: filter_dates(Groups.JF, old_version), old_data))
    outputfiles.append('Jahresprogramm_JF_' + version + '.pdf')
    generate_pdf('Jahresprogramm JF', 'Jugendfeuerwehr', year, version, currentdate,
                 outputfiles[-1], data_kp, old_data_kp, old_versions)
    outputfiles.append('Jahreskalender_JF_' + version + '.pdf')
    generate_cal(data_kp, year, outputfiles[-1], 'Jugendfeuerwehr Jahreskalender ' + str(year),
                 'Jugendfeuerwehr', currentdate, version, holidays, additional_days)
    outputfiles.append('Jahresprogramm_JF_' + version + '.ics')
    generate_ics(data_kp, year, outputfiles[-1], version)

    data_kp = filter_dates(Groups.RB, data)
    old_data_kp = list(map(lambda old_version: filter_dates(Groups.RB, old_version), old_data))
    outputfiles.append('Jahresprogramm_RB_' + version + '.pdf')
    generate_pdf('Jahresprogramm RB', 'Feuerwehr Riehen-Bettingen', year, version, currentdate,
                 outputfiles[-1], data_kp, old_data_kp, old_versions)
    outputfiles.append('Jahreskalender_RB_' + version + '.pdf')
    generate_cal(data_kp, year, outputfiles[-1], 'Feuerwehr Riehen-Bettingen Jahreskalender ' + str(year),
                 'Feuerwehr Riehen-Bettingen', currentdate, version, holidays, additional_days)
    outputfiles.append('Jahresprogramm_RB_' + version + '.ics')
    generate_ics(data_kp, year, outputfiles[-1], version)

    data_kp = filter_dates(Groups.KB, data)
    old_data_kp = list(map(lambda old_version: filter_dates(Groups.KB, old_version), old_data))
    outputfiles.append('Jahresprogramm_KB_' + version + '.pdf')
    generate_pdf('Jahresprogramm KB', 'Feuerwehr Kleinbasel', year, version, currentdate,
                 outputfiles[-1], data_kp, old_data_kp, old_versions)
    outputfiles.append('Jahreskalender_KB_' + version + '.pdf')
    generate_cal(data_kp, year, outputfiles[-1], 'Feuerwehr Kleinbasel Jahreskalender ' + str(year),
                 'Feuerwehr Kleinbasel', currentdate, version, holidays, additional_days)
    outputfiles.append('Jahresprogramm_KB_' + version + '.ics')
    generate_ics(data_kp, year, outputfiles[-1], version)

    data_kp = filter_dates(Groups.GB, data)
    old_data_kp = list(map(lambda old_version: filter_dates(Groups.GB, old_version), old_data))
    outputfiles.append('Jahresprogramm_GB_' + version + '.pdf')
    generate_pdf('Jahresprogramm GB', 'Feuerwehr Grossbasel', year, version, currentdate,
                 outputfiles[-1], data_kp, old_data_kp, old_versions)
    outputfiles.append('Jahreskalender_GB_' + version + '.pdf')
    generate_cal(data_kp, year, outputfiles[-1], 'Feuerwehr Grossbasel Jahreskalender ' + str(year),
                 'Feuerwehr Grossbasel', currentdate, version, holidays, additional_days)
    outputfiles.append('Jahresprogramm_GB_' + version + '.ics')
    generate_ics(data_kp, year, outputfiles[-1], version)

    outputfiles.append('Änderungen_Jahresprogramm_' + version + '.pdf')
    generate_change_file(outputfiles[-1], data, version, old_data, old_versions, currentdate, year)

    shutil.rmtree('pdf/Jahresprogramm_'+version+'/', ignore_errors=True)
    shutil.rmtree(output_path+'Jahresprogramm_'+version+'/', ignore_errors=True)
    os.mkdir('pdf/Jahresprogramm_'+version+'/')

    for f in outputfiles:
        shutil.move('pdf/' + f, 'pdf/Jahresprogramm_'+version+'/')
    shutil.move('pdf/Jahresprogramm_'+version+'/', output_path)

    tmp_files = ['outputrows.aux', 'outputrows.tex', 'outputrows.gen.log', 'outputrows.log', 'outputrows.out',
                 'outputrows.synctex.gz', 'addition.aux', 'addition.tex', 'addition.gen.log', 'addition.log',
                 'addition.out', 'addition.synctex.gz', 'Jahreskalender.aux', 'Jahreskalender.tex',
                 'Jahreskalender.gen.log', 'Jahreskalender.log', 'Jahreskalender.out', 'Jahreskalender.synctex.gz',
                 'Jahresprogramm.aux', 'Jahresprogramm.tex', 'Jahresprogramm.gen.log', 'Jahresprogramm.log',
                 'Jahresprogramm.out', 'Jahresprogramm.synctex.gz', 'Änderungen_Jahresprogramm.aux',
                 'Änderungen_Jahresprogramm.tex', 'Änderungen_Jahresprogramm.gen.log', 'Änderungen_Jahresprogramm.log',
                 'Änderungen_Jahresprogramm.out', 'Änderungen_Jahresprogramm.synctex.gz']

    for f in tmp_files:
        try:
            os.remove('pdf/' + f)
        except:
            pass
