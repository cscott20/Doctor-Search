import docob
import time
import random 

#a random delay time will be chosen from this list
delay_choice = [2,3,4,5,6,7,8] #seconds

#read_file should have NPI's in col A and provider names in col B
read_file = "cigna.csv"
write_file = "nyu.csv" 

f = open(read_file, "r")

#overwrite data in write_file, create header
docob.write_header(write_file)

count = 1 #keeps count of how many providers have been scraped
for line in f:
    #delay random choice from delay_choice
    wait = random.choice(delay_choice)
    time.sleep(wait)
    
    #Parse read_file data
    line = line.split(",")
    npi = line[0]
    name = line[1]
    
    #create doctor object, update attributes, write to csv file
    d = docob.Doctor(npi, name)
    d.update()
    d.write_csv(write_file)

    #print count of providers completed
    print(count)
    count += 1
