import threading
import time
import OverlayBAC
from commands import getoutput

pollDelay = 2

class FilequeueWorker( threading.Thread ):
   def __init__(self, filedir):
      threading.Thread.__init__(self)
      self.filequeue = []
      self.filedir = filedir
      self.running = True

   def run(self):
      print "[QUEUE]  Startup"
      while(self.running):
         if len(self.filequeue) == 0:
            time.sleep(pollDelay)
         else:
            self.doStuff()
      print "[QUEUE]  thread closing"

   def stop(self):
      print "[QUEUE]  attempting to kill thread"
      self.running = False
      self.join()

   def signal_handler(self, signal, frame):
      self.stop()

   def doStuff(self):
      print "[QUEUE]  Processing "+self.filedir+self.filequeue[0][0]
      OverlayBAC.overlayBAC(self.filedir+self.filequeue[0][0],self.filequeue[0][1])
      ret = getoutput('scp -i ~/.ssh/id_rsa '+self.filedir+self.filequeue[0][0]+' root@tergia-serv:/data/scratch/bugimages/')
      print "[QUEUE] "+ret
      print "[QUEUE]  Done processing "+self.filedir+self.filequeue[0][0]
      self.filequeue.pop(0)
