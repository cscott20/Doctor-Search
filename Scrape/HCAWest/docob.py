from bs4 import BeautifulSoup
import re
import requests
import csv

class Doctor:
    def __init__(self, npi, cigna_name):
        #Initialize attributes
        self.npi = npi
        self.cigna_name = cigna_name
        self.name = None
        self.middle_initial = None
        self.first = None
        self.last = None
        self.in_directory = False
        self.education = []
        self.headshot = None
        self.profile_link = "https://hcahoustonhealthcare.com/physicians/detail.dot?npi=" + str(self.npi)
        self.address_list = []
        #Get "soup" HTML Doc
        res = requests.get(self.profile_link).text
        self.soup = BeautifulSoup(res, 'lxml') 
        
    def __repr__(self):
        doc = "Not in Directory"
        if self.in_directory:
            doc = "Name: {0}\nNPI: {1}\nProfile Link: {2}\nHeadshot Link: {3}\nEducation Records: {4}\nAddresses: {5}".format(self.name, self.npi, self.profile_link, self.headshot, self.education, self.address_list)
        return(doc)
    
    def check_in_dir(self):
        message = self.soup.find(class_ = "error-message-text").text.strip()
        error = "Looks as though we were unable to lookup that provider."
        if message != error:
            self.in_directory = True
        else:
            self.profile_link = None
        return(self.in_directory)

    def update_name(self):
        #Get raw name from HTML
        name = self.soup.find('h1')
        #Parse name into first last middle initial, full name
        if name:
            name = name.text
            self.name = name
            name_list = name.split(" ")
            if len(name_list) == 3: #Has first, last, and middle.
                self.middle_initial = str(name_list[1][0])
            else:
                self.middle_initial = None
            self.first = str(name_list[0])
            self.last = str(name_list[len(name_list)-1])
        
    def update_edu(self):
        #Search HTML for credentials section
        #Append Education and Training data into a list
        credentials = self.soup.find(attrs = {"data-nav" : "Credentials"})
        if credentials:
            edu = credentials.find(string = re.compile("Education and Training"))
            if edu:
                edu = edu.parent.parent.find_all("li")
                for school in edu: 
                    self.education.append(school.string.strip())

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
        self.check_in_dir()
        self.update_name()
        self.update_edu()
        self.update_photo()
        self.update_location()


    def write_csv(self, f):
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
        csvfile.close()

def write_header(f):
        #Creates and writes a header to file f
        #overwrites data in file f
        fil = open(f, "w")
        to_write = ["NPI","Name in Portal","Provider Name", "Profile Link", "In Directory", "Headshot Link", "Education", "Locations"]
        with open(f, 'w') as csvfile:
            fil = csv.writer(csvfile)
            fil.writerow(to_write)
        csvfile.close()
