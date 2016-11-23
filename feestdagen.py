from bs4 import BeautifulSoup
import urllib2
import dateparser
import csv

feestdagen = []

# Feestdagen Belgie
for i in xrange(2016, 2018):
    feestdag_url = 'http://www.feestdagen-belgie.be/feestdagen-{0}-belgie'.format(i)
    html = urllib2.urlopen(url=feestdag_url).read()

    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find("div", attrs={"class": "class-mjd-agenda-generator class-mjd-agenda-lijst-feestdagen"})

    # The first tr contains the field names.
    headings = [th.get_text() for th in table.find("tr").find_all("th")]

    datasets = []
    for row in table.find_all("tr")[1:]:
        dataset = zip(headings, (td.get_text() for td in row.find_all("td")))
        datasets.append(dataset)

    for k, v in datasets:
        feestdagen.append(dateparser.parse(v[1]).date())

# Feestdagen Nederland
for i in xrange(2016, 2018):
    feestdag_url = 'http://www.feestdagen-nederland.nl/feestdagen-{0}.html'.format(i)
    html = urllib2.urlopen(url=feestdag_url).read()
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find("table", attrs={"id": "feestdagen_schema"})

    # The first tr contains the field names.
    headings = [th.get_text() for th in table.find("tr").find_all("th")]

    datasets = []
    for row in table.find_all("tr")[1:]:
        dataset = zip(headings, (td.get_text() for td in row.find_all("td")))
        datasets.append(dataset)

    for a, b, c, d, e in datasets:
        feestdagen.append(dateparser.parse(b[1]).date())

# Write away
with open('C:\\Users\\vande\\Dropbox\\Project Management\\Feestdagen.csv', 'wb') as myfile:
    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    wr.writerow(feestdagen)