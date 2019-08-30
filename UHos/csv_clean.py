import time
import shlex
new = open("new.csv", "w")
f = open("uhos_2.csv", "r")
for line in f:
    shlex.split(line, ",")
print("done")
f.close()
new.close()
