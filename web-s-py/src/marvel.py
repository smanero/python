#!/usr/bin/python3
import os
import time
from bs4 import BeautifulSoup
import zipper

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
   imgs = zipper.get_html(url).findAll('img', src=True, attrs={'class':'img-responsive img-vertical-card'})
   imgs_count = 0
   for img in imgs:
      title = "card-{}.jpg".format(card_idx)
      img_url = img['src']
      if not(img_url.startswith('http')):
         img_url = "https://es.marvelcdb.com" + img_url
      print(" " + title + ": " + img_url, )
      zipper.get_image(img_url, dir + "/" + title)
      imgs_count += 1
      inc_card_idx()
   print(url + " - Imagenes procesadas = {}".format(imgs_count))

def main():
   try:
      #gob
      URL = "https://es.marvelcdb.com/set/" + "trors"
      html = zipper.get_html(URL)
      scrapeMain(html, "TheRiseOfRedSkull")
   except Exception as e:
      print(e)

if __name__ == "__main__":
    main()
