from dafact import Dafacter
import argparse
import sys


def main():
    # Handles arguments of xclingo
    parser = argparse.ArgumentParser(
        description='Dafact CLI\n\tEncodes data as ASP facts.')
    parser.add_argument('infile', type=str, help="Input csv file.")
    parser.add_argument('outfile',
                        type=argparse.FileType('w'),
                        help="Ouput ASP program.")
    group = parser.add_argument_group("Options")
    group.add_argument('--feature-names',
                       nargs='*',
                       default=None,
                       help="Feature names for the csv columns.")
    group.add_argument('--factor', type=int, default=0, help="factor help")
    group.add_argument('--numerical-columns',
                       nargs='*',
                       default=None,
                       help="Indexes for numerical columns.")
    group.add_argument(
        '--have-names',
        action='store_true',
        default=False,
        help="Must be if csv have the name of the columns in the first line.")
    group.add_argument(
        '--omit-names',
        action='store_true',
        default=False,
        help=
        "Used together with --have-names for omitting the names in the file.")
    group.add_argument('--delimiter',
                       type=str,
                       default=',',
                       help="Field delimiter for the csv file.")
    args = parser.parse_args()

    # Reads input files
    args.outfile.write(
        Dafacter(
            args.infile,
            feature_names=args.feature_names,
            numerical_columns=args.numerical_columns,
            have_names=args.have_names,
            omit_names=args.omit_names,
            delimiter=args.delimiter,
        ).as_program_string(factor=args.factor))


if __name__ == "__main__":
    main()
