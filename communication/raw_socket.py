import socket
import struct
import ssl

import pclient

pclient.SERVER = SERVER = 'www.facebook.com'
pclient.SRC_IP = SRC_IP = '10.168.13.85'
pclient.PORT = PORT = 41444

client_hello = [0x16, 0x03, 0x01, 0x00, 0x6c, 0x01, 0x00, 0x00,
0x68, 0x03, 0x01, 0x56, 0x5c, 0x8a, 0x56, 0xf1, 
0x7e, 0xa0, 0x69, 0x41, 0xf7, 0x30, 0xf5, 0x12, 
0x3d, 0x28, 0xc2, 0x3c, 0xd1, 0xda, 0x5b, 0xf6, 
0x98, 0xf2, 0xf5, 0x0b, 0x44, 0xbe, 0x42, 0x1d, 
0x63, 0xa2, 0x62, 0x00, 0x00, 0x3a, 0x00, 0x39, 
0x00, 0x38, 0x00, 0x88, 0x00, 0x87, 0x00, 0x35, 
0x00, 0x84, 0x00, 0x16, 0x00, 0x13, 0x00, 0x0a, 
0x00, 0x33, 0x00, 0x32, 0x00, 0x9a, 0x00, 0x99, 
0x00, 0x45, 0x00, 0x44, 0x00, 0x2f, 0x00, 0x96, 
0x00, 0x41, 0x00, 0x05, 0x00, 0x04, 0x00, 0x15, 
0x00, 0x12, 0x00, 0x09, 0x00, 0x14, 0x00, 0x11, 
0x00, 0x08, 0x00, 0x06, 0x00, 0x03, 0x00, 0xff, 
0x02, 0x01, 0x00, 0x00, 0x04, 0x00, 0x23, 0x00, 
0x00]
        
def send_data(s, raw_bytes_list):
    ba = bytearray(client_hello)
    
    s.send(ba)
    print "data sent"

    data = s.recv(4096)
    total_data = data
    i = 0
    while (len(total_data)<2800):
        print "r #", i
        i = i + 1
        data = s.recv(4096)
        total_data = total_data + data
    print "total data read:", len(total_data)   
    #print('data: {d}'.format(d=total_data))

def get_data(ssl_socket):
    print "GET-ing data"
    ssl_socket.send("GET / HTTP/1.1\r\n\r\n")
    print "r #0"
    data = ssl_socket.recv(4096)
    total_data = data
    i = 0
    while (len(data)==4096):
        print "r #", i
        i = i + 1
        data = ssl_socket.recv(4096)
        total_data = total_data + data

def make_connection():
    print "connect until server-hello"
    print "=========================="
    connect_until_server_hello()

    #print "full connection"
    #print "=========================="
    #pclient.main()
    


def connect_until_server_hello():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)                    
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((SRC_IP, PORT))
    print('connecting to: {c}:443'.format(c=SERVER))
    #print('sleeping...')
    
    try:
        s.connect((SERVER, 443))
        #time.sleep(1)
        print('connected from: {c}'.format(c=s.getsockname()))

        # send client-heelo message and recieve server-hello + cert. + sever-hello-done
        send_data(s, client_hello)

        # close the connection gracefully
        s.close()

        print
        print "reconnecting"
        print
        #make a ssl connection
        #s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)                    
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((SRC_IP, PORT))
        sec_s = ssl.wrap_socket(s, 
                    keyfile = None,                         # no key file to use as a client (we don't use a client cert.)
                    certfile = None,                        # no cert. to provide as a client
                    server_side = False,                    # we are a client 
                    cert_reqs = ssl.CERT_REQUIRED,          # we want a cert. to be supplied by the server
                    ssl_version = ssl.PROTOCOL_TLSv1,       # use TLSv1
                    ca_certs = "/etc/ssl/certs/ca-bundle.crt", #CA_CERTS, #None,             # use default CA certs. for validation (whatever the OS uses)
                    do_handshake_on_connect = True,         
                    suppress_ragged_eofs = True, 
                    ciphers = None)

        sec_s.connect((SERVER, 443))
        #time.sleep(1)
        print('connected from: {c}'.format(c=sec_s.getsockname()))

        get_data(sec_s)

        sec_s.shutdown(socket.SHUT_RDWR)
        sec_s.close()

    except Exception as e:
        print "caught exception:", e



def main():
    make_connection()

if __name__ == '__main__':
    main()
