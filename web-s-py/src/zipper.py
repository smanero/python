#!/usr/bin/python3
import sys
import os
import zipfile
from zipfile import ZipFile
import requests
import shutil
from bs4 import BeautifulSoup

### unzip method
def unzip(zipname:str):
   if os.path.isfile(zipname):
      with ZipFile(zipname, 'r') as ziph:
         # Extract all the contents of zip file in current directory
         # ziph.extractall()
         fileNameList = ziph.namelist()
         for fileName in fileNameList:
            fileName = fileName.replace('../', '')
            ziph.extract(fileName)
   else:
      print('{} is not a file'.format(zipname))

### zip method
def zip(path2zip: str, zipname:str):
   ziph:ZipFile = None
   try:
      # ziph is zipfile handle
      ziph = zipfile.ZipFile(zipname, 'w', zipfile.ZIP_DEFLATED)
      if os.path.isdir(path2zip):  
         for root, dirs, files in os.walk(path2zip):
            for file in files:
               ziph.write(os.path.join(root, file))
      elif os.path.isfile(path2zip):
         ziph.write(path2zip)
   except Exception as e:
      print(e)
   finally:
      if ziph is not None:
         ziph.close()

##########################################################################
# FUNCTION Descargar una imagen dada una url
def get_image(img_url:str, fileName:str):
   # Open the url image, set stream to True, this will return the stream content.
   resp = requests.get(img_url, stream=True)
   # Open a local file with wb ( write binary ) permission.
   local_file = open(fileName, 'wb')
   # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
   resp.raw.decode_content = True
   # Copy the response stream raw data to local image file.
   shutil.copyfileobj(resp.raw, local_file)
   # Remove the image url response object.
   del resp
   # import wget
   # Invoke wget download method to download specified url image
   #local_image_filename = wget.download(img_url)
   #return local_image_filename

##########################################################################
#
def get_html(url:str) -> BeautifulSoup:
   print("Scrapping " + url)
   page = requests.get(url)
   soup = BeautifulSoup(page.content, 'html.parser')
   #print("page.content " + soup.prettify())
   return soup

### main method
def main():
   path2zip = 'tmp/'
   zipname = 'ziptest.zip'
   # print command line arguments
   # for arg in sys.argv[1:]:
      # print arg
   if (len(sys.argv) == 2):
      path2zip = sys.argv[1]
      zipname = sys.argv[2]
   zip(path2zip, zipname)

if __name__ == '__main__':
   main()