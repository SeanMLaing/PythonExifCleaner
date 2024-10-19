# ExifCleaner - Sean Laing - Oct 2024
# Clean exif data from a JPEG file 
from PIL import Image
import os
import sys

# Global variables
RUNPATH = os.getcwd()
RECURSIVE = False
DIRECTORYNAME = "ExifCleanedImage"
SINGLEFILEMODE = False
SUPPORTEDFILETYPES = ["jpg", "jpeg", "tiff", "im"]


def ProcessSingleImage(FilePath):
    try:
        # verify it is a file not a dir
        if not os.path.isfile(FilePath): 
            NonBreakError('FilePath is not a file')
            return True

        # verify it is a supported filetype
        if not IsSupportedFileType(FilePath): 
            NonBreakError('FilePath is not a supported file type: ' + FilePath)
            return True

        # verify the exif cleaned dir exists in the files local dir
        workingpath = os.path.dirname(FilePath)
        if not DoesExifCleanedDirExistLocally(workingpath): 
            if not CreateLocalExifCleanDir(workingpath):
                return False

        cleandirpath = os.path.join(workingpath, DIRECTORYNAME)

        # open the file
        image = Image.open(FilePath)

        # save a new version in the exif cleaned dir
        if(SaveNewImage(image, cleandirpath) == False):
            return False
        image.close()

    except Exception as errmsg:
        HelpMenu(errmsg)

    # success
    return True


def SaveNewImage(IMG, CleanDirPath):
    try:
        imgname = IMG.filename.split('/')[-1]

        newimgpath = os.path.join(CleanDirPath, IMG.filename.split('/')[-1]) 
        IMG.save(newimgpath)

        if(os.path.exists(newimgpath)):
            if(os.path.isfile(newimgpath)):
                    return True            

    except Exception as errmsg:
        HelpMenu(errmsg)

    return False 


def IsSupportedFileType(FilePath):
    global SUPPOERTEDFILETYPES 

    try:
        for imgtype in SUPPORTEDFILETYPES:
            if(os.path.basename(FilePath).endswith(imgtype)):
                return True
    except Exception as errmsg:
        HelpMenu(errmsg)
        
    return False


def DoesExifCleanedDirExistLocally(FilePath):
    global DIRECTORYNAME

    try:
        fileroot = FilePath
        localdirs = os.listdir(fileroot)

        # VERIFY IF FILE PATH OR IF DIR PATH
        if not os.path.exists(FilePath):
            # not good here
            HelpMenu('Path not found when trying to create Clean Exif Directory')
        if(os.path.isfile(FilePath)):
            fileroot = os.path.dirname(FilePath)

        joinedpath = os.path.join(fileroot, DIRECTORYNAME)

        if(os.path.exists(os.path.join(fileroot, DIRECTORYNAME))):
            return True

    except Exception as error:
        HelpMenu(error)

    return False


def CreateLocalExifCleanDir(WorkingPath):
    global DIRECTORYNAME
   
    if(DoesExifCleanedDirExistLocally(WorkingPath)):
        return True
    
    dirfullpath = os.path.join(WorkingPath, DIRECTORYNAME)

    try:
        os.mkdir(dirfullpath)
        
        if(os.path.exists(dirfullpath)):
            return True
        else: 
            return False

    except Exception as errmsg:
        HelpMenu(errmsg)




def ProcessDirectory(DirectoryPath):
    global RECURSIVE
    # if file then no
    if not os.path.exists(DirectoryPath):
        HelpMenu('Attempted to process invalid path')

    if(os.path.isfile(DirectoryPath)):
        HelpMenu('Tried to process a file as a directory')
   
    for item in os.listdir(DirectoryPath):

        itemPath = os.path.join(DirectoryPath, item)

        if not os.path.exists(itemPath):
            HelpMenu('Got an invalid file path from the directory')

        if(os.path.isfile(itemPath)):
            if not ProcessSingleImage(itemPath):
                HelpMenu('Failed to process the supplied image or path')
        elif(RECURSIVE):
            ProcessDirectory(itemPath)

def NonBreakError(error):
    print('A file was not processed due to the error: ' + error)



def HelpMenu(error):
    print()
    print(error)
    print()
    print()
    print('Exif File Cleaner possible options:')
    print()
    print('Option:\t\t\tDescription')
    print()
    print('-p {DirectoryPath}\tSave a copy of all supported image types in the provided directory in a new directory')
    print()
    print('-f {FilePath}\t\tSave a copy of the provided file, if type is supported, in a new directory')
    print()
    print('-r\t\t\tWhen paired with the -p option recusively itterate through the directory and sub directories saving the supported image types in new directories in their parent folder')
    print()
    print('-h\t\t\tPrint this help menu') 


    exit(1)

def GetCommandLineArgs():
    global DIRPATH
    global FILEPATH
    global RECURSIVE
    global DIRECTORYNAME
    global SINGLEFILEMODE
   
    index = 1

    while index < len(sys.argv):
        arg = sys.argv[index]

        if(arg == '-r'):
            RECURSIVE = True
            index +=1 
        elif(arg == '-f'):
            # try parse the next arg as a path
            if(len(sys.argv)-1 < index +1):
                HelpMenu('No path after -f argument')

            if(os.path.exists(sys.argv[index + 1])):
                if not os.path.isfile(sys.argv[index +1]):
                    HelpMenu('Path after -f argument is not a file')

                SINGLEFILEMODE = True
                FILEPATH = sys.argv[index + 1]
                index += 2

        elif(arg == '-p'):
            if(len(sys.argv)-1 < index +1):
                HelpMenu('No path after -p argument')
            if not os.path.exists(sys.argv[index +1]):
                HelpMenu('Path after -p argument is not a valid path')
            if(os.path.isfile(sys.argv[index +1])):
                HelpMenu('Path after -p argument is a file, did you mean -f?');
            
            SINGLEFILEMODE = False
            FILEPATH = sys.argv[index +1]
            index += 2

        elif(arg == '-r'):
            RECURSIVE = True
            index += 1
        elif(arg == '-h'):
            HelpMenu('-h provided')
        else: 
            HelpMenu('Invalid argument ' + arg)
            index += 1




def main():
    global DIRPATH
    global FILEPATH
    global RECURSIVE
    global DIRECTORYNAME
    global SINGLEFILEMODE
    
    GetCommandLineArgs()

    if(SINGLEFILEMODE and RECURSIVE):
        HelpMenu('-f and -r cannot be used at the same time')
    elif(SINGLEFILEMODE):
        ProcessSingleImage(FILEPATH)
    else:
        ProcessDirectory(FILEPATH)


main()
