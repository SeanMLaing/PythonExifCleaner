# Clean exif data from a JPEG file 
from PIL import Image
import os
import sys
#--------------------- Version 2 -------------------------

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
#-------Testing----------
#print(ProcessSingleImage(os.path.abspath("/home/blendedcookie/Pictures/exifImages/Canon.jpg")))
#--------------------- Version 2 -------------------------
# global vars

#singleFile = False
#verbose = False
#recursive = False
#
#filePath = Path.cwd()
#runPath = Path.cwd()
#file = Path.cwd()
#dirname = 'ExifCleanImages'
#
#
#def ReadCommandLineArgs():
#    global singleFile
#    global recursive
#    global verbose
#    global runPath 
#    global singeFile
#    global filePath
#    global file
#    global dirname
#
#    systemArgs = sys.argv
#    index = 0
#
#    for checkverbose in systemArgs:
#        if(checkverbose == '-v' or checkverbose == '-V'):
#            verbose = True
#
#
#    for arg in systemArgs:
#        #print('arg: ' + arg)
#        if(arg == '-p'):
#            if(len(systemArgs)-1 < index+1):
#                print('No path provided after argument -p')
#                print('Correct syntax is: python '+ systemArgs[0] + ' -p /path/to/directory')
#                exit(1)
#            if(Path(systemArgs[index + 1]).is_dir()):
#                runPath = Path(systemArgs[index + 1])
#                index += 2
#                if(verbose):
#                    print('Got directory for images:')
#                    print(runPath)
#                continue
#        elif(arg == '-f'):
#            if(len(systemArgs)-1 < index+1):
#                print('No path provided after argument -f')
#                print('Correct syntax is: python '+ systemArgs[0] + ' -f /path/to/file')
#                exit(1)
#            if(Path(systemArgs[index + 1]).is_file()):
#                singleFile = True
#                filePath = Path(systemArgs[index + 1])
#                #runPath = Path.parent(filePath)
#                runPath = os.path.basename(filePath)
#                if(verbose):
#                    print('Single file useage on path:')
#                    print(filePath)
#            else:
#                print('Path entered is not a file, double check your arguments')
#                exit(1)
#        elif(arg == '-r'):
#            recursive = True
#        elif(arg == '-h' or arg == 'h' or arg == '--help' or arg == 'help'):
#            print('--- Help Menu ---')
#            print('To clean exif on all files in a folder provide the folder path:')
#            print('-p {folderpath}')
#            print('To clean exif on a single file provide the file path:')
#            print('-f {filepath}')
#            print('-r Recursivly go through directoreis')
#        index += 1
#
#
#
#def SingleFileHandler(filepath):
#    HandleSingleImage(filepath)
#
#def HandleDir(dirpath):
#    global recursive
#    global verbose
#    global dirname 
#
#    if(recursive):
#        # get all dir in current
#        # for each dir, call HandleDir
#        if(verbose):
#            print("Recursive, looking through: ")
#            print(dirpath)
#        childDirs = ListChildDirs(dirpath)
#        for cdir in childDirs:
#            if(os.path.dirname == dirname):
#                continue
#
#            if(verbose):
#                print("Found a child dir: ")
#                print(cdir)
#            HandleDir(cdir)
#    
#    # check for the exif cleaned dir
#    CreateNewExifCleanFolder(dirpath)
#
#    for file in ListFilesInDir(dirpath):
#        HandleSingleImage(dirpath / file)
#
#def ListChildDirs(localPath):
#    return [f for f in Path(localPath).iterdir() if f.is_dir()]
#
#def ListFilesInDir(directory):
#    return [f for f in Path(directory).iterdir() if f.is_file()]
#
#def PrintExifToConsole(image):
#    try:
#        for exif in image.getexif():
#            print(exif)
#    except:
#        print("exception when printing exif to console")
#
#def CreateNewExifCleanFolder(directory):
#    global verbose
#    global singleFile
#    global dirname 
#    if(singleFile or IsImagePath(directory)):
#        directory = os.path.dirname(directory)
#        if(verbose):
#            print("Provided directory is a file")
#            print("new path:")
#            print(directory)
#
#
#    joinedDirPath = os.path.join(directory, dirname)
#
#    dirExists = True
#    dirExists = os.path.exists(joinedDirPath)  
#    
#    if(verbose):
#        print("Checking if a clean folder exists")
#
#    if(dirExists == False): 
#        os.mkdir(joinedDirPath)
#        if(os.path.exists(joinedDirPath)): 
#            print('Created '+dirname+'')
#        else:
#            print('Failed to create the ' + dirname + 'direcory')
#
#def CleanExifAllLocalImages(localPath):
#    localFiles = ListFilesInDir(localPath)
#
#    for file in localFiles:
#        try:
#            HandleSingleImage(file)
#        except Exception as error: 
#            print("Got an exception: " + error)
#            print("Type: " + type(error))
#            print("Not an image?")
#
#def HandleSingleImage(filepath): 
#    global verbose
#    global dirname
#    if(verbose):
#        print("Starting single file")
#    try:
#        if(os.path.isfile(filepath) == False):
#            print("Path is not a file, faiure")
#            exit(1)
#        if(verbose):
#            print("check if filepath is an image:")
#            print(filepath)
#
#        if(IsImagePath(filepath) != True):
#            # is not image, need to break
#            if(verbose):
#                print("Provided path is not an image file: ")
#                print(filepath)
#            print("Not a filepath, quitting...")
#            exit(1)
#        else:
#            if(verbose):
#                print("Got an image at: ")
#                print(filepath)
#
#        image = Image.open(filepath)
#        if(image != 'undefined'): 
#            filename = image.filename.split('/')[-1]
#            localPath = os.path.dirname(filepath)
#            if(verbose):
#                print(filename)
#                print("Exif Before: ")
#                PrintExifToConsole(image)
#            prepath = os.path.join(localPath, dirname) buildpath = os.path.join(prepath, filename) image.save(buildpath)
#            image.close()
#
#            if(verbose):
#                imageAfter = Image.open(buildpath)
#                print("Exif After: ")
#                PrintExifToConsole(imageAfter)
#        image.close()
#    except Exception as error:
#        print("except at HandleSingleImage")
#        print(error)
#
#def IsImagePath(filepath):
#    # returns true if provided filepath is an image
#    supportedImageTypes = ["jpg", "jpeg", "tiff", "im"] 
#    
#    # dev code
#    print(filepath)
#
#    for imgtype in supportedImageTypes:
#        try:
#            if(verbose):
#                print("Check if filetype is: " + imgtype)
#            if(os.path.basename(filepath).endswith(imgtype)):
#                return True
#        except Exception as error:
#            print("Not an image or failed to read file:")
#            print(filepath)
#
#    # If we got here it is not a supported image type
#    print("Not an image or not a supported type:")
#    print(filepath)
#    return False
#
#
#
## Begin exectuion
## todo:
## put in method
## handle paths for multi / single / recursive
#def main():
#    print("Starting to clean exif from image(s)")
#    global singleFile
#    global runPath
#    global verbose
#
#    try:
#        ReadCommandLineArgs()
#        
#        if(verbose):
#            print("Got command line args")
#
#        CreateNewExifCleanFolder(runPath)
#
#        if(verbose):
#            print("created folder")
#
#        if(singleFile):
#            HandleSingleImage(filePath)
#
#        else:
#            HandleDir(runPath)
#    except Exception as error:
#        print("except at main")
#        print(error)
#
#
#    print("Exif Cleaner complete")
#
#main()
