from bs4 import BeautifulSoup
import re
import requests
import csv
import time

class Doctor:
    def __init__(self, npi, cigna_name, org):
        #Initialize attributes
        self.npi = npi
        self.org = org
        self.cigna_name = cigna_name
        self.name = None
        self.middle_initial = None
        self.first = None
        self.last = None
        self.in_directory = False
        self.education = []
        self.headshot = None
        self.profile_link = "https://nyulangone.org/doctors/{0}".format(self.npi)
        self.address_list = []
        self.response = False #does requests.get(url) return a valid object
        #Some profiles do not respond, and errors are populated when requests.get(url) is called.
        #Hence the following try/except block
        try: 
            #Record time it takes to get response
            start = time.time()
            #Get "soup" HTML Doc
            res = requests.get(self.profile_link).text
            end = time.time()
            self.soup = BeautifulSoup(res, 'lxml') 
            self.response_time = end - start
            self.response = True
        except:
            self.soup = ""
            self.response_time = 0 #if there is no response, make another calll ASAP. 
                                   #response time = 0 then delay = 0    
    
    def __repr__(self):
        #For testing purposes, prints doctor objects nicely.
        doc = "Not in Directory"
        if self.in_directory:
            doc = "Name: {0}\nNPI: {1}\nProfile Link: {2}\nHeadshot Link: {3}\nEducation Records: {4}\nAddresses: {5}".format(self.name, self.npi, self.profile_link, self.headshot, self.education, self.address_list)
        return(doc)
    
    def check_in_dir(self):
        if not self.response:
            self.profile_link = None
            return(self.in_directory)
        message = self.soup.find("h1")
        if message:
            message = message.text.strip()
        error = "Sorry, we can’t find the page you’re looking for."
        if message != error:
            self.in_directory = True
        else:
            self.profile_link = None
        return(self.in_directory)

    def update_name(self):
        #Get raw name from HTML
        name = self.soup.find('b')
        #Parse name into first last middle initial, full name
        if name:
            name = name.text
            self.name = name
            name_list = name.split(" ")
            if len(name_list) == 3 and name_list[1] != "": #Has first, last, and middle. Middle name is not " ". (ran into this problem in the past.)
                self.middle_initial = str(name_list[1][0])
            else:
                self.middle_initial = None
            self.first = str(name_list[0])
            self.last = str(name_list[len(name_list)-1])
        
    def update_edu(self):
        #Search HTML for credentials section
        #Append Education and Training data into a list 
        education = []
        credentials = self.soup.find(attrs = {"data-nav" : "Credentials"})
        if credentials:
            edu = credentials.find(string = re.compile("Education and Training"))
            if edu:
                edu = edu.parent.parent.find_all("li")
                for school in edu: 
                    education.append(school.string.strip())
        for school in education:
            school = re.split(" from |, ", school)
            uni = ""
            split = False
            for part in school:
                if part != school[0] and part != school[len(school) - 1]:
                    uni += (part + ", ")
                    split = True
            if split:
                uni = uni[:len(uni) - 2]
            self.education.append("Degree type: {0}\nInstitution: {1}\nYear: {2}\n".format(school[0], uni,school[len(school) - 1]))

    def update_photo(self):
        #Grab photo URL from HTML data
        photo = self.soup.find(class_ = "square doctor-image")
        #Check to see if the doctor has a "Square photo" if not, get the background image.
        if photo:
            photo = photo.img["src"]
            self.headshot = "https://nyulangone.org" + str(photo)
        else:
            photo = self.soup.find(class_="parallax")
            if photo:
                photo = str(photo["style"])
                photo = (photo[photo.find("url") + 4:len(photo)-1])
                self.headshot = photo

    def update_location(self):
        #Get locations
        locations = self.soup.find_all(class_ = "trigger location-address")
        for place in locations:
            if place.p:
                p1 = ""
                location = place.p.text.split("\n")
                for line in location:
                    line = line.strip()
                    p1 += str(line)
                    p1 += "\n"
                self.address_list.append(p1.strip() + "\n")

    def update(self):
        #update all attributes (scrape entire profile)
        #only do so if the doctor is in the directory
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
        to_write = ["NPI","Name in Cigna Portal","Provider Name in Directory","Organization", "Profile Link", "In Directory", "Headshot Link", "Education", "Locations", "Responded?"]
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
