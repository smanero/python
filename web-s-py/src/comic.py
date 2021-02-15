#!/usr/bin/python3
import os
import time
import requests
import shutil
from bs4 import BeautifulSoup
import json
import zipper

##########################################################################
# base website URL
URL : str = 'https://readcomiconline.to'

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

##########################################################################
# FUNCTION get cover url in a comic
def obtainComicCover(html:BeautifulSoup):
   cover = html.find('div', attrs={'class':'col cover'}).find('img', src=True)
   img_url:str = cover['src']
   if not(img_url.startswith('http')):
      img_url = URL + img_url
   return img_url

##########################################################################
# FUNCTION list all issues in a comic
def obtainComicIssues(html:BeautifulSoup):
   issues_to_do = []
   issue_idx : int = 1
   issues = html.find('ul', attrs={'class':'list'}).findAll('li')
   for issue in issues:
      co = issue.find('a', href=True)
      co_url : str = URL + co['href']
      co_title : str = co.find('span').text #.strip().split()
      co_prx : str = "issue-"
      if -1 != co_title.find('#'):
         issue_idx = int(co_title[co_title.find('#')+1:])
      elif -1 != co_title.find('Annual'):
         co_prx = "annual-"
         issue_idx = int(co_title[co_title.find('Annual')+7:])
      elif -1 != co_title.find('TPB'):
         co_prx = "tpb-"
         issue_idx = int(co_title[co_title.find('TPB')+4:])
      elif -1 != co_title.find('Part'):
         co_prx = "part-"
         issue_idx = int(co_title[co_title.find('Part')+4:-1])

      if issue_idx <= 176:
         co_title = co_prx + str(issue_idx).strip().zfill(3)
         issues_to_do.append('{"co_title":"'+co_title+'","co_url":"'+co_url+'"}')
         # next issue
         issue_idx = issue_idx+1
   return issues_to_do

##########################################################################
#
def obtainIssueImagesByHtml(co_html: BeautifulSoup):
   images_to_do = []
   img_idx : int = 0
   try:
      images = co_html.find('div', {'id':'divImage'}).find('img', src=True)
      for image in images:
         img_url:str = image['src']
         img_title = "img-" + str(img_idx).zfill(3) + ".jpg"
         images_to_do.append('{"img_title":"'+img_title+'","img_url":"'+img_url+'"}')
         # next img
         img_idx = img_idx+1
   except Exception as e:
      print(e)
      raise(e)
   return images_to_do

##########################################################################
#
def obtainIssueImagesByText(co_html: BeautifulSoup):
   images_to_do = []
   img_idx : int = 0
   co_html_str : str = co_html.prettify()
   try:
      html_idx : int = co_html_str.find('lstImages.push')
      if (-1 == html_idx):
         print("Error in html -> " + co_html_str)
         return -1
      while -1 != html_idx:
         co_html_str = co_html_str[html_idx:]
         img_url = co_html_str[:co_html_str.find('");')]
         img_url = img_url.replace('lstImages.push("', '').replace('")', '')
         img_title = "img-" + str(img_idx).zfill(3) + ".jpg"
         images_to_do.append('{"img_title":"'+img_title+'","img_url":"'+img_url+'"}')
         # next img
         co_html_str = co_html_str[co_html_str.find(';'):]
         html_idx = co_html_str.find('lstImages.push')
         img_idx = img_idx+1
   except Exception as e:
      print("Error in html -> " + co_html_str)
      raise(e)
   print(str(len(images_to_do)))
   return images_to_do

##########################################################################
# FUNCTION list all images in a issue
def obtainIssueImages(co_url : str):
   co_html : BeautifulSoup = get_html(co_url)
   # text treating
   images_to_do = obtainIssueImagesByText(co_html)
   #if 0 >= len(images_to_do):
      # html treating
      #obtainIssueImagesByHtml(co_html)
   return images_to_do

##########################################################################
# FUNCTION Scrape all images in an issue
def scrapeIssue(co_title:str, co_url:str, dir:str):
   print(" " + co_title + ": " + co_url)
   # create directory for an issue
   co_dir = dir + "/" + co_title
   if not os.path.exists(co_dir):
      os.makedirs(co_dir)
   # obtain images to get in an issue
   images_to_do = obtainIssueImages(co_url)
   for image_to_do in images_to_do:
      image = json.loads(image_to_do)
      img_title = image["img_title"]
      img_url = image["img_url"]
      print(img_title + ": " + img_url)
      get_image(img_url, co_dir + "/" + img_title)
      time.sleep(3)

##########################################################################
# FUNCTION Scrape all issues in a comic
def scrapeComic(html:BeautifulSoup, dir:str):
   # obtain cover of the comic
   img_url = obtainComicCover(html)
   cover_file = dir + "/cover.jpg"
   get_image(img_url, cover_file)
   print("title: " + dir + "cover: " + img_url)
   # obtain array of issues to scrape
   issues_to_do = obtainComicIssues(html)
   for issue_to_do in issues_to_do:
      issue = json.loads(issue_to_do)
      co_title = issue["co_title"]
      co_url = issue["co_url"]
      scrapeIssue(co_title, co_url, dir)
      time.sleep(5)

##########################################################################
# execute ./bin/python3 src/comic.py
#Mighty-Thor-At-the-Gates-of-Valhalla
#Conan-the-Barbarian-1970
#The-Savage-Sword-Of-Conan
#Conan-the-Barbarian-2019
#Red-Sonja-Omnibus
def main():
   try:
      # comic to scrape
      title : str = 'Conan-the-Barbarian-1970'
      # dir destiny
      dir = title.replace(':', '_').replace(',', '_').replace(' ', '_').replace('(', '').replace(')', '')
      if not os.path.exists(dir):
         os.makedirs(dir)
      # scrape all comic items
      html = get_html(URL + "/Comic/" + title)
      scrapeComic(html, dir)
      # zip result directory with cbz extension
      zipper.zip(dir, dir + '.cbz')
   except Exception as e:
      print(e)

if __name__ == "__main__":
    main()
