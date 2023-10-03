from dictionary.dictionary_market import market_link_dict, market_replace_dict
from config.config import SHEET_FOR_MARKET

from functions.get_scan_time import GET_SCAN_TIME
from functions.get_write_arr_market import GET_WRITABLE_ARR
from functions.get_scan_marker import FIND_SCAN_MARKER
from functions.driver_init import DRIVER_INIT

from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

import redis
import json
import time
import re



sh = SHEET_FOR_MARKET
worksheet_list = sh.worksheets()

r = redis.Redis(host='localhost', port=6379, db=0)



def GPR(seller, worksheet_title):
    print()
    print('sheet_name ------->', worksheet_title)
    print('seller ----------->', seller, '\n')
    product_price_dict = {}
    
    link_dict = market_link_dict['gpr']
    replace_dict = market_replace_dict['gpr']

    driver = DRIVER_INIT()
    driver.maximize_window()
    wait_element = By.CSS_SELECTOR, "div.offers-list"
    try:
        for page_link in link_dict[worksheet_title]:
            driver.get(page_link)
            # time.sleep(3)
            wait(driver, 10).until(EC.visibility_of_element_located(wait_element))
            product_title = driver.find_element(By.CLASS_NAME, 'has-mb-1').text.strip().lower()
            product_title_cut = re.sub(r'\W', '', product_title)
            for word in replace_dict[worksheet_title]:
                product_title_cut = product_title_cut.replace(word, replace_dict[worksheet_title][word])
            select_block = driver.find_element(By.CLASS_NAME, 'block-form')
            driver.execute_script('arguments[0].scrollIntoView()', select_block)
            print('--->>>', product_title_cut)
            if worksheet_title == 'watch':
                # если на странице есть блок выбора Версии (Обычная и Nike+), нажать на Обычную версию 
                try:
                    device_version_selector = driver.find_element(By.XPATH, "//label[contains(text(),'Версия')]").find_element(By.XPATH, "..").find_element(By.XPATH, "//a[contains(text(),'Обычная')]")
                    device_version_selector.click()
                except:
                    pass
                # нажать на первый попавшийся цвет
                try:
                    device_color_selector = driver.find_element(By.XPATH, "//label[contains(text(),'Цвет')]").find_element(By.XPATH, "..").find_element(By.CLASS_NAME, 'button')
                    device_color_selector.click()
                except:
                    pass
                try:
                    device_size_selector = driver.find_element(By.XPATH, "//label[contains(text(),'Размер')]").find_element(By.XPATH, "..").find_elements(By.CLASS_NAME, 'button')
                    for device_size_select in device_size_selector:
                        device_size_select.click()
                        device_size = device_size_select.text.strip().lower().replace(' ', '').replace('мм', 'mm')
                        product_price = driver.find_element(By.CSS_SELECTOR, 'span.is-price').text.strip().replace('₽', '').replace(' ', '')
                        product_full_name = product_title_cut + device_size
                        product_price_dict.update( {product_full_name : product_price} )
                except:
                    pass
                try:
                    device_size_selector = driver.find_element(By.XPATH, "//label[contains(text(),'Корпус')]").find_element(By.XPATH, "..").find_elements(By.CLASS_NAME, 'button')
                    for device_size_select in device_size_selector:
                        device_size_select.click()
                        device_size = device_size_select.text.strip().lower().replace(' ', '').replace('мм', 'mm')
                        product_price = driver.find_element(By.CSS_SELECTOR, 'span.is-price').text.strip().replace('₽', '').replace(' ', '')
                        product_full_name = product_title_cut + device_size
                        product_price_dict.update( {product_full_name : product_price} )
                except:
                    pass            
                try:
                    driver.find_element(By.XPATH, "//label[text()='Цвет ремешка']")
                    product_price = driver.find_element(By.CSS_SELECTOR, 'span.is-price').text.strip().replace('₽', '').replace(' ', '')
                    product_price_dict.update( {product_title_cut : product_price} )
                    print(product_title_cut, product_price)
                except:
                    pass
            if worksheet_title == 'iphone' or worksheet_title == 'macbook':
                try:
                    driver.find_element(By.XPATH, "//label[text()='Память']")
                    color_element = driver.find_element(By.XPATH, "//label[text()='Цвет']")
                    color_block = color_element.find_element(By.XPATH, "..")
                    color_selector = color_block.find_element(By.CLASS_NAME, 'button')
                    color_selector.click()
                    ssd_element = driver.find_element(By.XPATH, "//label[text()='Память']")
                    ssd_block = ssd_element.find_element(By.XPATH, "..")
                    ssd_selector = ssd_block.find_elements(By.CLASS_NAME, 'button')
                    for ssd_select in ssd_selector:
                        ssd_select.click()
                        product_ssd = ssd_select.text.strip().lower().replace(' ', '').replace('гб', '').replace('1тб', '1024')
                        product_price = driver.find_element(By.CSS_SELECTOR, 'span.is-price').text.strip().replace('₽', '').replace(' ', '')
                        product_full_name = product_title_cut + product_ssd
                        product_price_dict.update( {product_full_name : product_price} )
                        print(product_full_name, product_price)
                except:
                    pass
    except:
        print('err')
    print(product_price_dict)
    GET_WRITABLE_ARR(product_price_dict, seller, worksheet_title, sh=sh)
    # delete_cache(driver)
    driver.close()
    driver.quit()

