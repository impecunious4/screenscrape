import requests
from bs4 import BeautifulSoup
import datetime
import calendar
import re # regular expressions library
import os

def scrape(site):
    now = datetime.datetime.now()
    path = os.path.dirname(os.path.realpath(__file__))

    # Get uninteresting link text from exclusion file
    with open(path+'/'+site+'.exclude.txt', 'r') as f:
        content = f.readlines()
    f.close()

    content = [x.strip() for x in content]
    content = [x.decode('utf-8') for x in content]
    content = [x.lower() for x in content]
    ignorable = set(content)

    # Add last 10 days to the ignorable set, e.g. 'Monday, October 16'
    sd = datetime.datetime.now()
    for i in range(0,10):
        ignorable.add(sd.strftime("%A, %B %d").decode('utf-8').lower())
        sd = sd - datetime.timedelta(days=1)

    # Retrieve and scrape webpage
    result = requests.get('http://www.'+site)
    c = result.content
    soup = BeautifulSoup(c, "html.parser")

    p = re.compile('([0-9.KM]+Tweet|[0-9.KM]+Share)|^[0-9]+$') # define regular expressions to exclude
    link_text = set() # initialize empty set of headlines gleaned from the text portion of links

    for link in soup.find_all('a', href=True):
        lt = (link.text).strip()
        lt = lt.replace('\n', ' ')
        lt = lt.replace('\t', ' ')
        # if the link text is not empty, isn't a Tweet counter, and is not in ignorable set, then add it
        if ((0 != len(lt)) and  (None == p.match(lt)) and ignorable.isdisjoint(set([lt.lower()]))):
            link_text.add(lt)

    mylist = sorted(link_text)
    # for item in mylist:
    #     print(item)

    fileid = path+'/output/'+site+'_'+str(now.year)+str(now.month)+str(now.day)+'_'+str(now.hour)+str(now.minute)+'.txt'
    with open(fileid, 'w') as f:
        for item in mylist:
            f.write(item.encode('utf-8')+'\n')
    f.close()

    print(fileid)


# scrape('infowars.com')
# scrape('drudgereport.com')
# scrape('thegatewaypundit.com')
# scrape('thedailycaller.com')
# scrape('breitbart.com')
# scrape('slate.com')
# scrape('politico.com')
# scrape('huffingtonpost.com')
# scrape('motherjones.com')
scrape('realclearpolitics.com')

# sd = datetime.datetime.now()
#
# for i in range(0,10):
#     print(sd.strftime("%A, %B %d"))
#     sd = sd - datetime.timedelta(days=1)

