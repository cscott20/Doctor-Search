import docob
import time
import random 


#python will sleep for multiplier * response time between requests
multiplier = 10

#read_file should have NPI's in col A and provider names in col B
read_file = "cigna.csv"
write_file = "nyu.csv"

f = open(read_file, "r")

#overwrite data in write_file, create header
docob.write_header(write_file)

count = 1 #keeps count of how many providers have been scraped
for line in f:
    #Parse read_file data
    line = line.split(",")
    npi = line[0]
    name = line[1]
    
    #create doctor object, update attributes, write to csv file
    d = docob.Doctor(npi, name)
    d.update()
    d.write_csv(write_file)
   
    #delay response time times multiplier 
    time.sleep(d.response_time * multiplier)

    #print count of providers completed
    print(count)
    count += 1
