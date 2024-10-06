# Clean exif data from a JPEG file 
from PIL import Image
from pathlib import Path
import os
import sys

runPath = Path.cwd()
file = Path.cwd()
dirname = 'ExifCleanImages'


def listFilesInDir(directory):
    return [f for f in Path(directory).iterdir() if f.is_file()]

def PrintExifToConsole(image):
    try:
        for exif in image.getexif():
            print(exif)
    except:
        print("exception when printing exif to console")

def CreateNewExifCleanFolder(directory):
    global dirname 
    dirname = 'ExifCleanImages'
    # in directory add a new directory called ExifCleanImages
    # put exif clean version of each image in local dir in there
    # check if dir exists first though
    dirExists = True
    dirExists = os.path.exists(directory / dirname)  

    if(dirExists == False): 
        os.mkdir(directory / dirname)
        if(os.path.exists(directory / dirname)): 
            print('Create '+dirname+' success: true')
        else:
            print('Failed to create the ' + dirname + 'direcory')

def CleanExifAllLocalImages(localPath):
    localFiles = listFilesInDir(localPath)

    for file in localFiles:
        try:
            image = Image.open(file)
            if(image != 'undefined' and image.format != 'png'): # Pillow will not remove exif from PNG by default
                filename = image.filename.split('/')[-1]
                print(filename)
                print("Exif Before: ")
                PrintExifToConsole(image)
                global dirname
                prepath = localPath / dirname
                buildpath = prepath / filename 

                image.save(buildpath)
                image.close()

                imageAfter = Image.open(buildpath)
                print("Exif After: ")
                PrintExifToConsole(imageAfter)

        except Exception as error: 
            print("Got an exception: " + error)
            print("Type: " + type(error))
            print("Not an image?")





def readCommandLineArgs():
    index = 0
    global runPath 
    systemArgs = sys.argv


    for arg in systemArgs:
        #print('arg: ' + arg)
        if(arg == '-p'):
            if(len(systemArgs)-1 < index+1):
                print('No path provided after argument -p')
                print('Correct syntax is: python '+ systemArgs[0] + ' -p /path/to/directory')
                exit(1)
            if(Path(systemArgs[index + 1]).is_dir()):
                runPath = Path(systemArgs[index + 1])
                index += 2
                continue
        elif(arg == '-f'):
            if(len(systemArgs)-1 < index+1):
                print('No path provided after argument -p')
                print('Correct syntax is: python '+ systemArgs[0] + ' -f /path/to/file')
                exit(1)
            if(Path(systemArgs[index + 1]).is_file()):
                runPath = Path(systemArgs[index + 1])
            else:
                print('not file')
        #print('index incr')

        elif(arg == '-h' or arg == 'h' or arg == '--help' or arg == 'help'):
            print('--- Help Menu ---')
            print('To clean exif on all files in a folder provide the folder path:')
            print('-p {folderpath}')
            print('To clean exif on a single file provide the file path:')
            print('-f {filepath}')
        index += 1




# Begin exectuion

readCommandLineArgs()
CreateNewExifCleanFolder(runPath)
CleanExifAllLocalImages(runPath)