def HOUSE(seller, worksheet_title):
    print()
    print('sheet_name ------->', worksheet_title)
    print('seller ----------->', seller, '\n')
    product_price_dict = {}
    
    link_dict = market_link_dict['house']
    replace_dict = market_replace_dict['house']
    
    driver = DRIVER_INIT()
    driver.maximize_window()
    wait_element = By.ID, "order"
    try:
        for page_link in link_dict[worksheet_title]:
            driver.get(page_link)
            # time.sleep(3)
            wait(driver, 10).until(EC.visibility_of_element_located(wait_element))
            page = driver.page_source
            soup = BeautifulSoup(page, 'html.parser')
            product_title = soup.find('div', class_='section-header').text.strip().lower()
            product_title_cut = re.sub(r'\W', '', product_title)
            for word in replace_dict[worksheet_title]:
                product_title_cut = product_title_cut.replace(word, replace_dict[worksheet_title][word])
            print(product_title_cut)
            ads = soup.find_all('label', class_='w-100 shadow-sm rounded h-100')
            for ad in ads:
                if ad.find('p', class_='h5'):
                    product_ssd = ad.find('p', class_='h5').text.strip().lower()
                if ad.find('p', class_='mb-0 fw-bold'):
                    product_ssd = ad.find('p', class_='mb-0 fw-bold').text.strip().lower()
                product_ssd = re.sub(r'\W', '', product_ssd)
                for word in replace_dict[worksheet_title]:
                    product_ssd = product_ssd.replace(word, replace_dict[worksheet_title][word])
                product_price = ad.find('p', class_='price').text.strip().replace('₽', '').replace(' ', '')
                product_full_name = product_title_cut + product_ssd
                product_price_dict.update( {product_full_name : product_price} )
                print(product_full_name, product_price)
    except:
        print('err')
    print(product_price_dict)
    GET_WRITABLE_ARR(product_price_dict, seller, worksheet_title, sh=sh)
    driver.close()
    driver.quit()

