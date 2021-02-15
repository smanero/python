#!/usr/bin/python3
# -*- coding: utf-8 -*-

import pdb
import urllib.request
import os
import requests
import sys
import re
import json
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

##PARA ENVIAR MENSAJES AL BOT DE AVISO DE PRECIO
import telepot
TOKEN = 'xxxx:xxxxx' # Nuestro tokken del bot (el que @BotFather nos dió).
bot = telepot.Bot(TOKEN)
# import telebot # Librería de la API del bot.
# from telebot import types # Tipos para la API del bot.
# TOKEN = '884457178:xxxx' # Nuestro tokken del bot (el que @BotFather nos dió).
# bot = telebot.TeleBot(TOKEN) # Creamos el objeto de nuestro bot.
#pdb.set_trace()

def create_browser(webdriver_path):
    #create a selenium object that mimics the browser
    browser_options = Options()
    #headless tag created an invisible browser
    browser_options.add_argument("--headless")
    browser_options.add_argument('--no-sandbox')
    browser = webdriver.Chrome(webdriver_path, chrome_options=browser_options)
    print("Done Creating Browser")
    return browser

# def download(url):
# 	pdb.set_trace()
#     print("DESCARGA de la URL:" + url)
#     """Returns the HTML source code from the given URL
#         :param url: URL to get the source from.
#     """
#     headers = {'Accept-Encoding': 'identity, deflate, compress, gzip',
#         'Accept': '*/*','User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'
#     }
#     #headers = {
#     #'User-Agent': 'python-requests/1.2.0'
#     #}
#     try:
#         r = requests.get(url, headers=headers)
#         if r.status_code != 200:
#             sys.stderr.write("! Error {} retrieving url {}\n".format(r.status_code, url))
#             return None
#         #print(r.text)
#         return r
#     except Exception: # cuando ya no se encuentre la letra
#         print ('ERROR EN LA URL:', url)
#         return None   
def iniciarScraper():
	####PLAZA SUITES!!!!
	browser = webdriver.Chrome(executable_path=r'C:/Python27/chromedriver.exe')
	browser.minimize_window()
	browser.get('https://www.atrapalo.com/hoteles/3709-0_hotel-peniscola-plaza-suites?atoken=686ab371cba7d999e4247492fd13eafa')
	time.sleep(10)
	page_html = browser.page_source
	#print(str(page_html))
	productContainers = browser.find_elements_by_xpath("//div[@class='bloque-regimen-tarifa']")
	for productContainer in productContainers:
		textosContainer = productContainer.text
		time.sleep(1)
		enlaceContainer = productContainer
		if (textosContainer.find("Todo incluido") > -1):
			precioElement = productContainer.find_element_by_class_name("price")
			elPrecioXpath=precioElement.find_element_by_xpath(".//span")
			enlaceOferta = productContainer.find_elements_by_xpath(".//*[@class='row-tarifa column large-9 middle-table-block pad0']/a")
			print(elPrecioXpath.text)		
			elPrecio = elPrecioXpath.text
			elPrecioFinal = elPrecio[:len(elPrecio)-1]
			#print(elPrecioFinal)
			if (float(elPrecioFinal)<float("1.200")):
				bot.sendMessage(-xxxxxx,"PLAZA SUITES AL PRECIO: " + elPrecioFinal)
				bot.sendMessage(-xxxxxx,"LA URL ES: " + browser.current_url)
				print("PLAZA SUITES PRECIO MEJOR ENCONTRADO!!!!!!!!!!!!")
				#pdb.set_trace()
				#enlaceOferta = enlaceContainer.find_elements_by_xpath(".//*[@class='row-tarifa column large-9 middle-table-block pad0']/a")
				url = enlaceOferta[0].get_attribute("href")
				print(url)
				browser.get(url)
				browser.maximize_window()
				time.sleep(60000000)
				#bot.send_message( xxxxxx,'ATRAPALO JARDINES DEL PLAZA A '+ elPrecioFinal)
	#pdb.set_trace()
	print("ES MAYOR EN PLAZA SUITES")
	browser.close()
