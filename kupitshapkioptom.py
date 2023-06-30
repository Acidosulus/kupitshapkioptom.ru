from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import os
from my_library import *
import sys
import colorama
from colorama import Fore, Back, Style
from click import echo, style
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import os
from my_library import *
import colorama
from colorama import Fore, Back, Style
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import configparser
from lxml import html
import requests
from click import echo, style
from fake_useragent import UserAgent
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import uuid
from my_library import *
import colorama
from colorama import Fore, Back, Style
from urllib.parse import quote
from bs4 import BeautifulSoup as BS
from click import echo, style
from requests.auth import HTTPBasicAuth

class WD:
	def init(self):
		self.site_url = 'https://kupitshapkioptom.ru'
		self.autharization_url = 'https://kupitshapkioptom.ru/auth/sign-in-email.php?login=yes'
		print(Fore.RED + 'Chrome Web Driver '+Fore.YELLOW +self.autharization_url+Fore.RESET)
		chrome_options = webdriver.ChromeOptions()
		chrome_prefs = {}
		chrome_options.experimental_options["prefs"] = chrome_prefs
		#chrome_prefs["profile.default_content_settings"] = {"images": 2}
		#chrome_prefs["profile.managed_default_content_settings"] = {"images": 2}
		chrome_options.add_argument('--disable-gpu')
		chrome_options.add_argument("--disable-notifications")
		chrome_options.binary_location = "C:\Program Files\Google\Chrome\Application\chrome.exe"
		#chrome_options.add_argument('--headless')
		self.driver = webdriver.Chrome(chrome_options=chrome_options)
		self.driver.maximize_window()
		self.Get_HTML(self.autharization_url)
		time.sleep(1)
		self.driver.find_element(by=By.NAME, value='email').send_keys("acidos@yandex.ru")
		time.sleep(1)
		self.driver.find_element(by=By.NAME, value='password').send_keys("feloas852456")
		time.sleep(1)
		self.driver.find_element(by=By.NAME, value='password').send_keys("\n")
		time.sleep(2)

		return

		

	def __init__(self):
		self.init()
		if False:
			chrome_options = webdriver.ChromeOptions()
			chrome_prefs = {}
			chrome_options.experimental_options["prefs"] = chrome_prefs
			chrome_options.add_argument('--disable-gpu')
			chrome_options.add_argument("--disable-notifications")
			#chrome_options.add_argument('--headless')
			self.driver = webdriver.Chrome(options=chrome_options)
			self.driver.maximize_window()

	def __del__(self):
		try:
			pass
			#self.driver.quit()
		except: pass

	def Get_HTML(self, curl):
		if False:
			if os.path.isfile('response.html'):
					echo(style('Загружен локальный файл: ', fg='bright_red') + style('response.html', fg='red'))
					self.page_source = file_to_str('response.html')
			else:
				r = requests.get(curl)
				self.page_source = r.text
				str_to_file('response.html', self.page_source)
		else:
			self.driver.get(curl)
			return self.driver.page_source
 
		return self.page_source

	def Get_List_Of_Links_On_Goods_From_Catalog(self, pc_link):
		echo(style('Список товаров каталога: ', fg='bright_yellow') + style(pc_link, fg='bright_white'))
		list_of_pages =  self.Get_List_of_Catalog_Pages(pc_link)
		echo(style('Стрaницы каталога: ', fg='bright_yellow') + style(str(list_of_pages), fg='green'))
		ll_catalog_items = []
		for link in list_of_pages:
			self.Get_HTML(link)
			soup = BS(self.driver.page_source, features='html5lib')
			items = soup.find_all('a', {'class': 'catalog-item'})
			for item in items:
				lc_link = self.site_url + item['href']
				echo(style('Товар каталога: ', fg='bright_green') + style(lc_link, fg='green'))
				append_if_not_exists(lc_link, ll_catalog_items)
		return ll_catalog_items

	
	def Get_List_of_Catalog_Pages(self, pc_href:str) -> list:
		ll = []
		self.Get_HTML(pc_href)
		soup = BS(self.driver.page_source, features='html5lib')
		paginator = soup.find('ul',{'class':'pagination'}).find_all('a')
		lc_max = '0'
		for link in paginator:
			try:
				lc_link = link['href']
				lc_first_part = self.site_url + sx("|"+lc_link,'|','=') + '='
				lc_number = sx(lc_link+'|','=','|')
				lc_max = str(max([int(lc_max),int(lc_number)]))
			except Exception as e:
				print('Error: '+'Error on line {}'.format(sys.exc_info()[-1].tb_lineno) +'\n\n' + type(e).__name__ +'\n\n' + e.__str__())
				print('Link_Error')
		for i in range(1,int(lc_max)+1):
			ll.append(f'{lc_first_part}{str(i)}')
		if len(ll)==0:
			ll.append(pc_href)
		return ll
		

	def Get_Next_Page_in_Catalog(self, pc_link:str) -> str:
		echo(style('Find next page for: ', fg='bright_cyan') + style(pc_link,  fg='bright_green'))
		lc_link_result = ''
		return lc_link_result

	def Write_To_File(self, cfilename):
		file = open(cfilename, "w", encoding='utf-8')
		file.write(self.page_source)
		file.close()


