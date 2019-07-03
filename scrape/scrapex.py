class Doctor:
    def __init__(self, name):
        self.full_name = name
        name_list = name.split()
        if len(name_list) == 2:
            middle_initial = None
        elif len(name_list) == 3:
            middle_initial = name_list[1]
        self.first = name_list[0]
        self.last = name_list[len(name_list) - 1]
        self.in_directory = None
        self.experience = {}
        self.headshot = ""
        self.profile_link = ""
        self.address_list = []


#Sample Data
hos = open("hos.csv", "r")
cig = open("cigna.csv", "r")
cigdic = {}
hosdic = {}

def initialize_dictionary(csv_file):
    newdic = {}
    n = 0
    for line in csv_file:
        if n == 0:
            pass
        else:
            d = Doctor(line[0])
            edlis = []
            for uni in line[1]:
                edlis.append(uni)    
            d.experience["Education"] = edlis
            addlis = []
            for add in line[1]:
                addlis.append(add)
            d.address_list = addlis
            newdic[d.full_name] = d
        n = 1
    return newdic
print(initialize_dictionary(cig))

