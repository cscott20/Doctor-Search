from docob import Doctor as doc

npi = input("NPI: ")
d = doc(npi)
d.update()
print(d)
d.create_csv("nyu")
d.write_csv("nyu")
