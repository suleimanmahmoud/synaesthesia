from _socket import SHUT_RDWR
import os
import socket
import sys


class UDPServer():
    def __init__(self,server_ip,udp_port,buffer_size):
        #self.addrServer(host, port)
        self.UDPSock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.UDPSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.UDPSock.bind((server_ip, udp_port))
        self.BUFFER_SIZE=buffer_size
        print '[', os.uname()[1],'] Waiting for incoming messages...'
        
    def setAddrClient(self,address):
        self.addr = address
    
    def getAddrClient(self):
        return self.addr
            
    def sendUDPmsg(self,data,host,port):
        #set addr
        #self.addr = (host, port)
        #request script to be called from a certain raspberry pi host
        self.UDPSock.sendto(data, (host,port))
    
    def sendUDPmsgToLastClient(self,data):
        #set addr
        #self.addr = (host, port)
        #request script to be called from a certain raspberry pi host
        self.UDPSock.sendto(data, self.getAddrClient())
        print '[', os.uname()[1],'] Sent message: ', data,' to ',self.getAddrClient()
        return self.getAddrClient()
        
    def receiveUDPmsg(self,delay):
        init_delay=delay
        self.UDPSock.settimeout(delay)
        try:
            (data, addr) = self.UDPSock.recvfrom(self.BUFFER_SIZE) #maybe change to a local class parameter not a global
            self.setAddrClient(addr)
            print '[', os.uname()[1],'] Received message: ', data,' from ',addr
            return data
        except socket.timeout:
            delay *= 2 # wait even longer for the next request
            if delay > 10.0*init_delay:
                raise RuntimeError('Timeout! Got no response from Raspberry Pi. Is its UDP server down?')
                return "ERROR: Timeout! Got no response from Raspberry Pi. Is the server down?"
        except:
            raise # a real error so we let the user see it
            return "[EXCEPTION]: Exception not caught", sys.exc_info()[0]
                    
    def closeUDPserver(self):
        print "Exiting UDP Server socket..."   
        #self.UDPSock.shutdown(SHUT_RDWR) 
        self.UDPSock.close()
        
    
