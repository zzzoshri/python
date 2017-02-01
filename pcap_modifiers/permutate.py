from scapy.all import *
import sys
from optparse import OptionParser

DEBUG = False 

def print_debug(msg):
    global DEBUG
    if DEBUG:
        print(msg)

def add_vlan(in_pcap, in_vid):
    out_pcap = []

    print_debug("pcap size: " + str(len(in_pcap)))

    for idx, packet in enumerate(in_pcap):
        # gets the first layer of the current packet
        layer = packet.firstlayer()
        # loop over the layers
        while not isinstance(layer, NoPayload):
        
            if 'chksum' in layer.default_fields:
                del layer.chksum

            if (type(layer) is Ether):
                # adjust ether type
                layer.type = 33024
                # add 802.1q layer between Ether and IP
                dot1q = Dot1Q(vlan=int(in_vid))
                dot1q.add_payload(layer.payload)
                layer.remove_payload()
                layer.add_payload(dot1q)
                layer = dot1q
                  
            # advance to the next layer
            layer = layer.payload

        out_pcap.append(packet)

    return out_pcap

def define_cli_options():
    parser = OptionParser()
    parser.add_option("-i", "--in_file", dest="in_file", action='store', nargs=1, help="file to process")
    parser.add_option("-o", "--out_file", dest="out_file", action='store', nargs=1, help="output file name")
    parser.add_option("-v", "--vid", dest="vid", action='store', nargs=1, help="VLAN ID to add")

    return parser

def main():
    (options, args) = define_cli_options().parse_args(args=sys.argv[1:],)

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

    print_debug("modifying input pcap file")
    out_pcap = add_vlan(pcap, options.vid)

    print_debug("saving modified pcap to file:" + options.out_file)
    wrpcap(options.out_file, out_pcap)





if __name__ == '__main__':
    main()
