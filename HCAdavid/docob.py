from bs4 import BeautifulSoup
import re
import requests
import csv
import time


class Doctor:
    def __init__(self, npi, cigna_name):
        #Initialize attributes
        root = "https://stdavids.com/physicians/detail.dot?npi="
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
        doc = "Not in Directory"
        if self.in_directory:
            doc = "Name: {0}\nNPI: {1}\nProfile Link: {2}\nHeadshot Link: {3}\nEducation Records: {4}\nAddresses: {5}".format(self.name, self.npi, self.profile_link, self.headshot, self.education, self.address_list)
        return(doc)
    
    def check_in_dir(self):
        #checks if in directory. Grabs name at same time if in directory. Stores in self.name
        message = self.soup.find("h1").text.strip()
        error = "Looks as though we were unable to lookup that provider. "
        if message != error:
            self.in_directory = True
        else:
            self.profile_link = None
        return(self.in_directory)

    def update_name(self):
        name = self.soup.find("h1").text.strip()
        #Parse name into first last middle initial, full name. Gets rid of ", MD"
        if name:
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
        credentials = self.soup.find(class_="UH-Feature-Doctors-DoctorInformation-Education container-fluid")
        if credentials:
            edu = credentials.find_all("p")
            for ed in edu:
                st = ""
                lis = ed.text.split("                            ") #This directory has huge space gaps. 
                for element in lis:
                    st += element.strip()
                    st += "!!!"
                st = re.split(" \| |!!!\(", st)
                if len(st[0].split("!!!")) > 1:
                    st.append(st[1])
                    st[1] = st[0].split("!!!")[1]
                    st[0] = st[0].split("!!!")[0]
                else:
                    st[1] = re.split(" - ",st[1])[len(re.split(" - ",st[1]))-1]
                st[2] = st[2][:len(st[2])-4]
                self.education.append("Degree type: {0}\nInstitution: {1}\nYear: {2}\n".format(st[0],st[1],st[2]))

    def update_photo(self):
        #Grab photo URL from HTML data
        photo = self.soup.find(class_ = "UH-Feature-Doctors-DoctorInformation-Header-Photo")
        if photo:
            self.headshot = photo["src"]

    def update_location(self):
        #Get locations
        locations = self.soup.find_all(class_ = "UH-Feature-Doctors-DoctorInformation-Location")
        for place in locations:
            if place.p:
                #print(place.p.text)
                p1 = ""
                location = place.p.text.split("\n")
                for line in location:
                    line = line.strip()
                    p1 += str(line)
                    p1 += "\n"
                # Get rid of phone number
                p1 = p1.split("\n\n")
                p1 = p1[:len(p1)-1]
                p1 = p1[0]
                #add to address_list
                self.address_list.append(p1.strip() + "\n")

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
        to_write = ["NPI","Name in Cigna Portal","Provider Name in Directory", "Profile Link", "In Directory", "Headshot Link", "Education", "Locations", "Responded?"]
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
                to_write = [doctor.npi, doctor.cigna_name, doctor.name, doctor.profile_link, 
                            doctor.in_directory, doctor.headshot, edu.strip(), addy.strip(), 
                            doctor.response]
                fil.writerow(to_write)
            csvfile.close()

