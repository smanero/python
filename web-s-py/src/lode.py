#!/usr/bin/python3
import os
import zipper

##########################################################################
# base website URL
URL : str = 'http://laorbitadeendor.com/'


##########################################################################
# execute ./bin/python3 src/comic.py
def main():
   try:
      # comic to scrape
      title : str = 'Conan-the-Barbarian-1970'
      # dir destiny
      dir = "LODE"
      if not os.path.exists(dir):
         os.makedirs(dir)
      # scrape
      for num in ["1","2","3","4","5","6","7","8","9","10","11","12"]:
         temp = zipper.get_html(URL + "/category/lode/temporada-"+num+"/")

      # div.id=categorying - img.src
      issues = temp.find('ul', attrs={'class':'list'}).findAll('li')

      # zip result directory with cbz extension
      zipper.zip(dir, dir + '.cbz')
   except Exception as e:
      print(e)

if __name__ == "__main__":
    main()
