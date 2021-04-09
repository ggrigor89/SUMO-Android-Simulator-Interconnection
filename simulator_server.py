# -*- coding: utf-8 -*-
"""
Created on Wed Jul 17 19:12:18 2019

@author: ggrig
"""

"""https://www.afternerd.com/blog/python-http-server/ or https://pymotw.com/2/socket/tcp.html"""

"""By default, the port number is 80 for http and 443 for https"""

import http.server
import socketserver
import socket
import sys
import json
import time
import threading
from queue import Queue

NUMBER_OF_THREADS = 3
JOB_NUMBER =[1,2,3]#1 
queue = Queue()
all_connections = []
all_address = []
all_client_types = []

#def create_server():
"""create a functional https server""" 
HOST = '25.122.134.254'  # Standard loopback interface address (localhost) 25.122.134.254
PORT = 80        # Port to listen on (non-privileged ports are > 1023)
#HOST = r'//402f6729.ngrok.io'
#PORT = 80pw
#DEVICE_IP = "25.122.140.13"
DEVICE_IP = "25.22.76.201"

client_id = "SERVER"
client_SUMO = "SUMO"
shared_listSM =[]
shared_listMS =[]


def create_server_socket(client_type):
    # Create a TCP/IP socket
    if client_type == client_SUMO:
        PORT = 90
    else: 
        PORT = 80    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (HOST, PORT)
    print (sys.stderr, 'starting up on ',server_address,' port ',sock.bind(server_address))
    sock.listen(1)
    Server_STATUS = True #True ON, False OFF
    return sock



def create_workers():
    '''Create worker threads'''
    for i in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work)
        t.daemon = True#tells program to end the thread if program ends
        t.start()

#Do next job in queue (1 handle connection 2 send commands)
def work():
    while True:
        x = queue.get()
        
        if x == 1:
            sock = create_server_socket("SUMO")            
            accepting_connections(sock,"SUMO")
            
        if x ==2:
            connection_handle()
            
        if x == 3:
            sock = create_server_socket("MOBILE")                        
            accepting_connections(sock,"MOBILE")
            
        queue.task_done()    

def create_jobs():
    for x in JOB_NUMBER:
        queue.put(x)
    queue.join()
    

#https://402f6729.ngrok.io

def client_type(ip):
    if ip == DEVICE_IP:
        return "MOBILE"
    else:
        return "SUMO"
        

def client_id_check(c_id):
    '''corrects the client id for message transmission'''
    if c_id != client_id:
        return client_id


def example_operation(data,current_time):
    '''executes a simple example operation in server, transmits back the result to the client and enforces a specific change in SUMO'''
    d = json.loads(data)
    d["color"] = (255,192,203)
    d["client_id"] = client_id_check(d["client_id"])
    d["smartphone"] = current_time
    return d



#Handling connections from multiple clients and saving to a list
#closing previous connections 
    
def accepting_connections(sock,c_type_client):
    for c in all_connections:
        c.close()
        
    del all_connections[:]
    del all_address[:]
    while True:
        try: 
            conn, address = sock.accept()
            sock.setblocking(1) #prevents timeout
            c_type = client_type(address[0])
            if c_type_client !=c_type:
                continue
            all_connections.append(conn)
            all_address.append(address)
            all_client_types.append(c_type)
            print("connection has been established "+address[0]+address[1]+str(len(all_connections)))
        except:
#            print("Error accepting connection")
            continue
            
#2nd thread 1) See all clients and send commands           
            
            
def connection_handle():
    while True:
        results_conn,results_add,results_types = list_connections()
        for i in range(len(results_conn)):
                conn = results_conn[i]
                c_type = results_types[i]
                address = results_add[i]
                send_target_commands(conn,address,c_type)
            #add ip identifier sumo mobile
    
def list_connections():
    results_conn = []
    results_add = []
    results_types = []
    
    for i in range(len(all_connections)):
        try:
                conn = all_connections[i]   
                message1 = 'ServerStartStream'
                conn.sendall(message1.encode("Utf-8"))       
#                data = conn.recv(10240)
            
        except:
            continue
        results_conn.append(conn)
        results_add.append(all_address[i])
        results_types.append(all_client_types[i])
    return results_conn,results_add,results_types 


def send_target_commands(connection,client_address,c_type):
    control = True
    try:
#        print ("CLIENT TYPE IS "+c_type)
        if c_type == "MOBILE":
            '''Server to Smartphone Client Communication'''
            while control == True:
#                print (sys.stderr, 'connection from mobile device', client_address)
                
                data = connection.recv(10240)
#                print (sys.stderr, 'received ',data)
                if data:
                    if data == "CC":
                        print ("end CC from client")
                        # Clean up the connection
                        connection.close()
                        break
                    t = time.localtime()

#                    print ("data received at server ",data)
#                    print (sys.stderr, 'sending data back to the client mobile device')   
                    output_string ="simple_test_12"
                    output_dict = {"server_to_android":"sta","id":"1","angle":12,"speed":12}
                    output_json = json.dumps(output_dict)                    