def Login():
	return WD()



def poiskpers(url):
	geourl = '{0}'.format(quote(url))
	return geourl

class Good:
	def __init__(self, ol:WD, pc_good_link, pc_price:str):
		pc_good_link = pc_good_link.replace(r'amp;', '')
		self.site_url = 'https://kupitshapkioptom.ru'
		self.pictures = []
		self.sizes = []
		self.prices = []
		self.color = ''
		self.article = ''
		self.name = ''
		self.description= ''
		self.price = ''
		self.brand = ''
		self.goods = []
		echo(style('Товар: ', fg='bright_yellow') + style(pc_good_link, fg='bright_white') + style('  Прайс:', fg='bright_cyan') + style(pc_price, fg='bright_green'))
		ol.Get_HTML(pc_good_link)
		soup = BS(ol.driver.page_source, features='html5lib')

		try:self.description = reduce(prepare_str(soup.find('div', {'class':'catalog-el__info-bottom'}).text)).replace('Описание и характеристики','').strip()
		except:pass
		#try:self.description = self.description + ' ' + reduce(prepare_str(  soup.find_all('div', {'class':'item_info_section'})[1].text  )).strip().replace("$(document).ready(function () { setInterval(function () { var colors = new Array() $('.bx_scu li:visible i').each(function () { colors.push($(this).attr('title')) }) $('.js-ps-color').text(colors.join(', ')) }, 1000) })",'')
		#except:pass
		echo(style('Описание: ', fg='yellow') + style(self.description, fg='bright_white'))

		

		self.name = reduce(prepare_str(soup.find('div', {'class':'catalog-el__title'}).find('h1').text)).strip()
		echo(style('Название: ', fg='yellow') + style(self.name, fg='bright_white'))
		self.price = '0'
		self.price = reduce(prepare_str(soup.find('div', {'class':'price'}).text)).strip()
		echo(style('Цена: ', fg='yellow') + style(self.price, fg='bright_blue'))

		'catalog-el__size'
		good_groups = soup.find_all('div', {'class':'catalog-el__size'})
		
		for good_group in good_groups:
			group_name = good_group.find('h3').text
			#print(group_name)
			group_items = good_group.find_all('div', {'class':'catalog-el__size-card'})
			for group_item in group_items:
				lc_picture_link = self.site_url + group_item.find('img',{'class':'img-fluid'})['src']
				self.pictures.append(lc_picture_link)
				self.sizes.append(f'{group_name} - {group_item.text.strip()}')
				print(f'{group_name} -> {group_item.text.strip()} -> {lc_picture_link}')
				
			


