# -*- coding: utf-8 -*-
"""
Created on Wed Jan  4 22:51:35 2023

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

@author: Jerome Roeser
"""

import requests
import argparse
import sys
from bs4 import BeautifulSoup

PATH_DOMAINS_LOCAL = 'domains.txt'
DEFAULT_INPUT = 'terms.txt'
DEFAULT_OUTPUT = 'output.txt'



def has_sitemap(url):
    """
    Not every website has a sitemap.xml link. This function checks whether
    a sitemap.xml link exists.
    """
    sitemap_url = url + '/sitemap.xml'
    r = requests.get(sitemap_url)
    if r.status_code == 200:
        return True
    return False

def get_domains(file):
    """
    Gets the domains from the input file and add sitemap.xml suffix.
    """
    with open(file, 'r') as f:
        domains = f.readlines()
    return ([domain.rstrip() + '/sitemap.xml' for domain in domains])
    

def get_terms(file):
    """
    Gets the domains from the input file
    """
    with open(file, 'r') as f:
        terms = f.readlines()
    return ([term.rstrip() for term in terms])
    

def is_sitemapindex(url):
    """
    Checks first if the root element is a sitemap index 
    other possibilities root_name == 'urlset' or else
    """
    r = requests.get(url).content
    soup = BeautifulSoup(r, features='lxml-xml')
    root_name = soup.find().name
    if root_name == 'sitemapindex':
        return True
    else:
        return False 


def get_soup(url):
    """
    Checks the sitemap.xml file for all url locations in case of a urlset.
    Calls process_sitemapindex function in case of sitemapindex xml.
    """
    try:
        r = requests.get(url).content
        soup = BeautifulSoup(r, features='lxml-xml')
    except:
        print(f'Invalid email address: {url}')
    return soup

def process_urlset(urlset):
    locs = urlset.find_all('loc')
    parsed_data = []
    for loc in locs:
        parsed_data.append(loc.text)
    return parsed_data
    

def process_sitemap_content(sitemap_adress):
    sitemap_content = get_soup(sitemap_adress)
    if sitemap_content.select('urlset'):
        return process_urlset(sitemap_content)
    elif sitemap_content.select('sitemapindex'):
        sitemapindexes = sitemap_content.find_all('loc')
        process_sitemapindex(sitemapindexes)
    else:
        # print(f'parsing of {sitemap_adress} should be done individually...')
        return sitemap_adress.rstrip('/sitemap.xml')
        

def process_sitemapindex(sitemapindexes):
    """
    Is call by get_loc function. Input is a sitemapindex.xml adress.
    All the locs in there are new sitemap.xml files that should be processed
    by get_locs function
    """
    for i in sitemapindexes:
        process_sitemap_content(i.text)

def main(path_domains, path_terms, path_output):
    """
    Loops through the domain list and the term list to match every terms.
    For each domain, a dictionnary of {terms:url_links} should be generated

    Returns
    -------
    A dictionnary in the form {domain_1:{term_1:[link_1, link_2]; term_2}}

    """
    domains, terms = get_domains(path_domains), get_terms(path_terms)
    with open(path_output, 'w') as out_file:
        links, failed = {}, set()
        for term in terms:
            locs = []
            links[term] = {}
            out_file.write('Links for the following term: ')
            out_file.write(term + '\n')
            for domain in domains:                
                if isinstance(process_sitemap_content(domain), list):
                    locs = process_sitemap_content(domain)
                    links[term][domain] = [loc for loc in locs if term.lower() in loc.lower()]
                    [out_file.write('\t->\t' + loc + '\n') for loc in locs if term.lower() in loc.lower()] 
                else:
                    failed.add(process_sitemap_content(domain))
            out_file.write('\n')
        out_file.write(str(failed))
    return links, failed

if __name__ == '__main__':
    result = main(PATH_DOMAINS_LOCAL, DEFAULT_INPUT, DEFAULT_OUTPUT)
    print('running...')
    
#%% test zone

# domains = get_domains(PATH_DOMAINS_LOCAL)
# terms = get_terms(DEFAULT_INPUT)
# path_domains, path_terms = PATH_DOMAINS_LOCAL, DEFAULT_INPUT
# d = {}
# matches = []

# for domain in domains:
#     d[domain.rstrip('/sitemap.xml')] = process_sitemap_content(domain)
# for term in terms:
#     for k in d.keys():
#         matches = [v[i] for v in d.values() for i in range(len(v))]

# domains, terms = get_domains(path_domains), get_terms(path_terms)
# with open(DEFAULT_OUTPUT, 'w') as out_file:
#     links = {}
#     failed = set()
#     count = 0
#     for term in terms:
#         locs = []
#         links[term] = {}
#         out_file.write('Links for the following term: ')
#         out_file.write(term + '\n')
#         for domain in domains:                
#             if isinstance(process_sitemap_content(domain), list):
#                 locs = process_sitemap_content(domain)
#                 links[term][domain] = [loc for loc in locs if term.lower() in loc.lower()]
#                 [out_file.write('\t->\t' + loc + '\n') for loc in locs if term.lower() in loc.lower()] 
#             else:
#                 failed.add(process_sitemap_content(domain))
#         out_file.write('\n')
#         out_file.write(str(failed))
        
            



        
# https://practicaldatascience.co.uk/data-science/how-to-parse-xml-sitemaps-using-python
# https://levelup.gitconnected.com/developing-a-website-scraper-b7a78bb5544a
        
        