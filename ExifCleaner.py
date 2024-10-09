# Clean exif data from a JPEG file 
from PIL import Image
from pathlib import Path
import os
import sys


# global vars

singleFile = False
verbose = False
recursive = False

filePath = Path.cwd()
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
    dirExists = True
    dirExists = os.path.exists(directory / dirname)  

    if(dirExists == False): 
        os.mkdir(directory / dirname)
        if(os.path.exists(directory / dirname)): 
            print('Created '+dirname+'')
        else:
            print('Failed to create the ' + dirname + 'direcory')

def CleanExifAllLocalImages(localPath):
    localFiles = listFilesInDir(localPath)

    for file in localFiles:
        try:
            HandleSingleImage(file)
        except Exception as error: 
            print("Got an exception: " + error)
            print("Type: " + type(error))
            print("Not an image?")

def HandleSingleImage(filepath): 
    # validate filepath
    try:
        if(os.path.isfile(filepath) == False):
            print("Path is not a file, faiure")
            exit(1)

        image = Image.open(filepath)
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
        print(error)


def readCommandLineArgs():
    global singleFile
    global recursive
    global verbose
    global runPath 
    global singeFile
    global filePath
    global file
    global dirname

    systemArgs = sys.argv
    index = 0

    for checkverbose in systemArgs:
        if(checkverbose == '-v' or checkverbose == '-V'):
            verbose = True


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
                if(verbose):
                    print('Got directory for images:')
                    print(runPath)
                continue
        elif(arg == '-f'):
            if(len(systemArgs)-1 < index+1):
                print('No path provided after argument -f')
                print('Correct syntax is: python '+ systemArgs[0] + ' -f /path/to/file')
                exit(1)
            if(Path(systemArgs[index + 1]).is_file()):
                singleFile = True
                filePath = Path(systemArgs[index + 1])
                if(verbose):
                    print('Single file useage on path:')
                    print(filePath)
            else:
                print('Path entered is not a file, double check your arguments')
                exit(1)
        elif(arg == '-r'):
            recursive = True
        elif(arg == '-h' or arg == 'h' or arg == '--help' or arg == 'help'):
            print('--- Help Menu ---')
            print('To clean exif on all files in a folder provide the folder path:')
            print('-p {folderpath}')
            print('To clean exif on a single file provide the file path:')
            print('-f {filepath}')
            print('-r Recursivly go through directoreis')
        index += 1




# Begin exectuion

readCommandLineArgs()


CreateNewExifCleanFolder(runPath)
CleanExifAllLocalImages(runPath)




