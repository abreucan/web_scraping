import requests
from bs4 import BeautifulSoup
import pprint

# variables for page 1
resource = requests.get('https://news.ycombinator.com/news')
soup = BeautifulSoup(resource.text, 'html.parser')
# variables for page 2
resource_more = requests.get('https://news.ycombinator.com/news?p=2')
soup2 = BeautifulSoup(resource_more.text, 'html.parser')


links = soup.select('.titleline > a')
subtext = soup.select('.subtext')
links_more = soup.select('.titleline > a')
subtext_more = soup.select('.subtext')

all_links = links + links_more
all_subtext = subtext + subtext_more


def sort_stories_by_votes(hnlist):
    return sorted(hnlist, key=lambda k: k['votes'], reverse=True)


def create_custom_hn(links, subtext):
    hn = []
    for idx, item in enumerate(links):
        title = item.getText()
        href = item.get('href', None)
        vote = subtext[idx].select('.score')
        if len(vote):
            points = int(vote[0].getText().replace(' points', ''))
            if points > 99:
                hn.append({'title': title, 'link': href, 'votes': points})
    return sort_stories_by_votes(hn)


pprint.pprint(create_custom_hn(all_links, all_subtext))
