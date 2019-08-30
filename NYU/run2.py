import docob
import time
import random 
import statistics

only_run = None #Stop after recording this many doctors

#python will sleep for multiplier * response time between requests
multiplier = 10


#read_file should have NPI's in col A and provider names in col B
read_file = "cigna.csv"
write_file = "nyu.csv"

f = open(read_file, "r")

#initialize list of doctor objects.
doclis = []

#Keeps track of statistics of average response times.
response = []

#keeps count of how many providers have been scraped
count = 0 

start = time.time()

#append each docotor object to a dictionary
for line in f:
    if (not bool(only_run)) or count < only_run:
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
        count += 1
        print(count)

end = time.time()

#overwrite data in write_file, create header
docob.write_header(write_file)

#write to new csv file
docob.write_csv(write_file, doclis)    

print("average response time: ", statistics.mean(response))
print("it took ", round(end - start), " seconds to scrape ", count, " doctors at a rate of ", round((count*3600)/(end-start)), "doctors per hour") 
