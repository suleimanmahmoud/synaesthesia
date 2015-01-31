#import the necessary packages
import numpy as np
import argparse
import cv2
import array
#import scipy
#import scipy.misc
#import matplotlib.pyplot as plt
#import matplotlib.colors as colors
from midiutil.MidiFile import MIDIFile
#from scipy import ndimage
#from scipy import misc
from cmath import sqrt

#python RPIcreateMIDIFromImage.py --image 7Anoes.jpg --resize 200 --tempo 600 --debug N --interpolation 1
#python RPIcreateMIDIFromImage.py --image 7Anoes.jpg --resize 0 --tempo 200 --debug N --interpolation 1
#aplaymidi -p 128 output.mid 

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", help = "path to the image")
ap.add_argument("-m", "--midi", help = "name of the midi to be saved")
ap.add_argument("-r","--resize", help = "define the resize ratio you want to use on the image (1 is the same as no resize)")
ap.add_argument("-c","--color", help = "define RED if you want to extract pure red")
ap.add_argument("-t","--tempo", help = "define the tempo value of the MIDI file")
ap.add_argument("-d","--debug", help = "define Y/N if you want to have the ranges printed as images")
ap.add_argument("-p","--interpolation", help = "0=NEAREST 1=BILINEAR 2=CUBIC 3=AREA 4=LANCZOS4")
args = vars(ap.parse_args())

# load the image
im = cv2.imread(args["image"])
imHSVoriginal = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)

height, width, depth = im.shape
print height, width, depth 

#120 pixels com tempo 200 = 36s de MIDI 
if(int(args["interpolation"])>0):
    interpolacao=int(args["interpolation"])
else:
    interpolacao=1  
print "SETANDO INTERPOLATION PARA interpolation=" + str(interpolacao)

if(int(args["resize"])>0):
    im_ratio=float(1/float(args["resize"]))
    print " RESIZE RATIO = "+str(im_ratio)
    if height==1:
        im = cv2.resize(im, (0,0), fx=im_ratio, fy=1.0,interpolation=interpolacao)
        print 'Not resizing height='+ str(height)
    elif width==1:
        im = cv2.resize(im, (0,0), fx=1.0, fy=im_ratio,interpolation=interpolacao)
        print 'Not resizing width='+ str(width)
    else:
        im = cv2.resize(im, (0,0), fx=im_ratio, fy=im_ratio,interpolation=interpolacao)
else:
    im_ratio=sqrt(120.0/(height*width)).real
    print "RATIO = "+str(im_ratio)
    im = cv2.resize(im,dsize=(int(round(width*im_ratio)),int(round(height*im_ratio))), fx=0.0,fy=0.0,interpolation=interpolacao)

height, width, depth = im.shape
print height, width, depth
#nesse ponto a imagem provavelmente foi resized, senao vou comparar ela com ela mesmo 
imHSV = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)

#valores da correlation dos histogramas de HxS HxV e SxV para serem plotados
correlation_h_s = 0
correlation_h_v = 0
correlation_s_v = 0

range_hist = [0, 180, 0, 256]
h_bins = 12; 
s_v_bins = 7;
histSize = [ h_bins, s_v_bins];

