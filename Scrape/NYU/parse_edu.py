import re
fil = "sample_edu.txt"
f = open(fil, "r")
for line in f:
    edu = re.split(" from |, ", line)
    uni = ""
    split = False
    for part in edu:
        if part != edu[0] and part != edu[len(edu) - 1]:
            uni += (part + ", ") 
            split = True       
    if split:
        uni = uni[:len(uni) - 2] 
    print("Type: {0}\nUni: {1}\nYear: {2}\n".format(edu[0],uni,edu[len(edu)-1]))
f.close()