def unload_one_good(dw:WD, lc_link_on_good: str, pc_price:str):
	lo_good = Good(dw, lc_link_on_good, pc_price)
	print(Fore.YELLOW + "Название:" + Fore.LIGHTCYAN_EX, lo_good.name, Fore.RESET)
	print(Fore.YELLOW + "Описание:" + Fore.LIGHTGREEN_EX, lo_good.description, Fore.RESET)
	print(Fore.YELLOW + "Цена:" + Fore.LIGHTRED_EX, lo_good.price, Fore.RESET)
	print(Fore.YELLOW + "Картинки:" + Fore.LIGHTBLACK_EX, lo_good.pictures, Fore.RESET)
	print(Fore.YELLOW + "Размеры:" + Fore.LIGHTBLUE_EX, lo_good.sizes, Fore.RESET)
	return lo_good


########################################################################################################################
########################################################################################################################
colorama.init()
########################################################################################################################
########################################################################################################################

if sys.argv[1] == 'good':
	wd = Login()

	print(sys.argv[1])
	print(sys.argv[2])
	links_list = [sys.argv[2]]
	print('Список товаров:', links_list)
	ln_total = len(links_list)
	ln_counter = 0
	price = Price(sys.argv[3])
	for link in links_list:
		ln_counter = ln_counter + 1
		print('Товар: ', link, Fore.LIGHTWHITE_EX, ln_counter, '/', ln_total, Fore.RESET)
		if is_price_have_link(sys.argv[3], link):
			print('Товар уже имеется в прайсе')
			continue
		lo_good = unload_one_good(wd, link, sys.argv[3])
		if int(round(float(lo_good.price.replace(',', '.').replace('₽','').replace(' ', ''))*float(sys.argv[4]), 2))!=0:
			price.add_good('',
									prepare_str(lo_good.name),
									prepare_str(lo_good.description),
									prepare_str( str(round(float(lo_good.price.replace(',', '.').replace('₽','').replace(' ', ''))*float(sys.argv[4]), 2))),
									'15',
									prepare_str(link),
									prepare_for_csv_non_list(lo_good.pictures),
									prepare_for_csv_list(lo_good.sizes))
			price.write_to_csv(sys.argv[3])
		else:
			echo(style('НУЛЕВАЯ ЦЕНА ТОВАРА', fg='bright_red'))


if sys.argv[1] == 'catalog':
	wd = Login()
	links_list = wd.Get_List_Of_Links_On_Goods_From_Catalog(sys.argv[2])
	print('Список товаров:', links_list)
	ln_total = len(links_list)
	ln_counter = 0
	price = Price(sys.argv[3])
	for link in links_list:
		ln_counter = ln_counter + 1
		print('Товар: ', link, Fore.LIGHTWHITE_EX, ln_counter, '/', ln_total, Fore.RESET)
		if is_price_have_link(sys.argv[3], link):
			print('Товар уже имеется в прайсе')
			continue
		lo_good = unload_one_good(wd, link, sys.argv[3])
		if int(round(float(lo_good.price.replace(',', '.').replace('₽','').replace(' ', ''))*float(sys.argv[4]), 2))!=0:
			price.add_good('',
									prepare_str(lo_good.name),
									prepare_str(lo_good.description),
									prepare_str( str(round(float(lo_good.price.replace(',', '.').replace('₽','').replace(' ', ''))*float(sys.argv[4]), 2))),
									'15',
									prepare_str(link),
									prepare_for_csv_non_list(lo_good.pictures),
									prepare_for_csv_list(lo_good.sizes))
			price.write_to_csv(sys.argv[3])
		else:
			echo(style('НУЛЕВАЯ ЦЕНА ТОВАРА', fg='bright_red'))


if sys.argv[1] == 'reverse':
	reverse_csv_price(sys.argv[2])

if sys.argv[1] == 'ansi':
	convert_file_to_ansi(sys.argv[2] + '_reversed.csv')

try: pass #wd.driver.quit()
except: pass