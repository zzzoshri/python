import socket
import ssl

CIPHERS = ""

def sendData(ssl_socket):
    pass

context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
context.verify_mode = ssl.CERT_REQUIRED
context.check_hostname = True
context.load_default_certs()

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #sec_s = ssl.wrap_socket(s, 
    #        keyfile = None,                         # no key file to use as a client (we dont't use a client cert.)
    #        certfile = None,                        # no cert. to provide as a client
    #        server_side = False,                    # we are a client 
    #        cert_reqs = ssl.CERT_REQUIRED,          # we want a cert. to be supplied by the server
    #        ssl_version = ssl.PROTOCOL_TLSv1,       # use TLSv1
    #        ca_certs = ssl.enum_certificates("ROOT"), #"/etc/ssl/certs/ca-bundle.crt", #None,                        # use default CA certs. for validation (whatever the OS uses)
    #        do_handshake_on_connect = True,         
    #        suppress_ragged_eofs = True, 
    #        ciphers = None)
    
    #sec_s = context.wrap_socket(s, server_hostname='facebook.com')
    #sec_s.connect(('facebook.com', 443))
    s.connect(('10.168.163.216', 443))
        
    #sendData(sec_s)
except Exception as e:
    print e
    pass
finally:
    #sec_s.close()
    print "wait for input"
    raw_input()
    s.close()
