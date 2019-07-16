class Doctor:
    def __init__(self, name):
        name_list = name.split()
        if len(name_list) == 3:
            name_string = str(name[0]) + " " + str(name[2]) #First and Last name only, not middle.
            self.middle_initial = str(name[1][0])
        else:
            name_string = str(name_list[0]) + " " + str(name_list[1]) 
            self.middle_initial = None
        self.name = name_string
        self.in_directory = None
        self.experience = {}
        self.headshot = ""
        self.profile_link = ""
        self.address_list = []


#Sample Data
Cigna_Names = ["Charlie Scott", "Erik Yan", "John Doe"]
Hospital_Names = ["Mary Lastname", "Charlie Scott", "Erik Yan", "Random A Doctor"]

Scraped_Data = {"Erik Yan": 

Cigna_Directory = {}

for name in Cigna_Names:
    doc = Doctor(name)
    Cigna_Directory[name] = doc
    doc.in_directory = bool(doc.name in Hospital_Names)
    if doc.in_directory:
        doc.profile_link = 
