from scapy.all import *
from optparse import OptionParser
 
VERBOSE = False 

def printer(*args, **kwargs):
    if VERBOSE:
        print(args, kwargs)

def max_silence_time(session):
   max_delta = 0
   first = True
   prev_time = 0
   for p in session:
      if first:
         first = False
         prev_time = p.time
      else:
         max_delta = max(p.time - prev_time, max_delta)
         prev_time = p.time
   return max_delta

def split2sessions(in_pcap):
   all = []
   sessions = in_pcap.sessions()

   max_delta = 0
   max_key = None
   for key, session in sessions.iteritems():
      ret = max_silence_time(session)
      print("flow: {}, max silence time: {}".format(key, ret))
      all.append(ret)
      if max_delta < ret:
         max_delta = ret
         max_key = key
      
   return all, key, max_delta 

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
    print split2sessions(pcap)

if __name__ == '__main__':
    main()
