#!/usr/bin/env python3

import threading
import time
import glob
import os
import random
import shutil

srcDir = "/media/raiddisk/" #"/Users/lemling/Desktop/source/"
destDir0 = "/media/disk0/"  #/Users/lemling/Desktop/dest0/"
destDir1 = "/media/disk1/"  #"/Users/lemling/Desktop/dest1/"
destDir2 = "/media/disk2/"  #"/Users/lemling/Desktop/dest2/"
destDir0_lock = False
destDir1_lock = False
destDir2_lock = False
file0_lock = ""
file1_lock = ""
file2_lock = ""

def mover(srcPath,dest):
    if os.path.isfile(srcPath) == False:
        return

    #time.sleep(random.randint(11,20))
    global destDir0_lock
    global file0_lock
    global destDir1_lock
    global file1_lock
    global destDir2_lock
    global file2_lock

    if destDir0_lock and file0_lock == srcPath:
        #os.system("mv "+srcPath+" "+dest) 
        shutil.move(srcPath,dest)
        destDir0_lock = False
        file0_lock = ""
        print("done with "+srcPath)
    elif destDir1_lock and file1_lock == srcPath:
        #os.system("mv "+srcPath+" "+dest) 
        shutil.move(srcPath,dest)
        destDir1_lock = False
        file1_lock = ""
        print("done with "+srcPath)
    if destDir2_lock and file2_lock == srcPath:
        #os.system("mv "+srcPath+" "+dest) 
        shutil.move(srcPath,dest)
        destDir2_lock = False
        file2_lock = ""
        print("done with "+srcPath)

#print(glob.glob(srcDir))
print("MainThread: "+str(time.perf_counter()))
threadPool = []
old0 = -1
old1 = -1

while True:
    time.sleep(10)
    threadPool = []
    files = glob.glob(srcDir+"*.plot")
    nrOfFiles = len(files)
    print("Active Threads: "+str(threading.active_count()))

    if nrOfFiles == 0 and old0 != nrOfFiles:
        print("No Files In Source Directory")
        old0 = nrOfFiles
        continue

    if destDir0_lock and destDir1_lock and destDir2_lock:
        print("all directories are busy")
        continue

    for index, filePath in enumerate(files):
        if destDir0_lock == False and file0_lock == "":
            destDir0_lock = True
            file0_lock = filePath
            t0 = threading.Thread(target=mover,args=(filePath,destDir0))
            t0.start()
            threadPool.append(t0)
            print("thread started moving "+filePath) 
        elif destDir1_lock == False and file1_lock == "":
            destDir1_lock = True
            file1_lock = filePath
            t1 = threading.Thread(target=mover,args=(filePath,destDir1))
            t1.start()
            threadPool.append(t1)
            print("thread started moving "+filePath)
        elif destDir2_lock == False and file2_lock == "":
            destDir2_lock = True
            file2_lock = filePath
            t2 = threading.Thread(target=mover,args=(filePath,destDir2))
            t2.start()
            threadPool.append(t2)
            print("thread started moving "+filePath)
        #else:
            #print("all directories are STILL busy")

    print("Active Threads: "+str(threading.active_count()))

    for thread in threadPool:
        thread.join()