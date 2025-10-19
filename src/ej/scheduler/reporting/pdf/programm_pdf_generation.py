import os
import shutil

from ej.scheduler.util.date_utils import convert_to_date, get_weekday_name
from ej.scheduler.util.file_generation_utils import translate_umlauts
from ej.scheduler.util.row_names import RowNames
from .change_table_generation import generate_change_table_tex


def generate_tex(data, year):
    with open('pdf/outputrows.tex', 'w') as output_file:
        i = 1
        for index, row in data.iterrows():
            tmp = generate_row(row, i, year)
            output_file.writelines(tmp)
            i += 1


def load_addition():
    with open('pdf/templates/addition_tmpl.tex', 'r') as file:
        return file.read()


def generate_addition_tex(data, version, old_data, old_versions):
    addition = load_addition()
    addition = addition.replace('$change_table', generate_change_table_tex(data, version, old_data, old_versions))
    with open('pdf/addition.tex', 'w') as output_file:
        output_file.write(addition)


def generate_pdf(title, displaytitle, year, version, date, filename, data, old_data, old_versions):
    print('Generating {}'.format(title))
    generate_tex(data, year)
    with open('pdf/templates/Jahresprogramm_tmpl.tex', 'r') as template:
        with open('pdf/Jahresprogramm.tex', 'w') as output:
            for line in template:
                line = line.replace('$title', title)
                line = line.replace('$displaytitle', displaytitle)
                line = line.replace('$version', version)
                line = line.replace('$date', date)
                line = line.replace('$year', str(year))
                output.write(line)

    generate_addition_tex(data, version, old_data, old_versions)

    cline = 'cd pdf && lualatex.exe -synctex=1 -interaction=nonstopmode Jahresprogramm.tex >> Jahresprogramm.gen.log'
    if os.system(str(cline)):
        raise RuntimeError('program {} failed!'.format(str(cline)))

    shutil.move('pdf/Jahresprogramm.pdf', 'pdf/' + filename)
    print('saved to pdf/{}'.format(filename))


def generate_row(series, index, year):
    # read file row_templ.tex
    with open('pdf/templates/row_tmpl.tex', 'r') as file:
        row = file.read()
        date = convert_to_date(series[RowNames.DATE.value], year)
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
