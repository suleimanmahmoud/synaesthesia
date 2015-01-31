#!/usr/bin/env python
from __builtin__ import exit
import os,subprocess
import sys

from TCPClient import TCPClient
from TCPServer import TCPServer
from UDPServer import UDPServer

#****************************************************************
#                            MAIN
#****************************************************************
# Improvement: Implement https://docs.python.org/2/library/socketserver.html
if __name__ == "__main__":
    RPI_IP = '192.168.1.1'
    #RPI_IP = '127.0.0.1'
    TCP_PORT = 5005
    UDP_PORT = 13000
    BUFFER_SIZE = 512
    delay=100
    #IP DO IMAGE SOURCE VAI SER SETADO COM BASE NA CONEXAO RECEBIDA POR UDP! NO PARAMETRO imageSource_addr[0]
    while True:
        try:
            # ********************************************************
            #Start listening t    o UDP socket on UDP_PORT
            udpServer = UDPServer(RPI_IP,UDP_PORT,BUFFER_SIZE)
            # ********************************************************
            #Wait for UDP packet Image Information in the format "IMAGE_NAME,IMAGE_SIZE"
            msg_rx =  udpServer.receiveUDPmsg(delay)
            im_data=msg_rx.split(',')
            print '[MidiSource] Image Name: {0}, Image Size: {1}'.format(im_data[0], im_data[1])
            # ********************************************************
            #Start TCP server and start listening to TCP_PORT
            tcpServer = TCPServer(RPI_IP,TCP_PORT,BUFFER_SIZE,os.uname()[1])
            #server.setSName(socket.gethostname())
            tcpServer.bindSocket()
            #tcpServer.setFileName(im_data[0])
            #tcpServer.setFileSize(im_data[1])
            #tcpServer.start()
            #tcpServer.join()
            # ********************************************************
            #Acknowledge that it is ready to receive the image
            imageSource_addr = udpServer.sendUDPmsgToLastClient("OK")
            tcpServer.acceptSocket()
            # ********************************************************
            #Receive and save Image of name:IMAGE_NAME and size:IMAGE_SIZE
            #print 'Using transfer to receive: '+im_data[0]
            #tcpServer.transfer(im_data[0])
            print '[MidiSource] Using receiveDatabySize to receive: '+im_data[1]+' bytes of '+im_data[0]
            data_received = tcpServer.receiveDataBySize(int(im_data[1]))
            f = open(im_data[0],"w")
            f.write(data_received)
            f.close()
            print '[MidiSource] Created file '+im_data[0]+' with the data received by TCP.'
            # ********************************************************
            #Close TCP socket
            tcpServer.closeTCPServer()
            print '[MidiSource] TCPServer closed'
    #**************************MIDI PART******************************************            
            # ********************************************************        
            imname=im_data[0].split('.')
            midiname=imname[0]+'.midi'
            command = "/usr/bin/python2.7 ./RPIcreateMIDIFromImage.py"
            #command = "python RPIcreateMIDIFromImage.py"
            parameters = " --image "+ im_data[0] +" --midi "+midiname+" --resize 0 --tempo 200 --debug N --interpolation 1"
            print 'SHELL COMMAND: ', command+parameters
            #scriptReturn = subprocess.check_call(command + parameters,shell=False)
            os.system(command + parameters)
            #print 'Return of Shell command:',scriptReturn
                
            #Send MIDI Information via UDP packet in the format "MIDI_NAME,MIDI_SIZE"
            print '[MidiSource] Initializing send of "%s"' % midiname
            print "[MidiSource] Opening file - ",midiname
            midi = open(midiname,'r')
            # f is a file-like object. 
            old_file_position = midi.tell()
            midi.seek(0, os.SEEK_END)
            size = midi.tell()
            midi.seek(old_file_position, os.SEEK_SET)
            #size = os.path.getsize(midiname)
            print '[MidiSource] Sending name:"%s" and size:"%s",' % (midiname,str(size))
            udpServer.sendUDPmsgToLastClient(midiname+','+str(size)+',')
            # ********************************************************
            ret = udpServer.receiveUDPmsg(delay)
            print "[MidiSource] Mensagem recebida do ImageSource " , ret
            # ********************************************************
            #Connect to Android TCP server on Android_IP and TCP_PORT
            if(ret=="OK"):
                tcpClient = TCPClient(imageSource_addr[0],TCP_PORT,BUFFER_SIZE)
                tcpClient.connectTCP()
                print '[MidiSource] TCP Client ready to send the MIDI'
                #tcpClient.sendFileByNameAndClose(imgname)
                # ********************************************************
                #Send Image
                tcpClient.sendDataBySize(midi.read(), size)
                # ********************************************************
                #Close TCP socket
                tcpClient.closeTCPclient()
                print '[MidiSource] TCPClient closed'
            # ********************************************************
            #Send MIDI
            # ********************************************************
            #If transfer has finished, Close TCP socket
    
        except:
            print sys.exc_info()[0]
            #raise
        finally:
            print >>sys.stderr, '[MidiSource] Exiting Program'
            try:
                udpServer.closeUDPserver()
                tcpServer.closeTCPServer()
                tcpClient.closeTCPclient()
            except:
                print sys.exc_info()[0]
                #raise
    exit(0)
            
