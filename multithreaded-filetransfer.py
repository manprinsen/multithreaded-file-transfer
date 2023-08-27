import threading
import time
import glob
import os
import random
import shutil
from subprocess import call
from datetime import datetime

srcDir = "Z:\\"     #"/media/raiddisk/" #"/Users/lemling/Desktop/source/"
destDir0 = "D:\\"   #/media/disk0/"  #/Users/lemling/Desktop/dest0/"
destDir1 = "E:\\"   #"/media/disk1/"  #"/Users/lemling/Desktop/dest1/"
destDir2 = "F:\\"   #/media/disk2/"  #"/Users/lemling/Desktop/dest2/"
#os.system("sudo chmod 777 "+destDir0)
#os.system("sudo chmod 777 "+destDir1)
#os.system("sudo chmod 777 "+destDir2)

destDir0_lock = False
destDir1_lock = False
destDir2_lock = False
file0_lock = ""
file1_lock = ""
file2_lock = ""

def checkDiskUsage(driveLetter):
    total, used, free = shutil.disk_usage(driveLetter)#("D:\\")
    #print("Total: %d GiB" % (total // (2**30)))
    #print("Used: %d GiB" % (used // (2**30)))
    #print("Free: %d GiB" % (free // (2**30)))
    spaceFree = free // (2**30)
    return int(spaceFree)
    
def usedDiskSpace(driveLetter):
    total, used, free = shutil.disk_usage(driveLetter)
    usedSpace = used // (2**30)
    return int(usedSpace)

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
    
    idx = srcPath.rindex("\\") + 1
    dir = srcPath[:idx]
    file = srcPath[idx:]

    if destDir0_lock and file0_lock == srcPath:
        #os.system("mv "+srcPath+" "+dest) 
        #shutil.move(srcPath,dest)
        call(["robocopy",dir,dest,file,"/MOV","/LOG:log0"])
        destDir0_lock = False
        file0_lock = ""
        print("done with "+srcPath)
    elif destDir1_lock and file1_lock == srcPath:
        #os.system("mv "+srcPath+" "+dest) 
        #shutil.move(srcPath,dest)
        call(["robocopy",dir,dest,file,"/MOV","/LOG:log1"])
        destDir1_lock = False
        file1_lock = ""
        print("done with "+srcPath)
    elif destDir2_lock and file2_lock == srcPath:
        #os.system("mv "+srcPath+" "+dest) 
        #shutil.move(srcPath,dest)
        call(["robocopy",dir,dest,file,"/MOV","/LOG:log2"])
        destDir2_lock = False
        file2_lock = ""
        print("done with "+srcPath)
    
    print("end: "+str(datetime.now()))


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
    
    print(srcDir+": "+str(checkDiskUsage(srcDir))+" space free")
    usedSpace = usedDiskSpace(srcDir)
    if usedSpace < 300:
        continue

    if nrOfFiles == 0 and old0 != nrOfFiles:
        print("No Files In Source Directory")
        old0 = nrOfFiles
        continue

    if destDir0_lock and destDir1_lock and destDir2_lock:
        print("all directories are busy")
        continue

    print("start: "+str(datetime.now()))
    print(destDir0+": "+str(checkDiskUsage(destDir0))+" space free")
    print(destDir1+": "+str(checkDiskUsage(destDir1))+" space free")
    print(destDir2+": "+str(checkDiskUsage(destDir2))+" space free")
    for index, filePath in enumerate(files):        
        if destDir0_lock == False and file0_lock == "" and checkDiskUsage(destDir0) >= 110:
            destDir0_lock = True
            file0_lock = filePath
            #mover(filePath,destDir0)
            t0 = threading.Thread(target=mover,args=(filePath,destDir0))
            t0.start()
            threadPool.append(t0)
            print("thread started moving "+filePath) 
        elif destDir1_lock == False and file1_lock == "" and checkDiskUsage(destDir1) >= 110:
            destDir1_lock = True
            file1_lock = filePath
            #mover(filePath,destDir1)
            t1 = threading.Thread(target=mover,args=(filePath,destDir1))
            t1.start()
            threadPool.append(t1)
            print("thread started moving "+filePath)
        elif destDir2_lock == False and file2_lock == "" and checkDiskUsage(destDir2) >= 110:
            destDir2_lock = True
            file2_lock = filePath
            #mover(filePath,destDir2)
            t2 = threading.Thread(target=mover,args=(filePath,destDir2))
            t2.start()
            threadPool.append(t2)
            print("thread started moving "+filePath)
        #else:
            #print("all directories are STILL busy")

    print("Active Threads: "+str(threading.active_count()))

    for thread in threadPool:
        thread.join()
