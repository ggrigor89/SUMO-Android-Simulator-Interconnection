# -*- coding: utf-8 -*-
"""
Created on Wed Jul 17 19:50:52 2019

@author: ggrig
"""

import socket
import sys
import struct

# Create a TCP/IP socket
# The client program sets up its socket differently from the way a server does. Instead of binding to a port and listening, it uses connect() to attach the socket directly to the remote address.


#def example():
#    HOST = '127.3.3.1'  # Standard loopback interface address (localhost)
#    PORT = 65432        # Port to listen on (non-privileged ports are > 1023)
#    
#    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#    
#    # Connect the socket to the port where the server is listening
#    server_address = (HOST, PORT)
#    print (sys.stderr, 'connecting to ', server_address)
#    sock.connect(server_address)
#    
#    # After the connection is established, data can be sent through the socket with sendall() and received with recv(), just as in the server.
#    
#    try:
#        
#        # Send data
#        message = 1231231412558798679090
#        print (sys.stderr, 'sending ', message)
#        sock.sendall(str(message).encode("Utf-8")) #use .encode("Utf-8") for strings
#        
#        # Look for the response
#        amount_received = 0
#        amount_expected = len(str(message))
#        
#        while amount_received < amount_expected:
#            data = sock.recv(16)
#            amount_received += len(data)
#            print (sys.stderr, 'received ',data)
#    
#    finally:
#        print (sys.stderr, 'closing socket')
#        sock.close()
            
def transmit(message):

    HOST = '25.122.134.254'  # Standard loopback interface address (localhost) 25.122.134.254
    PORT = 90        # Port to listen on (non-privileged ports are > 1023)
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Connect the socket to the port where the server is listening
    server_address = (HOST, PORT)
    print (sys.stderr, 'connecting to ', server_address)
    sock.connect(server_address)
    
    # After the connection is established, data can be sent through the socket with sendall() and received with recv(), just as in the server.
    
    try:
        
        # Send data
#        print (sys.stderr, 'sending ', message)
        sock.sendall(message.encode("Utf-8")) #use .encode("Utf-8") for strings
#        sock.sendall(message) #use .encode("Utf-8") for strings
    
        # Look for the response
        amount_received = 0
        amount_expected = 2*len(str(message))
        
        while amount_received < amount_expected:
            data_rc = sock.recv(1024)
            amount_received += len(data_rc)
#            print (sys.stderr, 'received data_rc ',data_rc)
            return data_rc
    
    finally:
#        print (sys.stderr, 'closing socket')
        sock.close()        