def REBRO(seller, worksheet_title):
    print()
    print('sheet_name ------->', worksheet_title)
    print('seller ----------->', seller, '\n')
    product_price_dict = {}
    
    link_dict = market_link_dict['rebro']
    replace_dict = market_replace_dict['rebro']
    
    driver = DRIVER_INIT()
    driver.maximize_window()
    # try:
    for page_link in link_dict[worksheet_title]:
        print(page_link)
        driver.get(page_link)
        # page = driver.page_source
        # soup = BeautifulSoup(page, 'html.parser')
        # print(soup)
        product_title = driver.find_element(By.ID, 'pagetitle').text.strip()
        print('product_title', product_title)
        product_title_cut = re.sub(r'\W', '', product_title.lower()).replace('appleiphone', 'iphone')
        
        # select_block = driver.find_element(By.CLASS_NAME, 'nw__filter__item')
        select_block = driver.find_element(By.CSS_SELECTOR, 'label.nw__filter__item')
        driver.execute_script('arguments[0].scrollIntoView()', select_block)
        select_block.click()
        
        time.sleep(5)
        view_toggle = By.CLASS_NAME, 'nw__filter__item.bx-filter-param-label._active'
        wait(driver, 20).until(EC.visibility_of_element_located(view_toggle))
        ssd_select_block_title = driver.find_element(By.XPATH, "//span[text()='Выберите объём накопителя:']")
        # print(ssd_select_block_title.text)
        ssd_select_block_title_parent = ssd_select_block_title.find_element(By.XPATH, "..")
        ssd_select_block = ssd_select_block_title_parent.find_element(By.XPATH, "..")
        # print(ssd_select_block)
        ssd_selector = ssd_select_block.find_elements(By.CLASS_NAME, 'nw__filter__item')
        # product_price_cut = ''
        for ssd_select in ssd_selector:
            product_ssd = ssd_select.find_element(By.CSS_SELECTOR, 'span.nw__filter__item_prop_name').text.strip().lower().replace(' ', '').replace('1тб', '1024').replace('гб', '')
            product_price = ssd_select.find_element(By.CSS_SELECTOR, 'p.nw__filter__item_prop_dop').text.strip().lower().replace(' ', '').replace('₽', '')
            print('product_price', product_price)
            # ищет <br> перенос строки \n и убирает из строки все, что ижет после переноса
            for index, elem in enumerate(product_price):
                if elem == '\n':
                    product_price_cut = product_price[:index]
                    break
            product_full_name = product_title_cut + product_ssd
            product_price_dict.update( {product_full_name : product_price_cut} )
            print(product_full_name, product_price_cut)
    # except:
    #     print('err')
    # print(product_price_dict)
    # GET_WRITABLE_ARR(product_price_dict, seller, worksheet_title, sh=sh)
    driver.close()
    driver.quit()

def ISTUDIO(seller, worksheet_title):
    print()
    print('sheet_name ------->', worksheet_title)
    print('seller ----------->', seller, '\n')
    product_price_dict = {}
    
    link_dict = market_link_dict['istudio']
    replace_dict = market_replace_dict['istudio']
  
    driver = DRIVER_INIT()
    driver.maximize_window()
    wait_element = By.CLASS_NAME, 'normal_price'
    try:
        for page_link in link_dict[worksheet_title]:
            driver.get(page_link)
            # time.sleep(3)
            wait(driver, 10).until(EC.visibility_of_element_located(wait_element))
            product_title = driver.find_element(By.TAG_NAME, 'h1').text.strip().lower()
            product_title_cut = re.sub(r'\W', '', product_title)
            for word in replace_dict[worksheet_title]:
                product_title_cut = product_title_cut.replace(word, replace_dict[worksheet_title][word])
            product_price = driver.find_element(By.CLASS_NAME, 'normal_price').text.strip().replace(' ', '').replace('₽', '')
            product_price_dict.update( {product_title_cut : product_price} )
            print(product_title_cut, product_price)
    except:
        print('err')
    print(product_price_dict)
    GET_WRITABLE_ARR(product_price_dict, seller, worksheet_title, sh=sh)
    driver.close()
    driver.quit()

def APPLE_ROSTOV(seller, worksheet_title):  
    print()
    print('sheet_name ------->', worksheet_title)
    print('seller ----------->', seller, '\n')
    product_price_dict = {}
    
    link_dict = market_link_dict['applerostov']
    replace_dict = market_replace_dict['applerostov']
   
    driver = DRIVER_INIT()
    driver.maximize_window()
    wait_element = By.CSS_SELECTOR, 'div.price'
    try:
        for page_link in link_dict[worksheet_title]:
            print(page_link)
            driver.get(page_link)
            # wait(driver, 20).until(EC.visibility_of_element_located(wait_element))
            time.sleep(3)
            product_cart_list = driver.find_element(By.CLASS_NAME, 'cat-block').find_elements(By.CSS_SELECTOR, 'div.cat-item')
            for product_cart in product_cart_list:
                product_title = product_cart.find_element(By.CSS_SELECTOR, 'a.cat-item__name').text.strip().lower().replace(' ', '')
                product_title = re.sub(r'\W', '', product_title)
                for word in replace_dict[worksheet_title]:
                    product_title = product_title.replace(word, replace_dict[worksheet_title][word])
                product_price = product_cart.find_element(By.CSS_SELECTOR, 'div.cat-item__price').text.strip().lower().replace(' ', '').replace('нетвналичии', '').replace('снятспроизводства', '').replace('p.', '')
                product_price_dict.update( {product_title : product_price} )
                print(product_title, product_price)
    except:
        print('err')
    print(product_price_dict)
    driver.close()
    driver.quit()
    GET_WRITABLE_ARR(product_price_dict, seller, worksheet_title, sh=sh)