#                    print (type(data),data)
#                    When reading data in bytes, we need to define our own protocol for communication between server and client. The simplest protocol which we can define is called TLV (Type Length Value). It means that every message written to the socket is in the form of the Type Length Value.
#           
#So we define every message sent as:
#
#A 1 byte character that represents the data type, like s for String
#A 4 byte integer that indicates the length to the data
#And then the actual data, whose length was just indicated
#                    print (type(bytes(b'ABCD')),b'ABCD')
#                    message = 'sID:ABCD_EFG113\n speed:12\n angle:45.12\n'
                    message1 = 'sID:ABCD_EFG113\n'
                    connection.sendall(message1.encode("Utf-8"))
                    

                    current_time = time.strftime("%H:%M:%S", t)
                    
                    print (current_time, " MOBILE")
                    
                    
                    
                    message2 = 'speed:12\n'
                    
                    connection.sendall(message2.encode("Utf-8"))                    

                    message3 = 'angle:45.12\n'
                    connection.sendall(message3.encode("Utf-8"))

                    try:
                        current_time = shared_listSM[-1]
                    except:    
                        current_time = time.strftime("%H:%M:%S", t)

                    print (shared_listSM)
                    message4 = 'timeserver_'+current_time+'\n'
                    connection.sendall(message4.encode("Utf-8"))  
                    
                    shared_listMS.append("MOBILE_"+data.decode("utf-8")+"_"+current_time)
                    
                     
                    
#                    connection.sendall(output_string)
                    control = False
                else:
#                    print (sys.stderr, 'no more data from mobile device', client_address)
                    control = True
                    connection.close()
                    
                    break            
        elif c_type == "SUMO":
#            print (sys.stderr, 'connection from client', client_address)
            
        # Receive the data in small chunks and retransmit it
            while control == True:
                
                data = connection.recv(10240)
#                print (sys.stderr, 'received ',data)
                if data:
#                    print ("data received at server from SUMO ",data)
                    t = time.localtime()
                    try:
                        current_time = shared_listMS[-1]
                    except:    
                        current_time = time.strftime("%H:%M:%S", t)                    
                    data_cl = json.dumps(example_operation(data,current_time))
#                    print (sys.stderr, 'sending data back to the client')
                    connection.sendall(data_cl.encode("Utf-8"))
                    control = False
                    
                    current_time = time.strftime("%H:%M:%S", t)
                    print (shared_listMS)
                    
                    print (current_time, " SUMO")
                    shared_listSM.append("SUMO_"+current_time)
                else:
                    control = True
                    connection.close()
                    
#                    print (sys.stderr, 'no more data from', client_address)
                    break
            
    finally:
#        print ("end")
        # Clean up the connection
        connection.close()
    

create_workers()
create_jobs()


## Create a TCP/IP socket
#sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#server_address = (HOST, PORT)
#print (sys.stderr, 'starting up on ',server_address,' port ',sock.bind(server_address))
#sock.listen(1)
#Server_STATUS = True #True ON, False OFF
#
#while Server_STATUS:
#    # Wait for a connection
#    print (sys.stderr, 'waiting for a connection')
#    connection, client_address = sock.accept()
##    print (sys.stderr, 'connection from ', client_address, " established")
#    control = True
#    try:
#        if client_address[0]==DEVICE_IP:
#            '''Server to Smartphone Client Communication'''
#            while control == True:
#                print (sys.stderr, 'connection from mobile device', client_address)
#                
#                data = connection.recv(10240)
##                print (sys.stderr, 'received ',data)
#                if data:
#                    if data == "CC":
#                        print ("end CC from client")
#                        # Clean up the connection
#                        connection.close()
#                        break
#                    print ("data received at server ",data)
##                    print (sys.stderr, 'sending data back to the client mobile device')   
#                    output_string ="simple_test_12"
#                    output_dict = {"server_to_android":"sta","id":"1","angle":12,"speed":12}
#                    output_json = json.dumps(output_dict)                    
##                    print (type(data),data)
##                    When reading data in bytes, we need to define our own protocol for communication between server and client. The simplest protocol which we can define is called TLV (Type Length Value). It means that every message written to the socket is in the form of the Type Length Value.
##           
##So we define every message sent as:
##
##A 1 byte character that represents the data type, like s for String
##A 4 byte integer that indicates the length to the data
##And then the actual data, whose length was just indicated
#                    print (type(bytes(b'ABCD')),b'ABCD')
##                    message = 'sID:ABCD_EFG113\n speed:12\n angle:45.12\n'
#                    message1 = 'sID:ABCD_EFG113\n'
#                    connection.sendall(message1.encode("Utf-8"))
#                    
#
#                    t = time.localtime()
#                    current_time = time.strftime("%H:%M:%S", t)
#                    
#                    print (current_time)
#                    
#                    
#                    
#                    message2 = 'speed:12\n'
#                    
#                    connection.sendall(message2.encode("Utf-8"))                    
#
#                    message3 = 'angle:45.12\n'
#                    connection.sendall(message3.encode("Utf-8"))
#
#                    message4 = 'timeserver_'+current_time+'\n'
#                    connection.sendall(message4.encode("Utf-8"))   
#                    
#                    connection.close()
#                     
#                    
##                    connection.sendall(output_string)
#                    control = False
#                else:
##                    print (sys.stderr, 'no more data from mobile device', client_address)
#                    control = True
#                    
#                    break            
#        elif client_address[0]!=DEVICE_IP:
#            print (sys.stderr, 'connection from client', client_address)
#            
#        # Receive the data in small chunks and retransmit it
#            while True:
#                
#                data = connection.recv(1024)
##                print (sys.stderr, 'received ',data)
#                if data:
#                    print ("data received at server ",data)
#                    data_cl = json.dumps(example_operation(data))
#                    print (sys.stderr, 'sending data back to the client')
#                    connection.sendall(data_cl.encode("Utf-8"))
#                else:
##                    print (sys.stderr, 'no more data from', client_address)
#                    break
#            
#    finally:
#        print ("end")
#        # Clean up the connection
#        connection.close()


#"""the TCP address is passed as a tuple of (ip address, port number)
#Passing an empty string as the ip address means that the server will be listening 
#on any network interface (all available IP addresses"""
#
#def transmit_data(data):
#     """function to transmit data to the simulator  server"""
#
#def receive_data_confirmation():
#     """function to confirm that data was received at the simulator server"""
#     
#create_server()                           