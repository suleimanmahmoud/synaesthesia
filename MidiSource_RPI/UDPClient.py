import socket
import os
import sys
from _socket import SHUT_RDWR

class UDPClient():
    
    def __init__(self,buffer_size):
        self.UDPSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.BUFFER_SIZE=buffer_size
    
    def sendUDPmsg(self,data,host,port):
        #set addr
        #self.addr = (host, port)
        #request script to be called from a certain raspberry pi host
        self.UDPSock.sendto(data, (host,port))
    
    def receiveUDPmsg(self,delay):
        init_delay=delay
        self.UDPSock.settimeout(delay)
        try:
            (data, addr) = self.UDPSock.recvfrom(self.BUFFER_SIZE) #maybe change to a local class parameter not a global
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
            
    def receiveDataValidFlag(self,delay):
        init_delay=delay
        self.UDPSock.settimeout(delay)
        try:
            (data,addr) = self.UDPSock.recvfrom(self.BUFFER_SIZE)
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
        
    def closeUDPclient(self):
        print "Exiting UDP client..."  
        self.UDPSock.shutdown(SHUT_RDWR)
        self.UDPSock.close()    