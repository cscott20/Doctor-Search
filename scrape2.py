import requests
from bs4 import BeautifulSoup
url = "https://www.adventisthealth.org/doctors/search-results/?PhysicianName=&Keyword=&Distance=500&ZipCodeSearch=&Specialty=&Languages=&Insurances=&Affiliations=&Gender=&HasPhoto=&PhysicianNameSearch=&KeywordNameSearch=&FFD6=1561428383314"
res = (requests.get(url)).text
soup = BeautifulSoup(res, 'html.parser')
name_boxes = soup.find_all('span', attrs = {'class': 'title-font'})
for name_box in name_boxes:
    print(name_box.contents[0])
