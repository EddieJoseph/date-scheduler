import argparse

from ej.scheduler.generate_output import generate_reports
from ej.scheduler.schedule import optimize


def parse_args():
    parser = argparse.ArgumentParser(prog='date_scheduler', description='Date Scheduling Tool')

    subparser = parser.add_subparsers(dest='command', required=True)

    parser_optimize = subparser.add_parser('optimize', help='Optimize dates')
    parser_optimize.add_argument('-i', '--input', help='Input file', required=True)
    parser_optimize.add_argument('-y', '--year', help='Year', type=int, required=True)
    parser_optimize.add_argument('-o','--output', help='Output file prefix', default='data')
    parser_optimize.add_argument('-H', "--holidays", help="Holidays file", required=True)
    parser_optimize.add_argument( "--random-seed", help="Holidays file", type=int)

    parser_generate = subparser.add_parser('generate', help='Generate report')
    parser_generate.add_argument('-i', '--input', help='Input file prefix', required=True)
    parser_generate.add_argument('-H', "--holidays", help="Holidays file", required=True)
    parser_generate.add_argument('-a', "--additional-dates", help="Additional date file", required=True)
    parser_generate.add_argument('-y', '--year', help='Year', type=int, required=True)
    parser_generate.add_argument('-v', '--version', help='Version', required=True)
    parser_generate.add_argument('-o', '--old-versions', help='Old versions', required=False)
    parser_generate.add_argument('-p', '--output-path', help='Output Folder', required=True)
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()

    if(args.command == 'optimize'):
        print("Starting optimization")
        print(args.input)
        print(args.year)
        print(args.output)
        print(args.holidays)
        print(args.random_seed)
        if args.random_seed:
            optimize(args.input, args.holidays, args.output, args.year, args.random_seed)
        else:
            optimize(args.input, args.holidays, args.output, args.year)

    elif(args.command == 'generate'):
        print("Starting report generation")
        print(args.input)
        print(args.holidays)
        print(args.additional_dates)
        print(args.year)
        print(args.version)

        old_versions = []
        if args.old_versions:
            old_versions = list(reversed(args.old_versions.split(',')))

        generate_reports(args.version,old_versions, args.input, args.holidays, args.additional_dates, args.year, args.output_path)