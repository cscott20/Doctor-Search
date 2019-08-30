import docob
import sys
var = sys.argv
if len(var) > 1:
    head = "headless"
else:
    head = None
driver = docob.open_chrome(head)
d = docob.Doctor("1518953462", "Name", driver)
#d = docob.Doctor("151isfadfs8953462", "Name", driver)
d.check_in_dir()
d.update_location()
for addy in d.address_list:
    print(addy)

driver.close()