def YABLOKO_ROSTOV(seller, worksheet_title):
    print()
    print('sheet_name ------->', worksheet_title)
    print('seller ----------->', seller, '\n')
    product_price_dict = {}
    
    link_dict = market_link_dict['yabloko']
    replace_dict = market_replace_dict['yabloko']
    
    driver = DRIVER_INIT()
    driver.maximize_window()
    try:
        for page_link in link_dict[worksheet_title]:
                driver.get(page_link)
                time.sleep(3)
                page = driver.page_source
                soup = BeautifulSoup(page, 'html.parser')
                ads = soup.find_all('div', class_='product-layout')
                for ad in ads:
                    product_full_name = ad.find('h4').text.strip().lower().replace(' ', '')
                    product_full_name = re.sub(r'\W', '', product_full_name)
                    for word in replace_dict[worksheet_title]:
                        product_full_name = product_full_name.replace(word, replace_dict[worksheet_title][word])

                    product_price = ad.find('p', class_='price').text.strip().replace('₽', '').replace(' ', '').replace('.00р.', '')
                    product_price_dict.update( {product_full_name : product_price} )
                    print(product_full_name, product_price)
    except:
        print('err')
    print('product_price_dict --> \n', product_price_dict)
    GET_WRITABLE_ARR(product_price_dict, seller, worksheet_title, sh=sh)
    driver.close()
    driver.quit()

def RECOVER(seller, worksheet_title):
    print()
    print('sheet_name ------->', worksheet_title)
    print('seller ----------->', seller, '\n')
    product_price_dict = {}
    
    link_dict = market_link_dict['recover']
    replace_dict = market_replace_dict['recover']
    
    driver = DRIVER_INIT()
    driver.maximize_window()
    wait_element = By.CLASS_NAME, 'zone-dialog-item-link'
    try:
        for page_link in link_dict[worksheet_title]:
            driver.get(page_link)
            # ждет появления попапа и закрывает его
            popover_overlay = By.CLASS_NAME, 'popover-overlay'
            wait(driver, 10).until(EC.visibility_of_element_located(popover_overlay))
            popover_overlay = driver.find_element(By.CLASS_NAME, 'popover-overlay')
            popover_overlay.click()
            # выбирает город
            location = driver.find_element(By.CSS_SELECTOR, 'a.link-dotted-invert')
            location.click()
            # time.sleep(3)
            wait(driver, 10).until(EC.visibility_of_element_located(wait_element))
            city_list = driver.find_elements(By.CLASS_NAME, 'zone-dialog-item-link')
            for item in city_list:
                city = item.text.strip()
                if city == 'Ростов-на-Дону':
                    item.click()
                    break
            # строка пагинации
            pagination_block = By.CSS_SELECTOR, 'div.pagenumberer'
            product_name = By.CSS_SELECTOR, 'a.products-view-name-link'
            page_list = ''
            try:
                if wait(driver, 10).until(EC.visibility_of_element_located(pagination_block)) and wait(driver, 10).until(EC.visibility_of_element_located(product_name)):
                    pagination_block = driver.find_element(By.CSS_SELECTOR, 'div.pagenumberer').find_elements(By.CSS_SELECTOR, 'a')
                    for item in pagination_block:
                        page = driver.page_source
                        page_list = page_list + page
                        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                        try:
                            pagination_next = driver.find_element(By.CSS_SELECTOR, 'a.pagenumberer-next')
                            pagination_next.click()
                        except:
                            print('страничек нету')
            except:
                page = driver.page_source
                page_list = page_list + page
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            soup = BeautifulSoup(page_list, 'html.parser')
            driver.close()
            driver.quit()
            ads = soup.find_all('div', class_='products-view-block') #список элементов, содержащих данные
            for index, ad in enumerate(ads):
                product_title = ad.find('a', class_='products-view-name-link')
                product_price_main = ad.find('div', class_='price')
                if product_title:
                    product_title = product_title.text.strip().lower().replace(' ', '')
                    product_title_cut = re.sub(r'\W', '', product_title)
                    for word in replace_dict[worksheet_title]:
                        product_title_cut = product_title_cut.replace(word, replace_dict[worksheet_title][word])
                elif product_title == None:
                        product_title = '-'
                if product_price_main:
                    product_price_main = product_price_main.text.strip()
                    product_price_main = re.sub(r'\W', '', product_price_main.lower()).replace('свяжитесьснаминасчетцены', 'уточняйте').replace('руб', '')
                elif product_price_main == None:
                    product_price_main = '-'
                product_price_dict.update( {product_title_cut : product_price_main} )
                print(product_title_cut, product_price_main)
    except:
        print('err')
    print('product_price_dict >>>', product_price_dict)
    GET_WRITABLE_ARR(product_price_dict, seller, worksheet_title, sh=sh)
