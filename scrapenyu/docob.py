from bs4 import BeautifulSoup
import re
import requests


class Doctor:
    def __init__(self, npi):
        self.npi = npi
        self.name = None
        self.middle_initial = None
        self.first = None
        self.last = None
        self.in_directory = False
        self.education = []
        self.headshot = None
        self.profile_link = "https://nyulangone.org/doctors/{0}".format(self.npi)
        self.address_list = []
        res = requests.get(self.profile_link).text
        self.soup = BeautifulSoup(res, 'lxml') 
        
    def __repr__(self):
        doc = "Not in Directory"
        if self.in_directory:
            doc = "Name: {0}\nNPI: {1}\nProfile Link: {2}\nHeadshot Link: {3}\nEducation Records: {4}\nAddresses: {5}".format(self.name, self.npi, self.profile_link, self.headshot, self.education, self.address_list)
        return(doc)
    
    def check_in_dir(self):
        message = self.soup.find("h1").text.strip()
        error = "Sorry, we can’t find the page you’re looking for."
        if message != error:
            self.in_directory = True
        return(self.in_directory)

    def update_name(self):
        #Get raw name from HTML
        name = self.soup.find('b')
        #Parse name into first last middle initial, full name
        if name:
            name = name.text
            self.name = name
            name_list = name.split()
            if len(name_list) == 3:
                name_string = str(name[0]) + " " + str(name[2]) #First and Last name only, not middle.
                self.middle_initial = str(name[1][0])
            else:
                name_string = str(name_list[0]) + " " + str(name_list[1]) 
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
        photo = self.soup.find(class_="parallax")
        if photo:
            photo = str(photo["style"])
            photo = (photo[photo.find("url") + 4:len(photo)-1])
            self.headshot = photo

    def update_location(self):
        #Get locations
        locations = self.soup.find_all(class_ = "trigger location-address")
        for place in locations:
            p1 = ""
            location = place.p.text.split("\n")
            for line in location:
                line = line.strip()
                line = line.strip()
                p1 += str(line)
                p1 += "\n"
            self.address_list.append(p1.strip())

    def update(self):
        self.check_in_dir()
        self.update_name()
        self.update_edu()
        self.update_photo()
        self.update_location()

    def write_csv_line(self, f):
        #write a single line to the csv flile
        pass
