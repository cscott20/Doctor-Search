import re
f = open("edu.txt", "r")
for line in f:
    line = re.split(" \| |, \(", line)
    if len(line[0].split(", ")) > 1:
        line.append(line[1])
        line[1] = line[0].split(", ")[1]
        line[0] = line[0].split(", ")[0]
    else:
        line[1] = re.split(" - ",line[1])[len(re.split(" - ",line[1]))-2]
    print(line)
f.close() 