#Hue x Saturation
histO = cv2.calcHist( [imHSVoriginal], [0, 1], None, histSize, range_hist)
histR = cv2.calcHist( [imHSV], [0, 1], None, histSize, range_hist)
base_base = cv2.compareHist(histO,histO,0)
base_resized = cv2.compareHist(histO,histR,0)
correlation_h_s = base_resized
print "Hue x Saturation HISTOGRAM CORRELATION\nMethod: {0} -- base-base: {1} , base-resized: {2}".format(0,base_base,base_resized)
# Hue x Value
#hist0 is the same
histO = cv2.calcHist( [imHSVoriginal], [0, 2], None, histSize, range_hist)
histR = cv2.calcHist( [imHSV], [0, 2], None, histSize, range_hist)
base_base = cv2.compareHist(histO,histO,0)
base_resized = cv2.compareHist(histO,histR,0)
correlation_h_v = base_resized
print "Hue x Value HISTOGRAM CORRELATION\nMethod: {0} -- base-base: {1} , base-resized: {2}".format(0,base_base,base_resized)
#Saturation x Value
histO = cv2.calcHist( [imHSVoriginal], [1, 2], None, [ s_v_bins, s_v_bins],[0, 256, 0, 256])
histR = cv2.calcHist( [imHSV], [1, 2], None, [ s_v_bins, s_v_bins], [0, 256, 0, 256])
base_base = cv2.compareHist(histO,histO,0)
base_resized = cv2.compareHist(histO,histR,0)
correlation_s_v = base_resized
print " Saturation x Value HISTOGRAM CORRELATION\nMethod: {0} -- base-base: {1} , base-resized: {2}".format(0,base_base,base_resized)

# define the list of boundaries
# BGR ao inves de RGB, pq OpenCV NumPy representa array ao contrario
if(args["color"]=='RED'):
    saturated_hues = [
        ([0,255,255]     ,[4, 255,255]),    # A
   #     ([156,255,255]   ,[165,255,255]),   # G#    
        ([166,255,255]   ,[179, 255,255])  # zA
    ]    
    note_name = ['A','zA']
else:
    saturated_hues = [
        ([0,255,255]     ,[4, 255,255]),    # A
        ([156,255,255]   ,[165,255,255]),   # G#       
        ([5,255,255]     ,[15,255,255]),    # A#
        ([16,255,255]    ,[32,255,255]),    # B
        ([33,255,255]    ,[52,255,255]),    # C
        ([53,255,255]    ,[61,255,255]),    # C#
        ([62,255,255]    ,[80,255,255]),    # D
        ([81,255,255]    ,[90,255,255]),    # D#
        ([91,255,255]    ,[108,255,255]),   # E
        ([109,255,255]   ,[128,255,255]),   # F
        ([129,255,255]   ,[137,255,255]),   # F#    
        ([138,255,255]   ,[155,255,255]),   # G
        ([166,255,255]   ,[179, 255,255])  # zA
    ]
    note_name = ['A','G#','A#','B','C','C#','D','D#','E','F','F#','G','zA']

def getMIDInoteNumber(nota,escala):
    if escala == 'W':       #para os intervalos de C8 = WHITE
        return 108
    elif escala == 'N': #para os intervalos de A0 = N-NOIR
        return 21
    elif escala == 'R': #para os intervalos de A#0 = R-GRIS
        return 22
    elif escala == 'T':   #para os intervalos de B0 = T-TROP GRIS
        return 23
    else:
        esc=int(escala)-1
        if nota == 'C':
            return 24+12*esc
        elif nota == 'C#':
            return 25+12*esc
        elif nota == 'D':
            return 26+12*esc
        elif nota == 'D#':
            return 27+12*esc
        elif nota == 'E':
            return 28+12*esc
        elif nota == 'F':
            return 29+12*esc
        elif nota == 'F#':
            return 30+12*esc
        elif nota == 'G':
            return 31+12*esc
        elif nota == 'G#':
            return 32+12*esc
        elif (nota == 'A' or nota == 'zA'): #zA is the o segundo intervalo do Vermelho
            return 33+12*esc
        elif nota == 'A#':
            return 34+12*esc
        elif nota == 'B':
            return 35+12*esc

