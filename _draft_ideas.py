# -*- coding: utf-8 -*-
"""
Created on Thu Nov 17 10:16:06 2022
My idea was a web scraping script that gets all URLs from a set of websites 
that contain one of the words in a given list/set of words.

Input: [List of Websites], [List of Terms]
Output: [List of URLs on Websites that contain one or more of Terms in Title]

Our standard rate is $30 per gig. 
This one should be relatively simple when using the sitemap.xml (for example).

Hey Jerome, I have no specific requirements. 
Yeah, it should be realistic if possible. 
For example, it would be great if I could put in a list of domains 
(e.g., as a file in the format: "example1.com, example2.com, example3.com, ...") 
and a list of terms (e.g., as a file in the format: "term1, term2, term3, ...") 
and it yields a list of URLs from the specific domains that contain 
one or more of the terms in the title:



https://example1.com/some-url-1, My Headline with term1 or term2
https://example2.com/some-url-2, Another Headline with term3
...



I think all input and output could be be file-based, 
so you have a Python project with a code.py file 
and an domains.txt file with the first input file, 
a terms.txt file with the second input file, 
and a output.txt file with the outputs.

@author: jerome.roeser1
"""

import requests
import argparse
import sys
from bs4 import BeautifulSoup

PATH_DOMAINS_LOCAL = 'domains.txt'
DEFAULT_INPUT = 'terms.txt'
DEFAULT_OUTPUT = 'output.txt'

# input_list = []
# term_list = ['Rugby', 'Golf', 'Handball']
output_list = []

url = 'https://lequipe.fr/sitemap.xml'

def main_check():
    domains = get_urls(path_domains)
    for domain in domains: 
        domain += '/sitemap.xml'
        try:
            r = requests.get(url).content
        except:
            print(f"{domain} hasn't a sitemap.xml link")
            continue
        soup = BeautifulSoup(r, features='lxml-xml')
        locs = soup.find_all('loc')
        for loc in locs:
            term_list = get_terms(path_terms)
            for term in term_list:
                output_list.append([loc[i].text for i in range(
                    len(loc)) if term.lower() in loc[i].text.lower()])
    return {domain:output_list}
            
    
# %%get url


def get_urls(file):
    with open(file, 'r') as f:
        input_list = f.readlines()
    return input_list


# %%
def get_terms(file):
    with open(file, 'r') as f:
        term_list = f.readlines()
    return term_list

# %% main


def scrape_sitemap():
    for term in term_list:
        output_list.append([loc[i].text for i in range(
            len(loc)) if term.lower() in loc[i].text.lower()])
        print([loc[i].text for i in range(len(loc))
              if term.lower() in loc[i].text.lower()])


# %% try if sitemap.xml

def has_sitemap(url):
    sitemap_url = url + '/sitemap.xml'
    r = requests.get(sitemap_url)
    if r.status_code == 200:
        return True
    return False

url = 'http://www.example.com'
if has_sitemap(url):
    print('The website has a sitemap.xml file!')
else:
    print('The website does not have a sitemap.xml file.')

url = "https://www.lequipe.fr/sitemap.xml"

response = requests.get(url)

if response.status_code == 200:
    print("The website has a sitemap.xml file")
else:
    print("The website does not have a sitemap.xml file")

# %% main
if __name__ == '__main__':
    print('Scraping websites...')

    parser = argparse.ArgumentParser(description="""
                                     A web scraping script that gets all URLs from a set of websites 
                                     that contain one of the words in a given list/set of words 
                                     """
                                     )
    parser.add_argument('-d', type=str, nargs='?',
                        help='Path of input file with the domains list.')
    parser.add_argument('-t', type=str, nargs='?',
                        help='Path of input file with the terms list.')
    parser.add_argument('-o', type=str, nargs='?',
                        help='Path where the output will be put.')

    args = parser.parse_args()

    path_domains = args.d if args.d else PATH_DOMAINS_LOCAL
    path_terms = args.t if args.t else DEFAULT_INPUT
    path_output = args.o if args.o else DEFAULT_OUTPUT

    try:
        mails_count = scrape_sitemap(path_domains, path_terms, path_output)
        print(f'Copied {mails_count} email addresses to the output file.')
        print('Done.')
    except:
        print(f'Sorry, an unexpected error ({sys.exc_info()[1]}) occurred!\nCall filtermails.py -h for help.')
