from optparse import OptionParser
import sys

class InputOutputFilesOptions(object):
    def __init__():
        pass

    @staticmethod
    def ParseOptions():
        parser = OptionParser()
        parser.add_option("-i", "--in_file", dest="in_file", action='store', nargs=1, help="file to process")
        parser.add_option("-o", "--out_file", dest="out_file", action='store', nargs=1, help="output file name")

        (options, args) = define_cli_options().parse_args(args=sys.argv[1:],)

