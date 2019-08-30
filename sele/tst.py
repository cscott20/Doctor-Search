from selenium import webdriver
chrome_options = webdriver.ChromeOptions()
#chrome_options.add_argument('--headless')
driver = webdriver.Chrome('/Users/h12566/Downloads/chromedriver', options = chrome_options)

def new_tab(driver, url):
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[len(driver.window_handles)-1])
    driver.get(url)
while True:
    url = input("url: ")
    new_tab(driver, url)
