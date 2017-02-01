import socket
import ssl
import sys
import time
import platform

# GLOBALS
CIPHERS = ''
SERVER = ''
OS = ''
CA_CERTS = ''
SRC_IP = ''
PORT = 44644

def config_ca_certs():
    OS = platform.system()
    print "platform system:", OS
    if OS == 'Windows':
        CA_CERTS = ssl.enum_certificates("ROOT")
    elif OS == 'Linux':
        CA_CERTS = "/etc/ssl/certs/ca-bundle.crt"

if len(sys.argv) > 2:
    SERVER = sys.argv[1]
else:
    SERVER = 'www.facebook.com'

if len(sys.argv) > 3:
    CIPHERS = sys.argv[2]
else:
    CIPHERS = ''

def sendData(ssl_socket):
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
        
    print('data: {d}'.format(d=total_data))

def make_connection():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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
                    
    sec_s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sec_s.bind((SRC_IP, PORT))
    print('connecting to: {c}:443'.format(c=SERVER))
    #print('sleeping...')
    
    try:
        sec_s.connect((SERVER, 443))
        #time.sleep(1)
        print('connected from: {c}'.format(c=sec_s.getsockname()))

        sendData(sec_s)
    except Exception as e:
        print "1) Exception caught:", e
    finally:
        try:
            stats = sec_s.session_stats()
            print stats
            print "shutting down the connection"
            sec_s.shutdown(socket.SHUT_RDWR)
            sec_s.close()
        except Exception as ee:
            print "shutting down the connection"

    #sec_s.shutdown(socket.SHUT_RDWD)
    #
    
    
def main():
    print('starting test')
    
    config_ca_certs()
    
    for i in xrange(1):
        print('connection #{c}'.format(c=i))
        make_connection()
    
    print('test finished')
    
if __name__ == '__main__':
    main()
