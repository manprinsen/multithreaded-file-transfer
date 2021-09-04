#!/usr/bin/env python3
#sudo mv /media/temp0/*.plot /media/output/

import threading
import time
import glob
import os
import random
import shutil

srcDir = "/Users/lemling/Desktop/source/"
destDir0 = "/Users/lemling/Desktop/dest0/"
destDir1 = "/Users/lemling/Desktop/dest1/"
destDir2 = "/Users/lemling/Desktop/dest2/"
destDir0_lock = False
destDir1_lock = False
destDir2_lock = False

def mover(srcPath,dest,lockId):
    #os.system("cp "+sourceFile+" "+destination)
    #shutil.move(sourceFile,destination)
    time.sleep(random.randint(11,20))
    shutil.copy(srcPath,dest)
    print("done with "+srcPath)
    if lockId == 0:
        global destDir0_lock
        destDir0_lock = False
        print("destDir0_lock="+str(destDir0_lock))
    elif lockId == 1:
        global destDir1_lock
        destDir1_lock = False
        print("destDir1_lock="+str(destDir1_lock))
    elif lockId == 2:
        global destDir2_lock
        destDir2_lock = False
        print("destDir2_lock="+str(destDir2_lock))
    else:
        print("null")


print(glob.glob(srcDir))
files = glob.glob(srcDir+"*.plot")
#print(files)


threadPool = []

for index, filePath in enumerate(files):
    threadPool.append(index)
    thread = threadPool[index]

    if destDir0_lock == False:
        thread = threading.Thread(target=mover,args=(filePath,destDir0,0))
        destDir0_lock = True
        print("destDir0_lock="+str(destDir0_lock))
    elif destDir1_lock == False:
        thread = threading.Thread(target=mover,args=(filePath,destDir1,1))
        destDir1_lock = True
    elif destDir2_lock == False:
        print("destDir1_lock="+str(destDir1_lock))
        thread = threading.Thread(target=mover,args=(filePath,destDir2,2))
        destDir1_lock = True
        print("destDir2_lock="+str(destDir2_lock))
    else:
        print("all directories are busy")

    thread.start()

    print("thread "+str(index)+" started")

print("Active Threads: "+str(threading.active_count()))
#print(threading.enumerate())
print("MainThread: "+str(time.perf_counter()))