####DESTINIA PLAZA SUITES!!!!
	browser = webdriver.Chrome(executable_path=r'C:/Python27/chromedriver.exe')
	browser.minimize_window()
	browser.get('https://online.destinia.com/online/hotels/search/hotel/194467?date_unix=1590732831805263002')
	time.sleep(5)
	page_html = browser.page_source
	#print(str(page_html))
	productContainers = browser.find_elements_by_xpath("//div[@class='hotels-information-box']")
	for productContainer in productContainers:
		textosContainer = productContainer.text
		botonContainer = productContainer
		print (textosContainer)
		if (textosContainer.find("Todo incluido") > -1):
			#pdb.set_trace()
			precioElement = productContainer.find_element_by_class_name("price")
			elPrecioXpath=precioElement.find_element_by_xpath(".//span")
			boton=botonContainer.find_element_by_xpath(".//button")
			#print(elPrecioXpath.text)		
			elPrecio = elPrecioXpath.text
			elPrecioFinal = elPrecio[:len(elPrecio)-2]
			print("DESTINIA T.I: " + elPrecioFinal)
			if (float(elPrecioFinal)<float("1.620")):
				browser.execute_script("arguments[0].click();", boton)
				bot.sendMessage(-xxxxxx,"DESTINIA PLAZA SUITES AL PRECIO: " + elPrecioFinal)
				bot.sendMessage(-xxxxxx,"DESTINIA LA URL ES: " + browser.current_url)
				print("DESTINIA PLAZA SUITES PRECIO MEJOR ENCONTRADO!!!!!!!!!!!!")
				time.sleep(60000000)
				#bot.send_message( xxxxxx,'ATRAPALO JARDINES DEL PLAZA A '+ elPrecioFinal)
	#pdb.set_trace()
	print("ES MAYOR EN DESTINIA PLAZA SUITES")
	browser.close()			
	# ####PLAZA SUITES!!!!
	# browser = webdriver.Chrome(executable_path=r'C:/Python27/chromedriver.exe')
	# browser.minimize_window()
	# browser.get('https://www.atrapalo.com/hoteles/3709-0_hotel-peniscola-plaza-suites?atoken=fd037585e201280194a911ab5c74ba9a&utoken=1%3A10%3A0%3A0%3A3070a')
	# try:
	# 	WebDriverWait(browser, 60).until(EC.element_to_be_clickable((By.XPATH, "//button[@id='submitFormButton']"))).click()
	# 	print("10 NOCHES PULSADO BOTON EN PLAZA SUITES")	
	# except Exception as errorButton:
	# 	print(errorButton)
	# page_html = browser.page_source
	# #print(str(page_html))
	# productContainers = browser.find_elements_by_xpath("//div[@class='bloque-regimen-tarifa']")
	# for productContainer in productContainers:
	# 	textosContainer = productContainer.text
	# 	if (textosContainer.find("Todo incluido") > -1):
	# 		precioElement = productContainer.find_element_by_class_name("price")
	# 		elPrecioXpath=precioElement.find_element_by_xpath(".//span")
	# 		print(elPrecioXpath.text)		
	# 		elPrecio = elPrecioXpath.text
	# 		elPrecioFinal = elPrecio[:len(elPrecio)-1]
	# 		#print(elPrecioFinal)
	# 		if (float(elPrecioFinal)<float("1.660")):
	# 			bot.sendMessage(-xxxxxx,"10 NOCHES PLAZA SUITES AL PRECIO: " + elPrecioFinal)
	# 			bot.sendMessage(-xxxxxx,"10 NOCHES LA URL ES: " + browser.current_url)
	# 			print("10 NOCHES PLAZA SUITES PRECIO MEJOR ENCONTRADO!!!!!!!!!!!!")
	# 			time.sleep(60000000)
	# 			#bot.send_message( xxxxxx,'ATRAPALO JARDINES DEL PLAZA A '+ elPrecioFinal)
	# #pdb.set_trace()
	# print("10 NOCHES ES MAYOR EN PLAZA SUITES")
	# browser.close()
	
	###LASTMINUTE PLAZA SUITES!!!!!!
	# browser = webdriver.Chrome(executable_path=r'C:/Python27/chromedriver.exe')
	# browser.minimize_window()
	# browser.get('https://viajes.es.lastminute.com/viajes/route/product-details/2628959?search.departureIntervals=20200622-202000701&search.destinationCities=136365&search.rooms%5B0%5D.adults=2&search.rooms%5B0%5D.children=1&search.rooms%5B0%5D.childrenAge%5B0%5D=5&search.type=OSE&search.accomodationOnly=true&bf_subsource=S01HPV10S10RR01&checkin=20200622&checkout=20200701&sessionId=ece65e32-fc41-4154-b5f0-8c59770038dd&requestId=1809204094')
	# time.sleep(20)
	# page_html = browser.page_source	
	# productContainers = browser.find_elements_by_xpath("//ul[@class='filters-group']")
	# for productContainer in productContainers:
	# 	textosContainer = productContainer.text
	# 	wrappers = browser.find_elements_by_xpath("//div[@class='wrapper']")		
	# 	for wrapper in wrappers:
	# 		textosWrapper = wrapper.text			
	# 		if (textosWrapper.find("Todo incluido") > -1):
	# 			precioElement = wrapper.find_element_by_xpath(".//span[@class='info info--highlight']")
	# 			print(precioElement.text)		
	# 			elPrecio = precioElement.text
	# 			elPrecioFinal = elPrecio[6:len(elPrecio)-2]				
	# 			precioFinalInt = int(elPrecioFinal)
	# 			print("LASTMINUTE T.I: " + str(precioFinalInt))
	# 			if (precioFinalInt<1620):
	# 				bot.sendMessage(-xxxxxx,"LASTMINUTE PLAZA SUITES AL PRECIO: " + str(precioFinalInt))
	# 				bot.sendMessage(-xxxxxx,"LASTMINUTE LA URL ES: " + browser.current_url)
	# 				print("LASTMINUTE PLAZA SUITES PRECIO MEJOR ENCONTRADO!!!!!!!!!!!!")
	# 				time.sleep(60000000)
	# 				#bot.send_message( xxxxxx,'ATRAPALO JARDINES DEL PLAZA A '+ elPrecioFinal)
	# #pdb.set_trace()
	# print("ES MAYOR EN LASTMINUTE PLAZA SUITES")
	# browser.close()
	###JARDINES DEL PLAZA!!!!!!
	# browser = webdriver.Chrome(executable_path=r'C:/Python27/chromedriver.exe')
	# browser.minimize_window()
	# browser.get('https://www.atrapalo.com/hoteles/3699-0_aparthotel-jardines-del-plaza?atoken=245a9a1b8f3a0ad9af386e8af713a06e')
	# try:
	# 	time.sleep(5)
	# 	boton=browser.find_element_by_xpath("//button[@id='submitFormButton']")
	# 	boton.click()
	# 	print("PULSADO BOTON EN JARDINES DEL PLAZA")
	# except Exception as errorButton:
	# 	print(errorButton)
	# time.sleep(5)
	# page_html = browser.page_source
	# #print(str(page_html))
	# productContainers = browser.find_elements_by_xpath("//div[@class='bloque-regimen-tarifa']")
	# for productContainer in productContainers:
	# 	textosContainer = productContainer.text
	# 	if (textosContainer.find("Todo incluido") > -1):
	# 		precioElement = productContainer.find_element_by_class_name("price")
	# 		elPrecioXpath=precioElement.find_element_by_xpath(".//span")
	# 		print(elPrecioXpath.text)		
	# 		elPrecio = elPrecioXpath.text
	# 		elPrecioFinal = elPrecio[:len(elPrecio)-1]
	# 		#print(elPrecioFinal)
	# 		if (float(elPrecioFinal)<float("1.470")):
	# 			bot.sendMessage(-xxxxxx,"JARDINES DEL PLAZA AL PRECIO: " + elPrecioFinal)
	# 			bot.sendMessage(-xxxxxx,"LA URL ES: " + browser.current_url)
	# 			print("JARDINES DEL PLAZA PRECIO MEJOR ENCONTRADO!!!!!!!!!!!!")
	# 			time.sleep(60000000)
	# 			#bot.send_message( xxxxxx,'ATRAPALO JARDINES DEL PLAZA A '+ elPrecioFinal)
	# #pdb.set_trace()
	# print("ES MAYOR EN JARDINES DEL PLAZA")
	# browser.close()

while True:
	try:
		iniciarScraper()
		time.sleep(300)
	except Exception as excepcionScraper:
		print(excepcionScraper)
		time.sleep(300)
		iniciarScraper()

print ("FIN DEL WEBSCRAPER!!!!!")
################################################################################
################################################################################