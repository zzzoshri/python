'''
Created on Jun 12, 2013

@author: MDorsett
'''
import os
import sys
from struct import *
from packety.all import *
from copy import deepcopy
from msd_utils import hexdump

def four2six(in_filename, out_filename):
    with packet_file(in_filename, 'r') as in_file:
        with packet_file(out_filename, 'w', format=type(in_file), linktype=PcapHeader.Networks.Ethernet) as out_file:
            i = 0
            for packet in in_file:
                i += 1

                if not IPv4 in packet:
                    out_file.write(packet)
                    continue
                layer = packet[Ethernet]
                a = [layer]
                while isinstance(layer.data,Packet):
                    layer = layer.data
                    a.append(layer)
                   
                found_ip = False 
                additional_length = 0
                six = None
                six_needs_mounting = False
                for l in reversed(a):
                    if found_ip == True:
                        if six_needs_mounting == True:
                            six_needs_mounting = False
                            l.data = six
                            if isinstance(l, Ethernet):
                                l[Ethernet].type = Ethernet.Types.IPv6
                            elif isinstance(l, IPv4):
                                l[IPv4].protocol = IP.Protocols.IPv6
                            elif isinstance(l, IPv6):
                                l[IPv6].next_header = IP.Protocols.IPv6
                            elif isinstance(l, PPP):
                                l[PPP].protocol = PPP.Types.IPv6
                        if l.has_field("length"):
                            l.length += additional_length
                    elif isinstance(l, IPv4):
                        found_ip = True
                        if l[IPv4].flags.more_fragments or l[IPv4].fragment_offset:
                            print "fragment found in packet", i
                            break
                        else:    
                            six = l[IPv4].to_ipv6()
                        six_needs_mounting = True
                        temp = deepcopy(six)
                        del temp.data
                        additional_length = len(temp)
                        six.payload_len = len(six.data)
                        six.next_header = l[IPv4].protocol
                        del l[IPv4].data
                        additional_length = additional_length - len(l[IPv4].data)
                        
                l.defaults(True)
                out_file.write(l)
                
                """ 
                if i % 100 == 0:
                    print i, "records processed"
                """
            print "processing complete.", i, "records processed."

if __name__ == "__main__":
    if (len(sys.argv) == 3):
        in_filename = str(sys.argv[1])
        out_filename = str(sys.argv[2])
        if os.path.exists(in_filename) == False:
            sys.stderr.write("Either {0} does not exist, or you do not have proper permissions\n".format(in_filename))
        else:
            sys.stdout.write("----> Starting to process file\n")
            four2six(in_filename, out_filename)
            sys.stdout.write("----> Finished processing file successfully\n")
    else:
        sys.stderr.write("USAGE: {0} <path to input file> <path to output file>\n".format(str(sys.argv[0])))
        
        