def defineEscalas(hue_lower,hue_upper):
    escalas_hues=[
        #preto, para todos os HUES e SATURATIONS
        ([hue_lower,0,0]    ,[hue_upper,255,32]),#A0
        #brancos e cinzas, para todos os HUES  
        #([hue_lower,0,0]    ,[hue_upper,23, 87]), #"A0"
        ([hue_lower,0,33]   ,[hue_upper,32, 128]), #"A#0"
        ([hue_lower,0,129]  ,[hue_upper,32, 191]), #"B0"
        ([hue_lower,0,192]  ,[hue_upper,32, 255]), #"C8"
        #escalas (se value maior ou igual a 88 e escala maior que 23)
        ([hue_lower,33,33]  ,[hue_upper,72, 255]), #7
        ([hue_lower,33,33]  ,[hue_upper,255, 72]), #7
        ([hue_lower,73,73]  ,[hue_upper,102,255]), #6
        ([hue_lower,73,73]  ,[hue_upper,255,102]), #6
        ([hue_lower,103,103]  ,[hue_upper,133,255]), #5
        ([hue_lower,103,103]  ,[hue_upper,255,133]), #5
        ([hue_lower,134,134] ,[hue_upper,163,255]), #4
        ([hue_lower,134,134] ,[hue_upper,255,163]), #4
        ([hue_lower,164,164] ,[hue_upper,193,255]), #3
        ([hue_lower,164,164] ,[hue_upper,255,193]), #3
        ([hue_lower,194,194] ,[hue_upper,223,255]), #2
        ([hue_lower,194,194] ,[hue_upper,255,223]), #2        
        ([hue_lower,224,224] ,[hue_upper,255,255]) #1
    ]   
    return escalas_hues

escalas = ['N','R','T','W','7','7_','6','6_','5','5_','4','4_','3','3_','2','2_','1']

#EFFICIENT ARRAYS
#    https://docs.python.org/2/library/array.html
#Initialize a 2D array that will hold notes values for each pixel(x,y) instead of BGR
seq2D = []
for i in range (0, height):
    new = []
    for j in range (0, width):
        new.append(21)
    seq2D.append(new)

#Notes sequence in 1D
seq=array.array('i',(21,)*(height* width))#preto e A0 = nota numero 21 na tabela de MIDI
count_hue=0
# loop over the boundaries
for (lower_sat, upper_sat) in saturated_hues:
    # find the colors within the specified boundaries and apply
    # the mask
    count_octave=0
    for (lower, upper) in defineEscalas(lower_sat[0],upper_sat[0]):
        lower = np.array(lower, dtype = "uint8")
        upper = np.array(upper, dtype = "uint8")    
        #output tem shape (height,width, depth) e mask (height, width)
        mask = cv2.inRange(imHSV, lower, upper) 
        mask_notes = mask[:] #AQUI aidna faco a copia para poder criar e validar as imagem individuais
        #print " GET NOTA "+note_name[count_hue] + " e ESCALA "+escalas[count_octave][:1]+" = " + str(getMIDInoteNumber(note_name[count_hue], escalas[count_octave][:1])) #[:1] pra cortar a diferenciacao das imgs
        mask_notes[mask_notes!=0]= getMIDInoteNumber(note_name[count_hue], escalas[count_octave][:1]) #[:1] pra cortar a diferenciacao das imgs
        for i in range(height):
            for j in range(width):
                if ((seq2D[i][j] == 21) & (mask_notes[i][j] != 0)):
                    seq2D[i][j] = mask_notes[i][j]
                
        #save the images
        if(args["debug"]=='Y'):
            output = cv2.bitwise_and(im, im, mask = mask)
            cv2.imwrite('Imagem_'+note_name[count_hue]+'_'+escalas[count_octave]+'.jpg',output)#([im, output]))
        
        # show the images
        #cv2.imshow("images", np.hstack([image, output]))
        #cv2.waitKey(0)
        count_octave+=1
    if(args["debug"]=='Y'):
        if count_hue == 999:
            print 'lower: '+ str(lower) +' upper: '+ str(upper)
            #print mask  #o pixel que estiver dentro do range vai ter na mascara um valor = dentro do range
            print 'MASK SHAPE: '+ str(mask.shape)
            print mask
            print 'output SHAPE: '+ str(output.shape)
            print output
            print 'MASK_NOTES SHAPE: '+ str(mask_notes.shape)
            print mask_notes
            print 'SEQ2D SHAPE: '+ str(len(seq2D)) + ','+str(len(seq2D[0]))
            print seq2D
            
    count_hue+=1
    
