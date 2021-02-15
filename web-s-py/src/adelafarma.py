#!/usr/bin/python3
from bs4 import BeautifulSoup
import csv
import pandas as pd
import requests
import wget
import json

# FUNCTION Descargar una imagen dada una url
def wget_image(img_url:str):
   # Invoke wget download method to download specified url image
   local_image_filename = wget.download(img_url)
   return local_image_filename
   #import requests
   #import shutil
   # This is the image url.
   #image_url = "https://www.dev2qa.com/demo/images/green_button.jpg"
   # Open the url image, set stream to True, this will return the stream content.
   #resp = requests.get(image_url, stream=True)
   # Open a local file with wb ( write binary ) permission.
   #local_file = open('local_image.jpg', 'wb')
   # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
   #resp.raw.decode_content = True
   # Copy the response stream raw data to local image file.
   #shutil.copyfileobj(resp.raw, local_file)
   # Remove the image url response object.
   #del resp

# FUNCTION Scrape el resultado de busqueda en dos farma
def scrape_articulo(num:int, name:str):
   page = requests.get(URL)
   soup = BeautifulSoup(page.content, 'html.parser')

   for a in soup.findAll('a',href=True, attrs={'class':'_31qSD5'}):
      print(a['href'])
      break
   for a in soup.findAll('a',href=True, attrs={'class':'_31qSD5'}):
      name=a.find('div', attrs={'class':'_3wU53n'})
      price=a.find('div', attrs={'class':'_1vC4OE _2rQ-NK'})
      img=a.find('div', attrs={'class':'_1Nyybr _30XEf0'})
      if None in (name, price, img):
         continue
      products.append(name.text)
      prices.append(price.text)
      imgs.append(wget_image(img.src))
      break
   return None

products=[] #List to store name of the product
prices=[] #List to store price of the product
imgs=[] #List to store rating of the product
URL = 'https://www.flipkart.com/laptops/buyback-guarantee-on-laptops-/pr?sid=6bo%2Cb5g&uniq'

with open("./assets/articulos.csv", "r") as f:
   reader = csv.reader(f, delimiter="\t")
   for i, line in enumerate(reader):
      print("linea[{0}] = {1}".format(i, line[1]))
      scrape_articulo(i, line[1])
   df = pd.DataFrame({'Product Name':products,'Price':prices}) 
   df.to_csv('./assets/products.csv', index=False, encoding='utf-8')

  
# results = soup.find(id='ResultsContainer')
# print(results.prettify())
# job_elems = results.find_all('section', class_='card-content')
# python_jobs = results.find_all('h2', string='Python Developer')
# python_jobs = results.find_all('h2', string=lambda text: "python" in text.lower())
# for p_job in python_jobs:
#  link = p_job.find('a')['href']
#  print(p_job.text.strip())
#  print(f"Apply here: {link}\n")
# if None in (title_elem, company_elem, location_elem):
#  continue
