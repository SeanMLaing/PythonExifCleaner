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


def ReadCommandLineArgs():
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
                #runPath = Path.parent(filePath)
                runPath = os.path.basename(filePath)
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



def SingleFileHandler(filepath):
    HandleSingleImage(filepath)

def HandleDir(dirpath):
    global recursive
    global verbose
    
    if(recursive):
        # get all dir in current
        # for each dir, call HandleDir
        print("if")    

    for file in ListFilesInDir(dirpath):
        HandleSingleImage(dirpath / file)

def ListChildDirs(localPath):
    return [f for f in Path(localPath).iterdir() if f.is_dir()]

def ListFilesInDir(directory):
    return [f for f in Path(directory).iterdir() if f.is_file()]

def PrintExifToConsole(image):
    try:
        for exif in image.getexif():
            print(exif)
    except:
        print("exception when printing exif to console")

def CreateNewExifCleanFolder(directory):
    global verbose
    global singleFile
    
    if(singleFile or IsImageFile):
        directory = os.path.dirname(directory)
        if(verbose):
            print("Provided directory is a file")
            print("new path:")
            print(directory)


    joinedDirPath = os.path.join(directory, dirname)

    dirExists = True
    dirExists = os.path.exists(joinedDirPath)  
    
    if(verbose):
        print("Checking if a clean folder exists")

    if(dirExists == False): 
        os.mkdir(joinedDirPath)
        if(os.path.exists(joinedDirPath)): 
            print('Created '+dirname+'')
        else:
            print('Failed to create the ' + dirname + 'direcory')

def CleanExifAllLocalImages(localPath):
    localFiles = ListFilesInDir(localPath)

    for file in localFiles:
        try:
            HandleSingleImage(file)
        except Exception as error: 
            print("Got an exception: " + error)
            print("Type: " + type(error))
            print("Not an image?")

def HandleSingleImage(filepath): 
    global verbose
    global dirname
    if(verbose):
        print("Starting single file")
    try:
        if(os.path.isfile(filepath) == False):
            print("Path is not a file, faiure")
            exit(1)
        if(verbose):
            print("check if filepath is an image:")
            print(filepath)

        if(IsImagePath(filepath) != True):
            # is not image, need to break
            if(verbose):
                print("Provided path is not an image file: ")
                print(filepath)
            print("Not a filepath, quitting...")
            exit(1)
        else:
            if(verbose):
                print("Got an image at: ")
                print(filepath)

        image = Image.open(filepath)
        if(image != 'undefined'): 
            filename = image.filename.split('/')[-1]
            if(verbose):
                print(filename)
                print("Exif Before: ")
                PrintExifToConsole(image)
            prepath = localPath / dirname
            buildpath = prepath / filename 

            image.save(buildpath)
            image.close()

            if(verbose):
                imageAfter = Image.open(buildpath)
                print("Exif After: ")
                PrintExifToConsole(imageAfter)
        image.close()
    except Exception as error:
        print("except at HandleSingleImage")
        print(error)

def IsImagePath(filepath):
    # returns true if provided filepath is an image
    supportedImageTypes = ["jpg", "jpeg", "tiff", "im"] 
    
    # dev code
    print(filepath)

    for imgtype in supportedImageTypes:
        try:
            if(verbose):
                print("Check if filetype is: " + imgtype)
            if(os.path.basename(filepath).endswith(imgtype)):
                return True
        except Exception as error:
            print("Not an image or failed to read file:")
            print(filepath)

    # If we got here it is not a supported image type
    print("Not an image or not a supported type:")
    print(filepath)
    return False



# Begin exectuion
# todo:
# put in method
# handle paths for multi / single / recursive
def main():
    print("Starting to clean exif from image(s)")
    global singleFile
    global runPath
    global verbose

    try:
        ReadCommandLineArgs()
        
        if(verbose):
            print("Got command line args")

        CreateNewExifCleanFolder(runPath)

        if(verbose):
            print("created folder")

        if(singleFile):
            HandleSingleImage(filePath)

        else:
            CleanExifAllLocalImages(runPath)
    except Exception as error:
        print("except at main")
        print(error)


    print("Exif Cleaner complete")

main()
