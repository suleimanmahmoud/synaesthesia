from _socket import SHUT_RDWR
import socket
#from threading import Thread


#class TCPServer(Thread):
class TCPServer():
    def __init__( self,server_ip,server_port,buffer_size,socketName ):
        # Thread.__init__( self )
        self.kill_received = False
        #by default will be always listening to Raspberry Pi connections
        self.keepAlive = True 
        self.SERVER_IP=server_ip
        self.SERVER_PORT=server_port
        self.BUFFER_SIZE=buffer_size
        self.sName=socketName
    
    def setSName(self,socketName):
        self.sName = socketName
        
    def getSName(self):
        return self.sName
    
    def setKillFlag(self,killFlag):
        self.kill_received = killFlag
        
    def getKillFlag(self):
        return self.kill_received 
    
    def setKeepAlive(self,aliveFlag):
        self.keepAlive = aliveFlag
        
    def getKeepAlive(self):
        return self.keepAlive 
    
    def setFileName(self,fileName):
        self.filename=fileName
    
    def getFileName(self):
        return self.filename
    
    def run(self):
        while not self.kill_received:
            self.process()          
        
    def bindSocket( self ):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        #For scalability take into account the TIME_WAIT
        #http://www.serverframework.com/asynchronousevents/2011/01/time-wait-and-its-design-implications-for-protocols-and-scalable-servers.html
        self.sock.bind((self.SERVER_IP, self.SERVER_PORT))
        self.sock.listen(1)
        print '[',self.getSName(),'] Listening on port ',self.SERVER_PORT
    
    def acceptSocket( self ):
        self.conn, self.addr = self.sock.accept()
        print '[',self.getSName(),'] Got connection from ', self.addr
    
    def transfer( self, saveFileAs ):        
        print '[',self.getSName(),'] Starting file transfer for "%s"' %saveFileAs
        i =0
        f = open(saveFileAs,"w")
        while 1:
            data = self.conn.recv(self.BUFFER_SIZE)
            if data == "exit":
                print "Received Exit call"
                self.close()
                break
            i+=1
            print i
            if not data: 
                print 'Em teoria terminou de receber o arquivo'
                break
            f.write(data)
        f.close()

        print '[',self.getSName(),'] Got "%s"' %saveFileAs
        print '[',self.getSName(),'] Closing file transfer for "%s"' %saveFileAs
        #If we want it to be executed just one, then we tell the thread to die
        if not self.keepAlive :
            self.kill_received = True
            print "Not keeping TCP Server alive anymore."
    
    def receiveDataBySize(self,size):
        chunks = []
        bytes_recd = 0
        while bytes_recd < size:
            chunk = self.conn.recv(min(size - bytes_recd, self.BUFFER_SIZE))
            if chunk == '':
                raise RuntimeError("Socket Connection broken")
            chunks.append(chunk)
            bytes_recd = bytes_recd + len(chunk)
        
        print '[',self.getSName(),'] Received ',bytes_recd,' bytes'
        print '[',self.getSName(),'] Returning data...'
        return ''.join(chunks)
    
    def closeTCPServer( self ):
        self.conn.close()
        #self.sock.shutdown(SHUT_RDWR)
        self.sock.close() 
        print "Exiting TCP Server..."
        return  
              
    def process( self ):
            print "Running TCP Server Thread..."
            self.bindSocket()
            self.acceptSocket()
            self.transfer(self.getFileName())
            self.__closeTCPServer()           
