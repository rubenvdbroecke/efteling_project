from bs4 import BeautifulSoup
import urllib2
import datetime
from dateutil import parser

names_attr = [u'JorisendeDraak', u'Baron1898',
              u'Droomvlucht', u'DeVliegendeHollander', u'Pirana', u'Python',
              u'CarnavalFestival', u'Stoomcarrousel', u'FataMorgana', u'Kleuterhof',
              u'VogelRok', u'VillaVolta', u'Bobbaan', u'HalveMaen', u'OudeTuffer',
              u'PandaDroom', u'MonsieurCannibale', u'Pagode', u'Kinderspoor',
              u'Gondoletta', u'KinderAvonturendoolhof', u'PolkaMarina', u'Spookslot',
              u'Diorama', u'Stoomtrein(Ruigrijk)', u'Stoomtrein(Marerijk)']

storingen = []
names_attr = ['1']
for i in xrangenames_attr:
    print i
    attr_name = i.lower().replace('(', '').replace(')', '')
    a_url = 'http://eftelstats.nl/attraction.php?Id={0}'.format(attr_name)
    a_url = 'http://eftelstats.nl/dayreport.php?history=11'
    print a_url
    u = urllib2.urlopen(a_url).read()
    soup = BeautifulSoup(u, 'html.parser')

    table = soup.find("table", attrs={"class": "table table-striped"})

    # The first tr contains the field names.
    headings = [th.get_text() for th in table.find("tr").find_all("th")]

    datasets = []
    for row in table.find_all("tr")[1:]:
        dataset = zip(headings, (td.get_text() for td in row.find_all("td")))
        datasets.append(dataset)

    for a, b, c in datasets:
        attr_name = a[1]
        start_storing = parser.parse(b[1]).time()
        start_storing = datetime.timedelta(hours=start_storing.hour, minutes=start_storing.minute)
        eind_storing = parser.parse(c[1]).time()
        eind_storing = datetime.timedelta(hours=eind_storing.hour, minutes=eind_storing.minute)
        difference = (eind_storing - start_storing).seconds / 60
        print difference
        storingen.append({'name': attr_name,
                          'start_storing': start_storing,
                          'stop_storing': eind_storing,
                          'time_diff': difference})


        # print soup
        # u = str(soup.get_text).rstrip().replace(' ', '')
        # stor = u.find('<h2>Storingen</h2>')
        # stor_a = u[stor + 170:].find('</td>')
        # storing_aantal = u[(stor + 170):(stor + 170 + stor_a)]
        # stor_b = u[(stor + 170 + stor_a + 9):].find('</td>')
        # storing_minuten = u[(stor + 170 + stor_a + 9): (stor + 170 + stor_a + 9 + stor_b)].replace('minuten', '')
        # storing_aantallen.append(storing_aantal)
        # # if not storing_aantal: storing_aantal = 0
        # # if not storing_minuten: storing_miuten = 0
        # date = datetime.date.today()
        # print date