# не работает macbook
def APPLE161(seller, worksheet_title):
    print()
    print('sheet_name ------->', worksheet_title)
    print('seller ----------->', seller, '\n')
    product_price_dict = {}
    
    link_dict = market_link_dict['apple161']
    replace_dict = market_replace_dict['apple161']
  
    driver = DRIVER_INIT()
    driver.maximize_window()
    try:
        for page_link in link_dict[worksheet_title]:
            driver.get(page_link)
            wait_element = By.CSS_SELECTOR, 'div.tovaridright'
            wait(driver, 10).until(EC.visibility_of_element_located(wait_element))
            product_cart_list = driver.find_elements(By.CSS_SELECTOR, 'div.tovarid')
            for product_cart in product_cart_list:
                product_info = product_cart.find_element(By.CSS_SELECTOR, 'div.tovaridright')
                product_title = product_info.find_element(By.CSS_SELECTOR, 'h2').text.strip().lower()
                product_title_cut = re.sub(r'\W', '', product_title)
                for word in replace_dict[worksheet_title]:
                    product_title_cut = product_title_cut.replace(word, replace_dict[worksheet_title][word])
                if product_info.find_elements(By.CSS_SELECTOR, 'span.obem'):
                    ssd_selector = product_info.find_elements(By.CSS_SELECTOR, 'span.obem')
                if product_info.find_elements(By.CSS_SELECTOR, 'span.nakopitel'):
                    ssd_selector = product_info.find_elements(By.CSS_SELECTOR, 'span.nakopitel')
                for ssd_select in ssd_selector:
                    print('ssd_select --->>>', ssd_select.text)
                    ssd_select.click()
                    time.sleep(0.5)
                    product_ssd = ssd_select.text.strip().lower().replace(' ', '').replace('гб', '').replace('1тб', '1024')
                    product_price = product_info.find_element(By.CSS_SELECTOR, 'span.price').text.strip().lower().replace('руб.', '').replace(' ', '').replace('ценууточняйтепотелефону', 'уточняйте')
                    product_full_name = product_title_cut + product_ssd
                    product_price_dict.update( {product_full_name : product_price} )
                    print(product_full_name, product_price)
                driver.execute_script('arguments[0].scrollIntoView()', product_cart)
    except:
        print('err')
    driver.close()
    driver.quit()
    #
    print(product_price_dict)
    GET_WRITABLE_ARR(product_price_dict, seller, worksheet_title, sh=sh)
    
