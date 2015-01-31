import socket
from _socket import SHUT_RDWR
import sys

class TCPClient():
    def __init__(self,server_ip,server_tcp_port,buffer_size):
        self.host = server_ip
        self.port = server_tcp_port
        self.BUFFER_SIZE=buffer_size
        
    def connectTCP(self):
        self.socketTCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.socketTCP.connect((self.host, self.port))
            #self.socketTCP.connect((TCP_IP, TCP_PORT))
            return 1
        except socket.error as err:
            print err
            self.socketTCP.close()
            self.socketTCP = None
            return -1
        except:
            print "[EXCEPTION] Unexpected error:", sys.exc_info()[0]
            self.__closeTCPclient()
            raise
    
    def sendFileByNameAndClose(self,fileName):
        #self.socketTCP.send(MESSAGE)
        #data = self.socketTCP.recv(BUFFER_SIZE)
        MESSAGE = "Sending ", fileName," to ",self.host," on port ",self.port
        print MESSAGE

        try:
            f = open(fileName, "r") #rb on Windows for binary
        except IOError as e:
            print "EXCEPTION] I/O error({0}): {1}".format(e.errno, e.strerror)
            self.__closeTCPclient()
        except:
            print "[EXCEPTION] Unexpected error:", sys.exc_info()[0]
            self.__closeTCPclient()
            raise
        else:
            data = f.read()
            f.close()
            self.socketTCP.sendall(data)
            print "[OK] Sent data to ",self.host," on port ",self.port
            self.__closeTCPclient()
            
    def sendDataBySize(self,data,size):
        totalsent = 0
        MESSAGE = "Sending Data with filesize ", size, " to ",self.host," on port ",self.port
        print MESSAGE
        while totalsent < size:
            sent = self.socketTCP.send(data[totalsent:])
            if sent == 0:
                raise RuntimeError("Socket Connection broken")
            totalsent = totalsent + sent
        print "[OK] Sent data to ",self.host," on port ",self.port
        
    def receiveDataBySize(self,size):
        chunks = []
        bytes_recd = 0
        while bytes_recd < size:
            chunk = self.socketTCP.recv(min(size - bytes_recd, self.BUFFER_SIZE))
            if chunk == '':
                raise RuntimeError("Socket Connection broken")
            chunks.append(chunk)
            bytes_recd = bytes_recd + len(chunk)
        return ''.join(chunks)

    def shutdownTCPServerAndClose(self):
        self.socketTCP.send("exit")
        self.__closeTCPclient()
    
    def closeTCPclient(self):
        print "Exiting TCP client socket..."
        #self.socketTCP.shutdown(SHUT_RDWR)
        self.socketTCP.close()