#Lineariza o seq2D para ser lido pelo gravador de MIDI
for i in range(height):
        for j in range(width):
            seq[j+i*width]=seq2D[i][j]
#AO INVES DISSO POSSO USAR O SCIPY.FLATTEN:
#http://docs.scipy.org/doc/numpy/reference/generated/numpy.ndarray.flatten.html
#seq2D.flatten('C') #=por linha = ([[1,2], [3,4]]) = ([1, 2, 3, 4]) 
#seq2D.flatten('F') #=por coluna = ([[1,2], [3,4]]) = ([1, 3, 2, 4])
            
# Create the MIDIFile Object with 1 track
MyMIDI = MIDIFile(1)

# Tracks are numbered from zero. Times are measured in beats.
track = 0   
time = 0
# Add track name and tempo.
MyMIDI.addTrackName(track,time,"Sample Track")
if(int(args["tempo"]) > 60):
    MyMIDI.addTempo(track,time,int(args["tempo"]))
else:
    MyMIDI.addTempo(track,time,120)
# Add a note. addNote expects the following information:
track = 0
channel = 0
#pitch = 60
time = 0
repeticoes = 0
volume = 100
print seq

#vai dizer por quantos segundos as notas que se repetem vao ficar "pressionadas"
#height*width is o tamanho maximo, mas se houve repeticoes, ele vai ser menor do que isso for sure
#duration_timing=array.array('i',(0,)*(height*width))
duration_timing=[]
#seq = (79,79,79,74,59,57,43)
temp = seq[1]
#primeira execucao vai contar as repeticoes de notas

duration_timing.insert(len(duration_timing),0)#para iniciar do tempo 0    
for note in seq:
    if temp != note:
        #print " TEMP = " +str(temp) +" NOTE = "+ str(note)+ " REPETICOES ="+str(repeticoes)
        temp = note
        duration_timing.insert(len(duration_timing),repeticoes)#a primeira nota, 79, repetiu tres vezes
        #print duration_timing
        repeticoes=1
    else:
        repeticoes+=1
if(args["debug"]=='Y'):
    print "REPETICOES PAROU EM "+str(repeticoes)
#verifica para a ultima transicao
if (seq[len(seq)-repeticoes] == seq[len(seq)-1]):        
    if(args["debug"]=='Y'):
        print " Seq [n-rep] = "+str(seq[len(seq)-repeticoes]) + " seq[n-1] = "+str(seq[len(seq)-1])
    duration_timing.insert(len(duration_timing),repeticoes)
duration_timing.insert(len(duration_timing),0)#para finalizar em 0    
#print duration_timing
#duration_timing.reverse()
#print duration_timing

if seq[1] != seq[0]:
    MyMIDI.addNote(track,channel,seq[0],0,1,volume)
    
iteracao=1
#adiciona arquivo midi contando as repeticoes das notas
#primeira nota = toca do tempo 0 ate a duracao[0]
#segunda nota  = toca do tempo (duracao[0]) ate duracao [1]
#e assim por diante...
#ultima nota = toca do tempo (duracao[n-1]) ate duracao[n]
print " Length duration_timing = "+str(len(duration_timing))
for note in seq:
    if temp != note:
        # Now add the note.
        temp = note
        time+=duration_timing[iteracao-1]#comeca da duration_timing[0]
        if(args["debug"]=='Y'):
            print "ITERACAO:"+str(iteracao) 
        if iteracao<len(duration_timing):
            if(args["debug"]=='Y'):
                print "NOTA " + str(note) + " do tempo "+ str(time) + "s por " + str(duration_timing[iteracao]) + "s"
            MyMIDI.addNote(track,channel,note,time,duration_timing[iteracao],volume)
            iteracao+=1

print " ESCREVENDO "+ str(iteracao-1)  +" notas"
print " Audio Duration: "+ str(time+duration_timing[iteracao-1])  +"s"
# And write it to disk.
#midiname= args["image"].split('.')
#print midiname
print args["midi"]
binfile = open(args["midi"], 'wb')
MyMIDI.writeFile(binfile)
binfile.close()

