from bs4 import BeautifulSoup
from urllib import request
import urllib.request
from urllib.request import Request
from urllib.request import urlopen
from collections import deque
import collections
import requests
import sys
from re import compile
import re
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords


# STEP 1
# web crawler function
def web_crawler(url):
    r = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    resp = urlopen(r)
    soup = BeautifulSoup(resp, features="html.parser")

    url_list = []
    # set count of articles to 0
    count = 0
    # write urls to a file
    with open('urls.txt', 'w') as f:
        for link in soup.findAll('a'):
            link_str = str(link.get('href'))
            if link_str.startswith('http'):
                url_list.append(link_str)

                f.write(link_str + '\n')
                count += 1
                if count > 20:
                    break
    f.close()

    # new list for function output
    new_list = []
    # open urls from first
    with open('urls.txt', 'r') as f:
        links = f.read().splitlines()
        for u in links:
            # create queue for urls and append to wait_list
            wait_list = collections.deque()
            wait_list.append(u)
        # reverse the list (first url in url.txt is useless)
        wait_list.reverse()
        # pop a url to crawl for relevant url
        pop = wait_list.pop()
        req = request.urlopen(pop).read()
        soup1 = BeautifulSoup(req, "html.parser")
        articles = 0
        for link in soup1.findAll('a'):
            link_str = str(link.get('href'))
            # print(link_str)
            new_list.append(link_str)
            if link_str.startswith('http') and 'Stocks' in link_str:
                articles += 1
                if articles > 40:
                    break
        new_list = list(reversed(new_list))

        # add 5 urls from url popped to url_list
        url_list.append(new_list[:5])
    return url_list[2:]


# STEP 2: Write a function to loop through your URLs and scrape all text off each page.
# Store each page’s text in its own file.
def scrape_text(scraped_urls):
    output = ''
    # name the url textfiles different number starting from 1-19
    count = 0
    for i in scraped_urls:
        count += 1
        with open(str(count) + '.txt', 'w') as file:
            # list of elements we need to begin preprocessing
            need = ['style', 'script', '[document]', 'head', 'title']
            html = urllib.request.urlopen(i)
            soup = BeautifulSoup(html, features="html.parser")
            text = soup.find_all(text=True)

            # loop through urls and extract elements we need
            for single_url in text:
                if single_url.parent.name not in need:
                    output += '{} '.format(single_url)
                    file.write(output)


# STEP 3:
# Clean up text, delete newlines/tabs.
# Extract sentences with sent_tokenize
def process_data(raw_text):
    out = 20
    with open(str(out) + '.txt', 'w') as f:
        out += 1
        # replace newlines / tabs with ''
        raw_text = raw_text.replace("\n", "")
        raw_text = raw_text.replace("\t", "")
        # lowercase all text
        # remove numbers and punctuation, replace with ' ' using regex
        raw_text = re.sub(r'[.?!,:;$#"@()=+%&\-\'\n\d]', ' ', raw_text.lower())

        # remove stopwords
        stop_words = set(stopwords.words('english'))

        # reduce tokens to tokens that are alpha, not stopwords
        raw_text = [t for t in raw_text if t not in stop_words]

    return raw_text


if __name__ == '__main__':
    # Get original links from finviz.com
    url = 'https://finviz.com/quote.ashx?t=spy'
    # output 20 relevant links - professor on piazza said more links the better so I added a couple more
    scraped_urls = web_crawler(url)

    # scrape 19 urls and create textfiles w text outputs(20 urls caused error)
    scrape_text(scraped_urls[:19])


    # takes a while to output all the files
    out = 20
    input_files = ['1.txt', '2.txt', '3.txt', '4.txt', '5.txt', '6.txt', '7.txt', '8.txt', '9.txt', '10.txt']
    for input in input_files:
        with open(input, 'r') as file, open(str(out) + '.txt', 'w') as f:
            out += 1
            raw_text = file.read()
            # process text from each url
            process_data(raw_text)

            # tokenize sentences
            sentences = sent_tokenize(raw_text)

            # print to a new files
            for sent in sentences:
                f.write(sent)