def ITEAM(seller, worksheet_title):
    worksheet_title = worksheet_title.lower()
    print()
    print('sheet_name ------->', worksheet_title)
    print('seller ----------->', seller, '\n')
    product_price_dict = {}
    
    link_dict = market_link_dict['iteam']
    replace_dict = market_replace_dict['iteam']          
    
    driver = DRIVER_INIT()
    driver.maximize_window()
    try:
        if worksheet_title == 'iphone':
            wait_element = By.XPATH, '//div[@data-edition-option-id = "Объем памяти"]'
            for page_link in link_dict[worksheet_title]:
                print(page_link)
                driver.get(page_link)
                time.sleep(1)
                if page_link == 'https://iteam61.ru/iphones/tproduct/286150581-344292385831-smartfon-apple-iphone-11-128gb-black' :
                    wait_element = By.CSS_SELECTOR, 'div.js-product-price'
                    wait(driver, 10).until(EC.visibility_of_element_located(wait_element))
                    product_title = driver.find_element(By.CLASS_NAME, 'js-store-prod-name').text.strip().lower()
                    product_title_cut = re.sub(r'\W', '', product_title)
                    for word in replace_dict[worksheet_title]:
                        product_title_cut = product_title_cut.replace(word, replace_dict[worksheet_title][word])
                    product_title_cut = 'iphone' + product_title_cut
                    print('--->>>', product_title_cut)
                    product_price = driver.find_element(By.CSS_SELECTOR, 'div.js-product-price').get_attribute('data-product-price-def').lower().replace(' ', '')
                    product_price_dict.update( {product_title_cut : product_price} )
                    continue
                wait(driver, 10).until(EC.visibility_of_element_located(wait_element))
                product_info_block = driver.find_element(By.CLASS_NAME, 't-store__prod-popup__info')
                product_title = product_info_block.find_element(By.CLASS_NAME, 'js-store-prod-name').text.strip().lower()
                product_title_cut = re.sub(r'\W', '', product_title)
                for word in replace_dict[worksheet_title]:
                    product_title_cut = product_title_cut.replace(word, replace_dict[worksheet_title][word])
                product_title_cut = 'iphone' + product_title_cut
                print('--->>>', product_title_cut)            
                product_ssd_selector = product_info_block.find_element(By.XPATH, '//div[@data-edition-option-id = "Объем памяти"]').find_elements(By.CSS_SELECTOR, 'label.t-product__option-item')    
                for product_ssd_select in product_ssd_selector:
                    product_ssd_select.click()
                    product_ssd = product_ssd_select.find_element(By.TAG_NAME, 'input').get_attribute('value').lower().replace('гб', '')
                    product_price = product_info_block.find_element(By.CLASS_NAME, 'js-store-price-wrapper').text.strip().replace(' ', '').replace('р.', '')
                    product_full_name = product_title_cut + product_ssd
                    product_price_dict.update( {product_full_name : product_price} )
        elif worksheet_title == 'macbook':
            for page_link in link_dict[worksheet_title]:
                # print(page_link)
                driver.get(page_link)
                time.sleep(1)
                if page_link == 'https://iteam61.ru/macbook/tproduct/343484960-243184189361-apple-macbook-air-13-m18256-space-gray':
                    wait_element = By.CSS_SELECTOR, 'div.js-store-prod-name'
                    wait(driver, 10).until(EC.visibility_of_element_located(wait_element))
                    product_title = driver.find_element(By.CLASS_NAME, 'js-store-prod-name').text.strip().lower()
                    product_title_cut = re.sub(r'\W', '', product_title)
                    for word in replace_dict[worksheet_title]:
                        product_title_cut = product_title_cut.replace(word, replace_dict[worksheet_title][word])
                    # product_title_cut = 'iphone' + product_title_cut
                    print('--->>>', product_title_cut)
                    product_price = driver.find_element(By.CSS_SELECTOR, 'div.js-product-price').get_attribute('data-product-price-def').lower().replace(' ', '')
                    product_price_dict.update( {product_title_cut : product_price} )
                    continue
                product_info_block = driver.find_element(By.CLASS_NAME, 't-store__prod-popup__info')
                # product_title
                product_title = product_info_block.find_element(By.CLASS_NAME, 'js-store-prod-name').text.strip().lower()
                product_title_cut = re.sub(r'\W', '', product_title)
                wait_element = By.XPATH, '//div[text()="Объем пaмяти"]'
                wait(driver, 10).until(EC.visibility_of_element_located(wait_element))
                for word in replace_dict[worksheet_title]:
                    product_title_cut = product_title_cut.replace(word, replace_dict[worksheet_title][word])
                print('--->>>', product_title_cut)
                # product_ssd
                product_ssd_selector = product_info_block.find_element(By.XPATH, '//div[@data-edition-option-id = "Объем пaмяти"]').find_elements(By.CSS_SELECTOR, 'label.t-product__option-item')
                for product_ssd_select in product_ssd_selector:
                    product_ssd_select.click()
                    product_ssd = product_ssd_select.find_element(By.TAG_NAME, 'input').get_attribute('value').lower().replace('гб', '')
                    product_price = product_info_block.find_element(By.CLASS_NAME, 'js-store-price-wrapper').text.strip().replace(' ', '').replace('р.', '')
                    product_full_name = product_title_cut + product_ssd
                    # print(product_full_name)
                    product_price_dict.update( {product_full_name : product_price} )
    except:
        print('err')
    print(product_price_dict)
    GET_WRITABLE_ARR(product_price_dict, seller, worksheet_title, sh=sh)
    driver.close()
    driver.quit()
    
    
    
    
