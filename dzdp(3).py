from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException
import requests
from bs4 import BeautifulSoup
import time
import random
import pandas as pd

def get_ua():
	user_agents = [
		'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 OPR/26.0.1656.60',
		'Opera/8.0 (Windows NT 5.1; U; en)',
		'Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.50',
		'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; en) Opera 9.50',
		'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0',
		'Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10',
		'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2 ',
		'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36',
		'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
		'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.133 Safari/534.16',
		'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36',
		'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
		'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11',
		'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER',
		'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)',
		'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 SE 2.X MetaSr 1.0',
		'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; SE 2.X MetaSr 1.0) ',
	]
	user_agent = random.choice(user_agents) #random.choice(),从列表中随机抽取一个对象
	return user_agent



def begin_search():

    input = browser.find_element_by_xpath('//*[@id="J-search-input"]')
    input.send_keys('西餐')
    button = browser.find_element_by_xpath('//*[@id="J-all-btn"]')
    button.click()

def get_regions():
    urls = []
    current_window = browser.current_window_handle
    all_window = browser.window_handles
    for handle in all_window:
        if handle !=  current_window:
            browser.switch_to.window(handle)
    time.sleep(3)
    button = browser.find_element_by_xpath('//*[@id="J_nav_tabs"]/a[2]')
    button.click()
    qus = browser.find_elements_by_xpath('//*[@id="region-nav"]//a')
    regions = []
    for qu in qus:
        regions.append(qu.get_attribute('href'))
    for region in regions:
        browser.get(region)
        places = browser.find_elements_by_xpath('//*[@id="region-nav-sub"]//a')
        if len(places) == 0:
            urls.append(region)
        for index in range(0,len(places)):
            # if places[index].get_attribute('class') != 'cur':
            urls.append(places[index].get_attribute('href'))
        time.sleep(3)
    return urls


def one_regions_urls(url):

    shop_urls = []
    browser.get(url)
    html = browser.page_source
    doc = BeautifulSoup(html,'lxml')
    contents = doc.find_all('div',attrs={'class':'tit'})
    for content in contents:
        item = content.find('a',attrs={'target':'_blank'})
        if item['href'] not in shop_urls:
            shop_urls.append(item['href'])
    return shop_urls

    # shop_urls = []
    #
    # headers = {
    #     'User-Agent': get_ua(),
    #     'Cookie':'_lxsdk_cuid=169d634d370c8-0bf4480804fc62-414c042a-100200-169d634d371c8; _lxsdk=169d634d370c8-0bf4480804fc62-414c042a-100200-169d634d371c8; _hc.v=f59b51af-51a0-115e-3bca-33c058a4c7dd.1554076981; s_ViewType=10; cy=2; cye=beijing; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; _lxsdk_s=169d634d372-29e-9dd-f53%7C%7C584'
    # }
    # html = requests.get(url, headers=headers).text
    # obj = BeautifulSoup(html, 'lxml')
    # pages = obj.find_all(attrs={'class': 'PageLink'})
    # for page in pages:
    #     print(page.text)
    # for i in range(1,3):
    #     new_url = url + 'p{}'.format(i)
    #     html = requests.get(new_url,headers = headers).text
    #     obj = BeautifulSoup(html)
    #     items = obj.find_all(attrs={'data-click-name':'shop_title_click'})
    #
    #     for item in items:
    #         shop_urls.append(item['href'])
    #     time.sleep(2)
    #
    #     return shop_urls



if __name__ == '__main__':
    browser = webdriver.Chrome()
    browser.get('https://www.dianping.com/shanghai')
    begin_search()
    region_urls = get_regions()
    for region_url in region_urls:
        with open('region_url.txt','a+') as fp:
            fp.write(region_url + '\n')

    f = open('region_url.txt','r')
    line = f.readline()
    while line:
        url = line
        if url != 'javascript:;\n':

            browser.get(url)
            try:
                last_page = int(browser.find_element_by_xpath('/html/body/div[2]/div[3]/div[1]/div[2]/a[last()-1]').text)
            except NoSuchElementException:
                last_page = 1
            for page in range(1,last_page + 1):
                new_url = url + 'p{}'.format(page)
                print(new_url)
                shop_urls = one_regions_urls(new_url)
                print(shop_urls)
                time.sleep(3)
                for shop_url in shop_urls:
                    with open('shop_urls.txt','a+') as fp:
                        fp.write(shop_url + '\n')
        line = f.readline()

f.close()


