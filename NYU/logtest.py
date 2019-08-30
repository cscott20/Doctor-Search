import time
f = open("testprint.txt", "w")
time.sleep(30)
print("hello")
f.write("hello! Complete")
f.close()
