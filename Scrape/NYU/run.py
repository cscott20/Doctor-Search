import docob
import time
import random 
import statistics

run_limit = 2441 #Stop after recording this many doctors
                #None will scrape all doctors in the file

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

tim = []

#lines = 0 
#if (not bool(run_limit)):
#    for line in f:
#        lines += 1
#    run_limit = lines

#append each docotor object to a dictionary
for line in f:
   # print(count)
   # if count < run_limit:
        dst = time.time()
        
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

        den = time.time()
        
        tim.append( den - dst )
        
        #print count of providers completed
        count += 1
        print(count, "Doctors scraped")
        print("Estimated time remaining: ", round((statistics.mean(tim) * (run_limit - count)) / 60), " minutes")

end = time.time()

#overwrite data in write_file, create header
docob.write_header(write_file)

#write to new csv file
docob.write_csv(write_file, doclis)    

print("average response time: ", statistics.mean(response))
print("it took ", round((end - start)/60), " minutes to scrape ", count, " doctors at a rate of ", round((count*3600)/(end-start)), "doctors per hour") 
