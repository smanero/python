#!/usr/bin/python3
import os
import time
from bs4 import BeautifulSoup
import zipper
import threading
import time

class myThread (threading.Thread):
   def __init__(self, threadID, name, counter):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.counter = counter
   def run(self):
      print("%s: %s" % (self.name, time.ctime(time.time())))

# @see https://www.tutorialspoint.com/python/python_multithreading.htm
def run_threads():
   threads = []
   # create new threads
   thread1 = myThread(1, "Thread-1", 1)
   thread2 = myThread(2, "Thread-2", 2)
   # start new Threads
   thread1.start()
   thread2.start()
   # add threads to thread list
   threads.append(thread1)
   threads.append(thread2)
   # wait for all threads to complete
   for t in threads:
      t.join()
   print("Exiting Main Thread")

# FUNCTION Scrape el resultado de busqueda en dos farma
def scrapeMain(html:BeautifulSoup, dir:str, issue_idx:int):
   #headings = html.findAll('div', attrs={'class':'heading'})
   #title = headings[0].find('h3').text.replace(':', '_').replace(',', '_').replace(' ', '_')
   cover = html.find('div', attrs={'class':'col cover'}).find('img', src=True)
   img_url:str = cover['src']
   if not(img_url.startswith('http')):
      img_url = "https://readcomiconline.to" + img_url
   print("title: " + dir + "cover: " + img_url)


   cover_file = dir + "/cover.jpg"
   zipper.get_image(img_url, cover_file)

   issues = html.find('ul', attrs={'class':'list'}).findAll('li')
   for issue in issues:
      co = issue.find('a', href=True)
      co_title = co.find('span').text
      if -1 != co_title.find('#'):
         co_title = "issue-" + str(co_title[co_title.find('#')+1:]).zfill(3)
      if -1 != co_title.find('Part'):
         co_title = "issue-" + str(co_title[co_title.find('Part')+4:-1]).zfill(3)
      else:
         co_title = "issue-" + str(issue_idx).zfill(3)
      co_dir = dir + "/" + co_title
      co_url = "https://readcomiconline.to" + co['href']
      scrapeIssue(co_title, co_url, co_dir)
      # next issue
      issue_idx = issue_idx+1
      time.sleep(5)

def scrapeIssue(co_title:str, co_url:str, co_dir:str):
   print(" " + co_title + ": " + co_url)
   if not os.path.exists(co_dir):
         os.makedirs(co_dir)
   co_html = zipper.get_html(co_url).prettify()
   img_idx = 0
   html_idx: int = co_html.find('lstImages.push')
   while -1 != html_idx:
      co_html = co_html[html_idx:]
      img_url = co_html[:co_html.find('");')]
      img_url = img_url.replace('lstImages.push("', '').replace('")', '')
      img_title = "img-" + str(img_idx).zfill(3) + ".jpg"
      print(img_title + ": " + img_url)
      zipper.get_image(img_url, co_dir + "/" + img_title)
      # next img
      img_idx = img_idx+1
      co_html = co_html[co_html.find(';'):]
      html_idx = co_html.find('lstImages.push')
      time.sleep(5)

# execute ./bin/python3 src/comic-thread.py
def main():
   try:
      URL = 'https://readcomiconline.to/Comic/'
      title = 'The-Savage-Sword-Of-Conan'
      html = zipper.get_html(URL + title)
      # dir destiny
      dir = title.replace(':', '_').replace(',', '_').replace(' ', '_').replace('(', '').replace(')', '')
      if not os.path.exists(dir):
         os.makedirs(dir)
      
      issue_idx = 96
      scrapeMain(html, dir, issue_idx)

      zipper.zip(dir, dir + '.cbz')
      #scrapeIssue('TPB', 'https://readcomiconline.to/Comic/Marvel-Zombies-2006/TPB?id=158840', 'Marvel_Zombies_(2006)/issue-TPB')
   except Exception as e:
      print(e)

if __name__ == "__main__":
    main()
