from bs4 import BeautifulSoup as bs
import re

html = open("/home/auri/temp/lucca/python_experiments/binarySearchTree1/DYNAMOSA-MIO-MOSA-WHOLE_SUITE/mutpy/mutants/7.html")

soup = bs(html, 'html.parser')
survided = soup.findAll(attrs={'class':'label label-danger'})
operator = soup.body.findAll(string=lambda t: " line " in t.text)
mutant = soup.findAll("pre")
print(survided[0].text)
print(operator[0].text)
print(mutant[0].text)


