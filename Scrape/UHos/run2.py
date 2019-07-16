import docob
import time
import random 
import statistics

#python will sleep for multiplier * response time between requests
multiplier = 10

#read_file should have NPI's in col A and provider names in col B
read_file = "cigtest.csv"
write_file = "uhos.csv"

f = open(read_file, "r")


#initialize dictionary
doclis = []
response = []

count = 1 #keeps count of how many providers have been scraped

#append each docotor object to a dictionary
for line in f:
    #Parse read_file data
    line = line.split(",")
    npi = line[0]
    name = line[1]
    
    #create doctor object, update attributes, write to dictionary
    d = docob.Doctor(npi, name)
    d.update()
    doclis.append(d)
 
    #delay response time times multiplier 
    print("response time: ", str(d.response_time))
    response.append(d.response_time)
    time.sleep(d.response_time * multiplier)

    #print count of providers completed
    print(count)
    count += 1

#overwrite data in write_file, create header
docob.write_header(write_file)

#write to new csv file
docob.write_csv(write_file, doclis)    

print("average response time: ", statistics.mean(response))
