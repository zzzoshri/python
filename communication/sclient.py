from scapy.all import *
import random
import sys

dns_map = {'facebook.com': '69.171.230.68',
           'www.google.com': '173.194.116.208',
           'www.yahoo.com': '46.228.47.114',
           'vimeo.com': '104.156.81.217',
           'payonline.fluidbranding.com': '81.133.14.166',
           'kyselyt-t.luke.fi': '213.138.153.185',
           'www.twitter.com': '104.244.42.1',
           'www.youtube.com': '173.194.116.206',
           'mail.google.com': '173.194.116.213',
           'www.example.com': '93.184.216.34',
           'http2.akamai.com': '23.221.135.45',
           's.yimg.com': '188.125.93.156',
           'www.linkedin.com': '185.63.147.10',
           'some.yahoo.com': '217.12.15.54',
           'test1_RST': '212.25.105.53'}

DEST_IP = dns_map['test1_RST']
#SRC_PORT = int(sys.argv[1])


pkts = rdpcap("client_hello.pcap")
CLIENT_HELLO_DATA = str(pkts[0][3])


def main():

    SEQ_NUM = 1
    ACK_NUM = 0
    
    ip = IP(src="10.168.13.91", dst=DEST_IP)

    tcp = TCP(sport=SRC_PORT, dport=443, seq=SEQ_NUM)

    syn_packet = ip/tcp
    syn_packet.payload.flags="S"

    # send SYN and get SYN+ACK
    syn_ack_packet = sr1(syn_packet,inter=0.5,retry=-4,timeout=1)
    
    # create ACK base on SYN+ACK
    ACK_NUM = syn_ack_packet.seq+1
    SEQ_NUM = SEQ_NUM + 1
    
    ack_packet = ip/tcp
    ack_packet.payload.flags="A"
    ack_packet.seq = SEQ_NUM
    ack_packet.ack = ACK_NUM
    
    # send the final ack in the 3-way handshake
    send(ack_packet)
       
    # send client-hello
    data = ack_packet/CLIENT_HELLO_DATA
    data.seq = SEQ_NUM
    sh = sr(data, multi=1, timeout=1.6)
    
    ans, unans = sh

    total_l4_data = 0
    for snd, rcv in ans:
        if len(rcv[TCP].payload) > 10:
            total_l4_data += len(rcv[TCP].payload)

    print "recv", total_l4_data
    
    SEQ_NUM += len(CLIENT_HELLO_DATA)
    ACK_NUM += total_l4_data
    
    print "sending FIN/ACK"
    # send fin-ack
    ack_packet = ip/tcp
    ack_packet.payload.flags="FA"
    ack_packet.ack = ACK_NUM
    ack_packet.seq = SEQ_NUM
    
    sh2 = sr(ack_packet, multi=1, timeout=1.6)
    
    ACK_NUM += 1
    SEQ_NUM += 1
    
    # send fin-ack
    ack_packet = ip/tcp
    ack_packet.payload.flags="A"
    ack_packet.ack = ACK_NUM
    ack_packet.seq = SEQ_NUM
    
    sh2 = send(ack_packet)

if __name__ == '__main__':
    # generate random src port in [20000, 65535]
    SRC_PORT = random.randrange(20000, 65535)
    for i in range(10):
        main()
