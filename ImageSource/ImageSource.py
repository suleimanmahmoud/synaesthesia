from __builtin__ import exit
import os
import sys
from TCPClient import TCPClient
from TCPServer import TCPServer
from UDPClient import UDPClient

#****************************************************************
#                            MAIN
#****************************************************************
# Improvement: Implement https://docs.python.org/2/library/socketserver.html

if __name__ == "__main__":
    RPI_IP = '192.168.1.1'
    #RPI_IP = '127.0.0.1'
    MY_IP = '192.168.1.3'
    #MY_IP = '127.0.0.1'
    TCP_PORT = 5005
    UDP_PORT = 13000
    BUFFER_SIZE = 512
    delay=100
    #     UPDATE UDP DELAY ACCORDING TO THE DURATION CHOSEN FOR THE USRP OPERATION
    try:
        imgname='7Anoes.jpg'
        #print >>sys.stderr, 'Initializing send of "%s"' % imgname
        print '[ImageSource] Initializing send of "%s"' % imgname
        print "[ImageSource] Opening file - ",imgname
        img = open(imgname,'r')
        # f is a file-like object. 
        old_file_position = img.tell()
        img.seek(0, os.SEEK_END)
        size = img.tell()
        img.seek(old_file_position, os.SEEK_SET)
        #size = os.path.getsize(imgname)
        print '[ImageSource] Sending name:"%s" and size:"%s"' % (imgname,str(size))

        # ********************************************************
        #Initialize UDP socket
        udpClient = UDPClient(BUFFER_SIZE)
        # ********************************************************
        #Send Image Information via UDP packet in the format "IMAGE_NAME,IMAGE_SIZE"   
        udpClient.sendUDPmsg(imgname+','+str(size), RPI_IP, UDP_PORT)
        #Assert that message with Image Name and Image Size was received
        ret = udpClient.receiveUDPmsg(delay)
        print "[ImageSource] Mensagem recebida do MidiSource" , ret
        # ********************************************************
        #Connect to RPI TCP server
        if(ret=="OK"):
            tcpClient = TCPClient(RPI_IP,TCP_PORT,BUFFER_SIZE)
            tcpClient.connectTCP()
            print '[ImageSource] TCP Client ready to send the image'
            #tcpClient.sendFileByNameAndClose(imgname)
            # ********************************************************
            #Send Image
            tcpClient.sendDataBySize(img.read(), size)
            # ********************************************************
            #Close TCP socket
            tcpClient.closeTCPclient()
            print '[ImageSource] TCPClient closed'
            
#**************************MIDI PART******************************************            
            # ********************************************************
            #Wait for UDP Packet Flag saying MIDI is ready to be sent
            ret = udpClient.receiveUDPmsg(delay)
            # ********************************************************
            #Start TCP Server
            midi_data=ret.split(',')
            print '[ImageSource] Image Name: {0}, Image Size: {1}'.format(midi_data[0], midi_data[1])
            # ********************************************************
            #Accept RPI TCP connection
            tcpServer = TCPServer(MY_IP,TCP_PORT,BUFFER_SIZE,os.uname()[1])
            tcpServer.bindSocket()
            udpClient.sendUDPmsg("OK", RPI_IP, UDP_PORT)
            tcpServer.acceptSocket()
            # ********************************************************
            #Receive MIDI
            print '[ImageSource] Using receiveDatabySize to receive: '+midi_data[1]+' bytes of '+midi_data[0]
            data_received = tcpServer.receiveDataBySize(int(midi_data[1]))
            f = open(midi_data[0],"w")
            f.write(data_received)
            f.close()
            print '[ImageSource] Created file '+midi_data[0]+' with the data received by TCP.'
            # ********************************************************
            #Close TCP socket
            tcpServer.closeTCPServer()
            print '[ImageSource] TCPServer closed'
            
            # ********************************************************
            #If transfer has finished, Close TCP socket
        else:
            print >>sys.stderr,'[ImageSource] Server did not receive image data. It returned: ',ret
        
    except:
        print sys.exc_info()[0]
    finally:
        print >>sys.stderr, '[ImageSource] Exiting Program'
        try:
            udpClient.closeUDPclient()    
            tcpClient.closeTCPclient()
            tcpServer.closeTCPServer()
        except:
            print sys.exc_info()[0]
            exit()
        
