from scapy.all import *
from optparse import OptionParser
 
VERBOSE = False 

def printer(*args, **kwargs):
    if VERBOSE:
        print(args, kwargs)


def split2sessions(in_pcap):
   printer(in_pcap.summary())
   sessions = in_pcap.sessions()

   for i, session_tupple in enumerate(sessions.iteritems()):
       out_filename = "stream_{num}.pcap".format(num=i)
       wrpcap(out_filename, session_tupple[1])

    

def define_cli_options():
    parser = OptionParser()
    parser.add_option("-i", "--in_file", dest="in_file", action='store', nargs=1, help="file to process")
    parser.add_option("-v", "--verbose", dest="verbose", action='store_true', help="be verbose")

    return parser

def main():
    (options, args) = define_cli_options().parse_args(args=sys.argv[1:],)

    if options.verbose:
        VERBOSE = True

    try:
        pcap = rdpcap(options.in_file)
    except IOError as io_exception:
        print("file: {fn}".format(fn=options.in_file))
        print io_exception
        exit()
    except IndexError as index_exception:
        print("no argv[1]")
        print index_exception
        exit()

    print("splitting pcap {p} to sessions".format(p=options.in_file))
    split2sessions(pcap)

if __name__ == '__main__':
    main()
