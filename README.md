# PythonExifCleaner

Create a copy of an image (or many images) in a new folder with only the image data, all exif data is removed on the copy.

## Options
-p {DirectoryPath}	Save a copy of all supported image types in the provided directory in a new directory')
-f {FilePath}		Save a copy of the provided file, if type is supported, in a new directory')
-r			When paired with the -p option recusively itterate through the directory and sub directories saving the supported image types in new directories in their parent folder
-h 			Print this help menu

## Supported Image Types
.jpg, .jpeg, .tiff, .im


## Useage examples:
The below example will recursively itterate through all the supported images in the user Pictures directory:
```python ExifCleaner.py -r -p ~/Pictures```

The below example will create a copy of the image ImageWithExifData.jpg and save it without any meta data in a new directory in the users Pictures directory:
```python ExifCleaner -f ~/Pictures/ImageWithExifData.jpg```
