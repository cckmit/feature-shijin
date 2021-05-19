from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time,os,xlrd
from selenium.common.exceptions import NoSuchElementException

driver = webdriver.Chrome(r'../国家药品监督管理局/chromedriver(1).exe')
driver.set_window_size(2000,1000)
driver.get('https://www.baidu.com')

driver.find_element_by_id('kw').send_keys("明星")
driver.find_element_by_id('su').click()
while True:
    time.sleep(1)
    aa = driver.find_element_by_xpath('//div[@class="op_exactqa_itemsArea c-row "]/div[1]/p[2]/a').text
    print(aa)
    aa = driver.find_element_by_xpath('//div[@class="op_exactqa_itemsArea c-row "]/div[2]/p[2]/a').text
    print(aa)
    aa = driver.find_element_by_xpath('//div[@class="op_exactqa_itemsArea c-row "]/div[3]/p[2]/a').text
    print(aa)
    aa = driver.find_element_by_xpath('//div[@class="op_exactqa_itemsArea c-row "]/div[4]/p[2]/a').text
    print(aa)
    aa = driver.find_element_by_xpath('//div[@class="op_exactqa_itemsArea c-row "]/div[5]/p[2]/a').text
    print(aa)
    aa = driver.find_element_by_xpath('//div[@class="op_exactqa_itemsArea c-row "]/div[6]/p[2]/a').text
    print(aa)
    aa = driver.find_element_by_xpath('//div[@class="op_exactqa_itemsArea c-row "]/div[7]/p[2]/a').text
    print(aa)
    aa = driver.find_element_by_xpath('//div[@class="op_exactqa_itemsArea c-row "]/div[8]/p[2]/a').text
    print(aa)
    aa = driver.find_element_by_xpath('//div[@class="op_exactqa_itemsArea c-row "]/div[9]/p[2]/a').text
    print(aa)
    aa = driver.find_element_by_xpath('//div[@class="op_exactqa_itemsArea c-row "]/div[10]/p[2]/a').text
    print(aa)
    aa = driver.find_element_by_xpath('//div[@class="op_exactqa_itemsArea c-row "]/div[11]/p[2]/a').text
    print(aa)
    aa = driver.find_element_by_xpath('//div[@class="op_exactqa_itemsArea c-row "]/div[12]/p[2]/a').text
    print(aa)
    driver.find_element_by_xpath('//span[@class="opui-page-next OP_LOG_BTN"]').click()