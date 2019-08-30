from bs4 import BeautifulSoup
from selenium import webdriver
import re
import requests
import csv
import time
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException

class Doctor:
    def __init__(self, npi, cigna_name, org, driver):
        #Initialize attributes
        root = "https://www.stonybrookmedicine.edu/profile?npi="
        self.driver = driver
        self.org = org
        self.npi = npi
        self.cigna_name = cigna_name
        self.name = None
        self.middle_initial = None
        self.first = None
        self.last = None
        self.in_directory = False
        self.education = []
        self.headshot = None
        self.profile_link = root + str(self.npi)
        self.address_list = []
        self.response = False #Does webpage load
        #Some profiles do not respond, and errors are populated when requests.get(url) is called.
        #Hence the following try/except block
        try: 
            #Record time it takes to get response
            start = time.time()
            self.driver.get(self.profile_link)
            end = time.time()
            self.response_time = end - start
            self.response = True
        except:
            self.response_time = 0 #if there is no response, make another calll ASAP. 
                                   #response time = 0 then delay = 0    

    def __repr__(self):
        doc = "Not in Directory"
        if self.in_directory:
            doc = "Name: {0}\nNPI: {1}\nProfile Link: {2}\nHeadshot Link: {3}\nEducation Records: {4}\nAddresses: {5}".format(self.name, self.npi, self.profile_link, self.headshot, self.education, self.address_list)
        return(doc)
    
    def check_in_dir(self):
        #checks if in directory. Grabs name at same time if in directory. Stores in self.name
        name = self.driver.find_elements_by_class_name("physician-name-lg")
        if name:
            self.in_directory = True
        else:
            self.profile_link = None
        return(self.in_directory)

    def update_name(self):
        name = self.driver.find_elements_by_class_name("physician-name-lg")
        #Parse name into first last middle initial, full name. Gets rid of ", MD"
        if name:
            name = name[0].text
            #Get rid of ", MD"
            name_list = name.split(",") 
            self.name = name_list[0]
            name_list = name_list[0].split(" ")
            if len(name_list) == 3 and name_list[1] != "": #Has first, last, and middle.
                self.middle_initial = str(name_list[1][0])
            else:
                self.middle_initial = None
            self.first = str(name_list[0])
            self.last = str(name_list[len(name_list)-1])

    def update_edu(self):
        #Search HTML for Education section
        #Append Education data into a list
        credentials = self.driver.find_elements_by_tag_name("strong")
        if credentials:
            if (credentials[0].text.split(":")[0] == "Board Certifications") and (len(credentials) > 1):
                edu = credentials[1]
            else:
                edu = credentials[0]
            c = edu.find_elements_by_xpath("..")
            for ele in c:
                ls = ele.text.split("\n")
                for element in ls:
                    lis = element.split(": ")
                    if len(lis) > 1:
                        self.education.append("Degree type: {0}\nInstitution: {1}\n".format(lis[0],lis[1]))
            
    def update_photo(self):
        badlis = ["https://www.stonybrookmedicine.edu/sites/default/files/webfiles/physician-picsnew/fad-male.png", "https://www.stonybrookmedicine.edu/sites/default/files/webfiles/physician-picsnew/fad-female.png"]
        #Grab photo URL from HTML data
        photo = self.driver.find_elements_by_class_name("bio-photo")
        if photo:
            self.headshot = (photo[0].value_of_css_property("background").split('url("')[1].split('")')[0])
        if self.headshot in badlis:
            self.headshot = None

    def update_location(self):
        #Get locations
        locations = self.driver.find_elements_by_class_name("bio-location")
        if locations:
            for loc in locations:
                item = ""
                soup = loc.get_attribute("innerHTML")
                soup = str(BeautifulSoup(soup, 'lxml')).split('div class="phone"')[0]
                stuff = (soup.split("<br/>"))
                stuff[0] = stuff[0].split("</a></div>")[1]
                stuff.pop()
                for thing in stuff:
                    thing = thing.split("<sup>")
                    thing = thing[0]
                    item += thing
                    item += "\n"
                self.address_list.append((item.strip() + "\n"))
        if self.address_list:
            self.address_list[len(self.address_list)-1] = self.address_list[len(self.address_list)-1].strip()
                
    def update(self):
        #update all attributes (scrape entire profile)
        if self.check_in_dir():
            self.update_name()
            self.update_edu()
            self.update_photo()
            self.update_location()

    def write_line_csv(self, f):
        #write a single line to the csv flile with provider's details
        #appends to file f, does not overwrite
        edu = ""
        for entry in self.education:
            edu += str(entry) +"\n"
        addy = ""
        for entry in self.address_list:
            addy += str(entry) +"\n"
        to_write = [self.npi, self.cigna_name, self.name, self.profile_link, self.in_directory, self.headshot, edu.strip(), addy.strip()]
        with open(f, 'a') as csvfile:
            fil = csv.writer(csvfile)
            fil.writerow(to_write)


# The following is not part of the Doctor Class 
# because you do not need a doctor object to create and write the csv file.

def write_header(f):
        #Creates and writes a header to file f
        #overwrites data in file f
        fil = open(f, "w")
        to_write = ["NPI","Name in Cigna Portal","Provider Name in Directory", "Organization", "Profile Link", "In Directory", "Headshot Link", "Education", "Locations", "Responded?"]
        with open(f, 'w') as csvfile:
            fil = csv.writer(csvfile)
            fil.writerow(to_write)
        csvfile.close()


def write_csv(f, doclis):
        #writes to file f, one line per doctor object
        #appends to file f, does not overwrite
        with open(f, 'a') as csvfile:
            fil = csv.writer(csvfile)
            for doctor in doclis:
                edu = ""
                for entry in doctor.education:
                    edu += str(entry) +"\n"
                addy = ""
                for entry in doctor.address_list:
                    addy += str(entry) +"\n"
                to_write = [doctor.npi, doctor.cigna_name, doctor.name, doctor.org, doctor.profile_link,
                            doctor.in_directory, doctor.headshot, edu.strip(), addy.strip(), 
                            doctor.response]
                fil.writerow(to_write)
            csvfile.close()


def open_chrome(headless):
    driver_location = '/Users/h12566/Downloads/chromedriver'
    if bool(headless):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        driver = webdriver.Chrome(driver_location, options = chrome_options)
    else:
        driver = webdriver.Chrome(driver_location)
    return(driver)

