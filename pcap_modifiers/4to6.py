from scapy.all import *
import sys
from optparse import OptionParser

def ipnumber(ip):
    ip=ip.rstrip().split('.')
    ipn=0
    while ip:
        ipn=(ipn<<8)+int(ip.pop(0))
    return ipn

def convertV4toV6(pcapname,outpcap):
    pcap = rdpcap(pcapname)
    newpcap = []
    bailing = 0
    for i in range (0, len(pcap)):
        #if it is IPv6 bail to save time
        if(pcap[i].haslayer(IPv6)):
            bailing = 1
            break
        #before we even start check for frag, if fragged bail... for now.
        if (pcap[i][IP].flags == 4L or pcap[i][IP].frag != 0L):
            print "Do not support Fragment at this time, packet " + str(i) + " failed"
            bailing = 1
            break
        src = ipnumber(pcap[i][IP].src)
        dst = ipnumber(pcap[i][IP].dst)
        src = hex(src)
        src = src.rstrip().split('0x')
        src = src.pop(1)
        v6src = src[0:4] + ':' + src[4:8]
        dst = hex(dst)
        dst = dst.rstrip().split('0x')
        dst = dst.pop(1)
        v6src = src[0:4] + ':' + src[4:8]
        v6dst = dst[0:4] + ':' + dst[4:8]
        ethersrc = pcap[i][Ether].src
        ethersrc = ethersrc.rstrip().split(':')
        etherdst = pcap[i][Ether].dst
        etherdst = etherdst.rstrip().split(':')
        v6src = '2011::1:' +v6src
        v6dst = '2011::1:' +v6dst
        # replace the header
        #print v6src + " " + v6dst + "packet is: " +  str(i)
        if pcap[i].haslayer(IP):
            if pcap[i].haslayer(TCP):
                del(pcap[i][TCP].chksum)
            if pcap[i].haslayer(UDP):
                del(pcap[i][UDP].chksum)
            del(pcap[i][IP].chksum)
            del(pcap[i][IP].len)
            if pcap[i].haslayer(Padding):
                del(pcap[i][Padding])
                #the IPv6 header length is 40.
                if len(pcap[i][IP].payload) < 6:
                    pcapload = ''.join(['0' for num in xrange(0,6-len(pcap[i][IP].payload))])
                    pcap[i] = pcap[i]/Padding(load=pcapload)
      
        newpcap.append(Ether(src=pcap[i][Ether].src,dst=pcap[i][Ether].dst,type=0x86dd)/IPv6(nh=pcap[i][IP].proto,src=v6src, dst=v6dst)/pcap[i][IP].payload)
        newpcap[i].time = pcap[i].time
    if (bailing != 1):
        wrpcap(outpcap,newpcap)

def TruncateV6Data(pcapname):
    pcap = rdpcap(pcapname)
    for i in range (0, len(pcap)):
        if (len(pcap[i]) > 1500):
            if (pcap[i].haslayer(TCP)):
                pcap[i][Raw].load = pcap[i][Raw].load[0:1426]
                del(pcap[i][TCP].chksum)
            if (pcap[i].haslayer(UDP)):
                pcap[i][Raw].load = pcap[i][Raw].load[0:1438]
                del(pcap[i][UDP].chksum)
                del(pcap[i][UDP].len)
        del(pcap[i][IPv6].plen)
    wrpcap(pcapname,pcap)

def define_cli_options():
    parser = OptionParser()
    parser.add_option("-i", "--in_file", dest="in_file", action='store', nargs=1, help="file to process")
    parser.add_option("-o", "--out_file", dest="out_file", action='store', nargs=1, help="output file name")
    parser.add_option("-v", "--vid", dest="vid", action='store', nargs=1, help="VLAN ID to add")

    return parser

def main():
    (options, args) = define_cli_options().parse_args(args=sys.argv[1:],)

    try:
        convertV4toV6(options.in_file, options.out_file)
    except IOError as io_exception:
        print io_exception
        exit()
    except IndexError as index_exception:
        print("no argv[1]")
        print index_exception
        exit()

if __name__ == '__main__':
    main()
