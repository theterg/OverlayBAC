#!/usr/bin/python

import serial
import time
import OverlayBAC
import filequeueworker
import signal
import sys


ser = serial.Serial("/dev/ttyACM0",9600)
filedir = "/home/root/images/"

queue = filequeueworker.FilequeueWorker(filedir)
queue.start()

def signal_handler(signal, frame):
   print '[MAIN]  quitting'
   queue.stop()
   ser.close()
   sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGINT, queue.signal_handler)

currentReading = []
print "[MAIN]  Staring loop"
while(1):
   line = ser.readline()
   if ord(line[0]) != 0x2:
      print "[SERIAL]  "+line
   else:
      if line[1] == 'H':
         print "[MAIN]  New Score: "+str(int(line[2:]))
         queue.filequeue.append([filename,int(line[2:])])
         print "[MAIN]       filequeue status: "+str(queue.filequeue)
      elif line[1] == 'P':
         print "[MAIN]  Taking a photo"
         filename = time.strftime("%d%m%y_%H%M%S",time.localtime())+"_pic.jpg"
         OverlayBAC.takePicture(filedir+filename)
         print "[MAIN]  Clearing the readylight"
         ser.write("C\r\n")
      elif line[1] == 'V':  #A Value!
         continue #NOP

