from selenium import webdriver
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys


def new_tab(driver, url):
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[len(driver.window_handles)-1])
    driver.get(url)

def switch_to_tab(driver, tab_num):
    driver.switch_to.window(driver.window_handles[tab_num])

f = open("fil.csv", "w")
global tabs, driver
pg_nm = 1
driver = webdriver.Chrome('/Users/h12566/Downloads/chromedriver')
srch_pg = 'https://www.centura.org/provider-search#!/?f%5B0%5D=location%20Colorado,%20USA&view=1&sortType=Alphabetical&page=' + str(pg_nm)
driver.get(srch_pg)
time.sleep(10)


tabs = {'search':1, 'profile':2}
count = 0 
while True:
    lks = driver.find_elements_by_class_name("m-card__detaillink")
    links = []
    for lk in lks:
        links.append(lk.get_attribute('href'))
    new_tab(driver, links[0])
    for link in links:
        driver.get(link)
        npi = driver.find_element_by_xpath('/html/head/meta[16]').get_attribute('content')
        f.write(str(link) + ","+ str((npi.split(" - ")[1][:10])))
        time.sleep(6)
        count += 1
        print(count)
    switch_to_tab(driver, 0)
    driver.find_element_by_xpath('//*[@id="main"]/section[2]/div/div[2]/div[2]/div/div/ul/li[12]/a').click()
    time.sleep(5)

