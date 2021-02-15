#!/usr/bin/python3
import os
import time
import requests
import shutil
from bs4 import BeautifulSoup
import json

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

def get_html(url:str) -> BeautifulSoup:
   print("Scrapping " + url)
   page = requests.get(url)
   soup = BeautifulSoup(page.content, 'html.parser')
   #print("page.content " + soup.prettify())
   return soup

card_idx = 0

def inc_card_idx():
    global card_idx    # Needed to modify global copy of globvar
    card_idx += 1

# FUNCTION Scrape el resultado de busqueda en dos farma
def scrapeMain(html:BeautifulSoup, dir:str):
   if not os.path.exists(dir):
      os.makedirs(dir)
   cards = html.findAll('td', attrs={'data-th':'Name'})
   for card in cards:
      card_dt = card.find('a', href=True)
      title = card_dt.text.strip()
      img_url = card_dt['href']
      if not(img_url.startswith('http')):
         img_url = "https://es.marvelcdb.com/card/" + img_url
      scrapeIssue(img_url, dir)
      time.sleep(5)      

def scrapeIssue(url:str, dir:str):
   imgs = get_html(url).findAll('img', src=True, attrs={'class':'img-responsive img-vertical-card'})
   imgs_count = 0
   for img in imgs:
      title = "card-{}.jpg".format(card_idx)
      img_url = img['src']
      if not(img_url.startswith('http')):
         img_url = "https://es.marvelcdb.com" + img_url
      print(" " + title + ": " + img_url, )
      get_image(img_url, dir + "/" + title)
      imgs_count += 1
      inc_card_idx()
   print(url + " - Imagenes procesadas = {}".format(imgs_count))

def main():
   try:
      #gob
      URL = "https://es.marvelcdb.com/set/" + "trors"
      html = get_html(URL)
      scrapeMain(html, "TheRiseOfRedSkull")
   except Exception as e:
      print(e)

if __name__ == "__main__":
    main()
