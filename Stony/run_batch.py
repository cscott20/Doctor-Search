import docob
import time
import random 
import statistics
import sys
import datetime

var = sys.argv
if len(var) > 1:
    head = "headless"
else:
    head = None
msg = input("overwrite? y/n\n")



ov = "a"
if msg == "y":
    ov = "w" 
data = open("data_col.csv", ov)

#both start and stop will be read.
start_read = 1000  #enter previous run_limit
run_limit = None #Stop after recording this many doctors
                #None will scrape all doctors in the file

#python will sleep for multiplier * response time between requests
multiplier = 5


#read_file should have NPI's in col A and provider names in col B
read_file = "cigna.csv"
write_file = "stony.csv"

f = open(read_file, "r")

#initialize list of doctor objects.
doclis = []

#Keeps track of statistics of average response times.
response = []

#keeps count of how many providers have been scraped

start = time.time()

f2 = open("data_col.csv", "r")

tim = []
dt = f2.readlines()
for entry in dt:
    tim.append(float(entry.strip()))
f2.close()

lines = 0 

for line in f:
    lines += 1

if (not bool(run_limit)) or run_limit > lines:
    run_limit = lines

newtim = []
f.close()
f = open(read_file, "r")
count = 0 
linenum = 0
driver = docob.open_chrome(head)
#append each docotor object to a dictionary
for line in f:
    if linenum < run_limit and linenum >= start_read:
        dst = time.time()
        
        #Parse read_file data
        line = line.split(",")
        npi = line[0]
        name = line[1]
        org = line[2]
        #create doctor object, update attributes, write to dictionary
        d = docob.Doctor(npi, name, org, driver)
        d.update()
        doclis.append(d)
 
        #delay response time times multiplier 
        print("response time: ", str(d.response_time))
        response.append(d.response_time)
        time.sleep(d.response_time * multiplier)

        den = time.time()
        #print count of providers completed
        count += 1

        if count > 1:
            tim.append( den - dst )
            newtim.append( den - dst )
        
        
        print(count, "Doctors scraped")
        if count > 1:
            time_remaining = round((statistics.mean(tim) * (run_limit  - (count + start_read)) / 60))
            print("Estimated time remaining: ",  time_remaining, " minutes")
            hour_later = datetime.datetime.now().hour
            min_later = datetime.datetime.now().minute
            new_minute = min_later + time_remaining
            hour_later += new_minute // 60
            new_minute = new_minute - ((new_minute // 60) * 60)
            if new_minute < 10:
                new_minute = "0"+str(new_minute)
            if hour_later > 12:
                hour_later -= 12
            print("Expected Completion Time: ", str(hour_later) + ":"+ str(new_minute))  
        
    linenum += 1

end = time.time()

#overwrite data in write_file, create header
if msg == "y":
    docob.write_header(write_file)

#write to new csv file
docob.write_csv(write_file, doclis)    

for entry in newtim:
    data.write(str(entry))
    data.write("\n")
data.close()

print("average response time: ", statistics.mean(response))
print("it took ", round((end - start)/60), " minutes to scrape ", count, " doctors at a rate of ", round((count*3600)/(end-start)), "doctors per hour")

driver.close() 

