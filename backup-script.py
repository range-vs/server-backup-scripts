import subprocess
import sys
from unittest import result
import requests
import datetime
import os
 
import pass_server

from pathlib import Path


endpoint = "https://api.telegram.org/bot" + pass_server.telegram_bot_id + "/sendMessage?chat_id=" + pass_server.telegram_chat_id + "&text="
extImgDisk = ".img.gz"
outputPathOSImg = "/mnt/Backup/os/"
outputPathFilesImg = "/mnt/Backup/files/"
outputPathAndNameOSImg = outputPathOSImg + "os_image_disk_"
outputPathAndNameFilesImg = outputPathFilesImg + "files_image_disk_"
extImgDiskZstd = ".zst"


def main():
    e = datetime.datetime.now()
    currentDateTime = "%s_%s_%s_%s_%s_%s" % (e.day, e.month, e.year, e.hour, e.minute, e.second)
    
    createRequest("[" + "%s-%s-%s %s:%s:%s" % (e.day, e.month, e.year, e.hour, e.minute, e.second) + "] Start create backups")

    osImg = outputPathAndNameOSImg + currentDateTime + extImgDisk
    removeOldArchives(outputPathOSImg)
    createImgDisk("/dev/sdb", osImg)
    compressedImgDisk(osImg)

    filesImg = outputPathAndNameFilesImg + currentDateTime + extImgDisk
    removeOldArchives(outputPathFilesImg)
    createImgDisk("/dev/md0", filesImg)
    compressedImgDisk(filesImg)

    eEnd = datetime.datetime.now()
    createRequest("[" + "%s-%s-%s %s:%s:%s" % (eEnd.day, eEnd.month, eEnd.year, eEnd.hour, eEnd.minute, eEnd.second) + "] Finish create backups")

    e = eEnd - e
    createRequest("[" + str(e) + "] Time created backups")




def removeOldArchives(outputPath):
    files = sorted(Path(outputPath).iterdir(), key=os.path.getmtime)
    if(len(files) < 2):
        return
    for file in files:
        if(len(os.listdir(outputPath)) == 1):
            return
        f = os.path.join(outputPath, file)
        print(f)
        os.remove(f)
        createRequest("[Correct] Remove old img disk: " + f)

def createImgDisk(disk, outputPathAndName):
    cmd_pass = subprocess.Popen(["echo",pass_server.sudo_password], stdout=subprocess.PIPE)
    proc = subprocess.Popen(
        ["sudo", "dd", "if=" + disk, "of=" + outputPathAndName, "status=progress"],
        stdin=cmd_pass.stdout,
        stdout=sys.stdout,
        stderr=sys.stderr,
        universal_newlines=True,
        bufsize=1)
    proc.poll()
    proc.wait()
    result = proc.returncode
    print(result)
    now = datetime.datetime.now()
    if (result != 0):
        createRequest("[" + "%s-%s-%s %s:%s:%s" % (now.day, now.month, now.year, now.hour, now.minute, now.second) + "] Error create img disk: " + disk)
    else:
        createRequest("[" + "%s-%s-%s %s:%s:%s" % (now.day, now.month, now.year, now.hour, now.minute, now.second) + "] Create img disk successfull. Name file: " + outputPathAndName + " Filesize: " + str(int(os.path.getsize(outputPathAndName)/ 1024 / 1024 / 1024)) + " GB")

def compressedImgDisk(imgPathAndName):
    newFile = imgPathAndName + extImgDiskZstd
    cmd_pass = subprocess.Popen(["echo",pass_server.sudo_password], stdout=subprocess.PIPE)
    proc = subprocess.Popen(
        ["sudo", "zstd", "-7", "-c", "--rm", imgPathAndName, "-o", newFile],
        stdin=cmd_pass.stdout,
        stdout=sys.stdout,
        stderr=sys.stderr,
        universal_newlines=True,
        bufsize=1)
    proc.poll()
    proc.wait()
    result = proc.returncode
    print(result)
    now = datetime.datetime.now()
    if (result != 0):
        createRequest("[" + "%s-%s-%s %s:%s:%s" % (now.day, now.month, now.year, now.hour, now.minute, now.second) + "] Error create zstd archive: " + imgPathAndName)
    else:
        createRequest("[" + "%s-%s-%s %s:%s:%s" % (now.day, now.month, now.year, now.hour, now.minute, now.second) + "] Create zstd archive successfull. Name file: " + newFile + " Filesize: " + str(int(os.path.getsize(newFile)/ 1024 / 1024 / 1024)) + " GB")

def createRequest(msg):
    res = requests.get(endpoint + msg)
    if res:
        print("Response OK")
    else:
        print("Response Failed")

if __name__ == "__main__":
	main()

# TODO: remove old copy (>= 2)