import urllib2
import itertools
from os.path import isfile
from bs4 import BeautifulSoup
from time import sleep

OUTPUT_FILE = "TLA.txt"
SLEEP_INTERVAL = 3
BROWSER_USER_AGENT = "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"

def tail(f, window=20):
    """
    Returns the last `window` lines of my_file `f` as a list.
    """
    if window == 0:
        return []
    BUFSIZ = 1024
    f.seek(0, 2)
    n_bytes = f.tell()
    size = window + 1
    block = -1
    data = []
    while size > 0 and n_bytes > 0:
        if n_bytes - BUFSIZ > 0:
            # Seek back one whole BUFSIZ
            f.seek(block * BUFSIZ, 2)
            # read BUFFER
            data.insert(0, f.read(BUFSIZ))
        else:
            # my_file too small, start from begining
            f.seek(0,0)
            # only read what was not read
            data.insert(0, f.read(n_bytes))
        linesFound = data[0].count('\n')
        size -= linesFound
        n_bytes -= BUFSIZ
        block -= 1
    return ''.join(data).splitlines()[-window:]
    
def get_result_count(query):    
    site = 'http://www.google.com.br/search?q=' + str(query)
    request = urllib2.Request(site, headers={'User-Agent' : BROWSER_USER_AGENT}) 
    html_doc = urllib2.urlopen(request).read()
    soup = BeautifulSoup(html_doc, "html.parser")
    return soup.find("div", id="resultStats").contents[0].encode("utf-8").split()[1]

if isfile(OUTPUT_FILE):
    my_file = open(OUTPUT_FILE, "r")
    last_code = tail(my_file, 1)[0][:3]
    my_file.close()
else:
    last_code = ""

print(last_code)
my_file = open(OUTPUT_FILE, "a")
    
for string in itertools.imap(''.join, itertools.product('ABCDEFGHIJKLMNOPQRSTUVWXYZ', repeat=3)):
    if string <= last_code:
        continue    
    result = "{0}:{1}".format(string, get_result_count(string))
    my_file.write(result+"\n")
    my_file.flush()
    sleep(SLEEP_INTERVAL)
    print(result)

my_file.close()