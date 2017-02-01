# importing the os package (see api at http://docs.python.org/2.6/library/io.html)
import os
# import function 'basename' from module os.path
from os.path import basename
# importing the sys package (see api at http://docs.python.org/2.6/library/sys.html)
import sys
import itertools
# importing the logging package (see api at http://docs.python.org/2.6/library/logging.html)
import logging
# by default Scapy attempts to find ipv6 routing information, 
# and if it does not find any it prints out a warning when running the module.
# the following statement changes log level to ERROR so that this warning will not 
# occur 
effective_level = logging.getLogger("scapy.runtime").getEffectiveLevel()
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
# importing Scapy
from scapy.all import PcapReader, PcapWriter, NoPayload
from scapy.layers.inet import IP 
from scapy.layers.inet6 import IPv6
from scapy.data import *
from scapy.layers.l2 import Ether
# return the log level o be what it was
logging.getLogger("scapy.runtime").setLevel(effective_level)
# unfortunately, somewhere in Scapy sys.stdout is being reset.
# thus, using the 'print' command will not produce output to the console.
# the following two lines place stdout back into sys.
if sys.stdout != sys.__stdout__:
    sys.stdout = sys.__stdout__

def get_ipv6_address_parts(address):
    addressLeft, addressRight=[x.split(":") for x in address.split("::")]
    return list(itertools.chain(addressLeft, addressRight))

def get_complete_ipv6_address_parts(address):
    addressLeft, addressRight=[x.split(":") for x in address.split("::")]
    addressZeros=["0" for i in range(0, 8-(len(addressLeft)+len(addressRight)))]
    return list(itertools.chain(addressLeft, addressZeros, addressRight))

def six2four(ipv6address):
    parts_list = get_ipv6_address_parts(ipv6address)
    if len(parts_list) > 4:
        parts_list = parts_list[len(parts_list) - 4:len(parts_list)]
    elif len(parts_list) < 4:
        parts_list = parts_list.insert([10] * (4 - len(parts_list)))
    
    for i in range(len(parts_list)):
        parts_list[i] = int(parts_list[i], 16) % 256
            
    if int(parts_list[0]) == 0:
        parts_list[0] = 10
    
    return parts_list
        
# this is a function declaration. there is no need for explicit types.
# python can infer an object type from its usage
def foo(in_filename, out_filename):
    # open the input file for reading
    f = PcapReader(in_filename)
    # open the output file for writing
    o = PcapWriter(out_filename)

    # read the first packet from the input file
    p = f.read_packet()

    # while we haven't processed the last packet
    while p:
        layer = p.firstlayer()
        while not isinstance(layer, NoPayload):
            if (type(layer) is IPv6):
                new_layer = IP()
                del new_layer.ihl
                new_layer.ttl = layer.hlim
                new_layer.proto = layer.nh
                new_layer.src = ".".join(map(str, six2four(layer.src)))
                new_layer.dst = ".".join(map(str, six2four(layer.dst)))
                new_layer.add_payload(layer.payload)
                prev_layer = layer.underlayer
                del layer
                prev_layer.remove_payload()
                prev_layer.add_payload(new_layer)
                if type(prev_layer) is Ether:
                    prev_layer.type = ETH_P_IP
                layer = new_layer
            
            if layer.default_fields.has_key('chksum'):
                del layer.chksum
            if layer.default_fields.has_key('len'):
                del layer.len
                
            # advance to the next layer
            layer = layer.payload

        # write the packet we just dissected into the output file    
        o.write(p)
        # read the next packet
        p = f.read_packet()
        
    # close the input file
    f.close()
    # close the output file
    o.close()
        
# i believe this is needed only if we are running the this module
# as the main module. i don't know if this will get executed if this module
# is imported into some other main module
if __name__ == "__main__":
    # letting the user know we are starting. 
    # sys.argv[0] includes the path to the module, including the module name.
    # convert sys.argv[0] into string, and extract the module name only
    # (using basename)
    print '===> Running', basename(str(sys.argv[0]))
    # making sure that two parameters were entered on the command line
    if (len(sys.argv) == 3):
        # get the path to the input file
        in_filename = str(sys.argv[1])
        # get the path to the output file
        out_filename = str(sys.argv[2])
        # make sure the input file actually exists.
        # if it doesn't, we print out an error and exit
        if os.path.exists(in_filename) == False:
            # note the method for entering conversion specifiers ({<ordinal>})
            sys.stderr.write("Either {0} does not exist, or you do not have proper permissions\n".format(in_filename))
        else:
            # if the input file does exist, execute 'foo'
            foo(in_filename, out_filename)
            # print an end script notification
            print basename(str(sys.argv[0])), '===> completed successfully'
    else:
        # write a USAGE message to the standard output stream
        sys.stderr.write("USAGE: {0} <path to input file> <path to output file>\n".format(basename(str(sys.argv[0]))))
