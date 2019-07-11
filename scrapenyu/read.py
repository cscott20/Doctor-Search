import docob
import time
cignaNPI = "cigna.csv"
f = open(cignaNPI, "r")
docob.create_csv("nyu2")
n = 0
for line in f:
    time.sleep(1)
    line = line.split(",")
    npi = line[0]
    name = line[1]
    d = docob.Doctor(npi, name)
    d.update()
    d.write_csv("nyu2")
    print(n)
    n += 1
