from bs4 import BeautifulSoup
import requests
import sys
from urllib.parse import urlparse, urljoin

printdebug = False

def canHaveAdditionalLinks(url):
    if '.' not in url:
        return True
    extensions=['.jpg', 'jpeg', '.png', 'gif', '.mp4', '.mp3', '.pdf', '.doc', 'docx', '.xls', 'xlsx', '.zip', '.tar.gz']
    for ext in extensions:
        if url.endswith(ext):
            return False
    return True

def ignoreURLString(url, allowHTTPPrefix = False):
    if url == '':
        return True
    if not allowHTTPPrefix:
        if url.startswith('http'):
            return True
    prefixes=['#', '?', '//', 'tel:', 'mailto:', 'document.', 'javascript:']
    for pre in prefixes:
        if url.startswith(pre):
            return True
    return False

def getLinksFromURL(url, includeEmbedded):
    if printdebug:
        print('url -', url)
    links = set()
    # jump out if this is a URL we don't want to try to parse
    if ignoreURLString(url, True) or not canHaveAdditionalLinks(url):
        return links
    response = ''
    try:
        response = requests.get(url)
    except:
        sys.stderr.write('***** ERROR retrieving url, returning empty set of links - URL = {}\n'.format(url))
        sys.stderr.flush()
        return links

    try:
        contentType = response.headers['content-type']
        if contentType and 'text/html' not in contentType:
            return links  # we are done because not parsable HTML
        soup = BeautifulSoup(response.content, 'html.parser')
    except Exception as e:
        sys.stderr.write('***** ERROR parsing HTML, returning empty set of links - URL = {}, Exception={}\n'.format(url, e))
        sys.stderr.flush()
        return links

    for link in soup.find_all('a', href=True):
        text = link['href'].strip()
        if ignoreURLString(text):
            continue
        # deal with relative URLs
        if text.startswith('..'):
            joinedurl = urljoin(url, text)
            parsedurl = urlparse(joinedurl)
            path = parsedurl.path
            if path.startswith('/..'):
                while path.startswith('/..'):
                    path = path[3:]
            else:
                if printdebug:
                    print('1 - ' + path)
                links.add(path)
        else:
            # exclude endless dotcms starter event calendar
            if '/?date=' not in text:
                if printdebug:
                    print('2 - ' + text)
                links.add(text)

    onclicks = soup.find_all(attrs={"onclick": True})
    for onclick in onclicks:
        text = onclick['onclick'].strip()
        if 'href=' in text:
            text = text[text.find('href=') + 5:].strip().split('\'')[1]
            if ignoreURLString(text):
                continue

        if text.startswith('..'):
            joinedurl = urljoin(url, text)
            parsedurl = urlparse(joinedurl)
            path = parsedurl.path
            if path.startswith('/..'):
                while path.startswith('/..'):
                    path = path[3:]
            else:
                if printdebug:
                    print('3 - ' + path)
                links.add(path)
        else:
            if printdebug:
                print('4 - ' + text)
            if not ignoreURLString(text):
                links.add(text)
    if includeEmbedded:
        # process script tags
        for link in soup.findAll('script', src=True):
            # skip useless links
            if ignoreURLString(link['src']):
                continue
            if printdebug:
                print('5 - ' + link['src'])
            links.add(link['src'])

        # process img tags
        for link in soup.findAll('img', src=True):
            #print('link:', link)
            # skip useless links
            if ignoreURLString(link['src']):
                continue
            if printdebug:
                print('6 - ' + link['src'])
            links.add(link['src'])

        # process link tags
        for link in soup.findAll('link', href=True):
            # skip useless links
            if ignoreURLString(link['href']):
                continue
            if printdebug:
                print('7 - ' + link['href'])
            links.add(link['href'])

    return links


def printFunctionCall(counter, link):
    print('\r\n    @task(1)')
    print('    def func_{}(self):'.format(counter))
    print('        self.client.get("{}")'.format(link))


def printLocustRequestFile(links):
    header = '''
from locust import HttpLocust, TaskSet, task
from bs4 import BeautifulSoup

class MyTaskSet(TaskSet):
    '''
    footer = '''

class MyLocust(HttpLocust):
    task_set = MyTaskSet
    min_wait = 500
    max_wait = 1000
    '''
    counter = 0
    print(header)
    for link in links:
        counter = counter + 1
        printFunctionCall(counter, link)
    print(footer)