def START_SCAN(worksheet):
    seller_list = {
                    'GPR'           : GPR,
                    'RECOVER'       : RECOVER,
                    'HOUSE'         : HOUSE,
                    'ЯБЛОКО'        : YABLOKO_ROSTOV,   # название в таблице : название функции 
                    'REBRO'         : REBRO,
                    'APPLE161'      : APPLE161,
                    'APPLE ROSTOV'  : APPLE_ROSTOV,
                    'ISTUDIO'       : ISTUDIO,
                    'ITEAM'         : ITEAM
    }
    actual_marker_dist = FIND_SCAN_MARKER(worksheet)
    for seller in actual_marker_dist:
        if actual_marker_dist[seller] == 'TRUE':
            try:
                seller_name = seller_list[seller]
                seller_name(seller, worksheet.title)
            except:
                print('ОШИБКА', seller)

def TIMER():
    # страница, на которой расположены ячейки с таймером
    worksheet_timer_page = sh.worksheet('timer')
    # scan_interval - время между опросами таблицы
    scan_interval = 30
    status_cell = worksheet_timer_page.find('STATUS')
    while True:
        time.sleep(.1)
        local_sec = time.localtime().tm_sec
        # добавляет ноль, если минуты до 10
        if len(str(local_sec)) == 1:
            local_sec = '0' + str(local_sec)
        # если прошло scan_interval, обновить время в таблице и проверить, не пора ли начать сканирование
        if (int(local_sec) % scan_interval) == 0 :
            local_time = time.strftime("%H:%M", time.localtime(time.time()))
            # print(local_time)
            # вывод локального времени сервереа в таблицу, в ячейку STATUS
            worksheet_timer_page.update_cell(status_cell.row + 1, status_cell.col, (local_time + ':' + str(local_sec)))
            # получает массив с временными метками | получается что делается опрос таблицы каждые scan_interval секунд
            # и каждый раз получает обновленные данные, если вдруг пользователь обновил время и интервал сканирования
            scan_time_arr = GET_SCAN_TIME(worksheet_timer_page)
            print(scan_time_arr)
            # не пора ли начать сканирование?
            for scan_marker in scan_time_arr:
                # print(scan_marker, local_time)
                if scan_marker == local_time:
                    print(local_time, 'SCAN')
                    worksheet_timer_page.update_cell(status_cell.row + 1, status_cell.col, 'SCAN')
                    #################
                    for worksheet in worksheet_list:
                        print('START_SCAN  --->>>')
                        START_SCAN(worksheet)
                        print('FINISH_SCAN --->>>')
                        # запись в redis
                        worksheet_title = worksheet.title
                        sellers_price_arr = sh.worksheet(worksheet_title).get_values()
                        json_list = json.dumps(sellers_price_arr)
                        r.set(worksheet_title, json_list)
                        # unpacked_list = json.loads(r.get(worksheet_title))
                        # print('unpacked_list --->', unpacked_list)
                        time.sleep(20)
                    #################
                    # если сканирование завершится ошибкой и время старта скана не прошло, а ошибка уже появилась
                    while scan_marker == local_time:
                        time.sleep(.1)
                        worksheet_timer_page.update_cell(status_cell.row + 1, status_cell.col, 'WAIT')
                        local_time = time.strftime("%H:%M", time.localtime(time.time()))
                        time.sleep(10)
                        print('pause')

# for worksheet in worksheet_list:
#     if worksheet.title == 'watch':
#         START_SCAN(worksheet)

# APPLE_ROSTOV('applerostov', 'watch')
# GPR('gpr', 'watch')
# APPLE161('apple161', 'watch')
# YABLOKO_ROSTOV('yabloko', 'watch')
# REBRO('rebro', 'iphone')
# RECOVER('recover', 'watch')

# ISTUDIO('istudio', 'iphone')

TIMER()
