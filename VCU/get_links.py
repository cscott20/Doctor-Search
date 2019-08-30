import docob
import selenium
import time

writefile = "links.csv"
driver = docob.open_chrome(None)
driver.get('https://www.vcuhealth.org/find-a-provider/find-a-provider')
driver.implicitly_wait(30)

def next_page(driver):
    button = driver.find_element_by_xpath('//*[@id="ctl00_cphContent_ctl00_lbResultsNext"]/span')
    button.click()

def get_links(driver):
    links = []
    doc = driver.find_elements_by_class_name('fad-individual')
    for d in doc:
        d = d.find_element_by_tag_name('a')
        d = d.get_attribute('href')
        links.append(d)
    return(links)

def get_npis(driver):
    npi_lis = []
    npis = driver.find_elements_by_class_name('result-wrap')
    for npi in npis:
        npi = npi.find_elements_by_tag_name('input')
        npi2 = npi[2].get_attribute('value')
        npi_lis.append(npi2)
    return(npi_lis)

def get_stuff(driver):
    links = get_links(driver)
    npis = get_npis(driver)
    for i in range(len(npis)):
        writefile.write("{0},{1}\n".format(npis[i],links[i]))
 

page = 0
while True:
    try:
        writefile = open("writefile.csv", "a")
        get_stuff(driver)
        time.sleep(7)
        next_page(driver)
        writefile.close()
    except:
        print("encountered error")
        page -= 1
    page += 1
    print("page: " + str(page))
writefile.close() 
