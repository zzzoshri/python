from optparse import OptionParser
import sys

def main():
    parser = OptionParser()
    parser.add_option("-i", "--in_file", dest="in_file", action='store', nargs=1, help="file to process")
    (options, args) = parser.parse_args(args=sys.argv[1:],)

    print options.in_file

if __name__ == '__main__':
    main()
