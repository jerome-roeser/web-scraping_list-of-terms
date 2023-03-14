# -*- coding: utf-8 -*-
"""
Created on Sun Jan 15 10:40:41 2023

@author: Jerome Roeser
"""

import requests
from bs4 import BeautifulSoup

url = 'https://new.siemens.com/sitemap.xml'
url2 = 'https://siemens.com/sitemap.xml'

def process_urlset(urlset):
    """
    This function processes <loc> tags of an <urlset> tagged xml sitemap document.
    It returns all "locs" in a list. 
    """
    locs = urlset.find_all('loc')
    parsed_data = []
    for loc in locs:
        parsed_data.append(loc.text)
    return parsed_data

def process_sitemap_content(url):
    """
    This function together with the process_sitemapindex function process an url 
    until an <urlset> tagged sitemap document is found. Takes care of the case 
    multiple nested sitemap files (i.e. sitemap indexes). 
    The function returns a list of all <loc> tags in an <urlset> document that 
    can be processed or a string of the domain if it can't be analyzed for 
    any reason - such has no sitemap.xml document or a wrong domnain name due
    to typo for instance.
    """
    # parsed_data = []
    try:
        r = requests.get(url).content
        sitemap_content = BeautifulSoup(r, features='lxml-xml')
        if sitemap_content.select('urlset'):
            return process_urlset(sitemap_content)
        elif sitemap_content.select('sitemapindex'):
            parsed_data = []
            sitemapindexes = process_urlset(sitemap_content)
            for i in sitemapindexes:
                parsed_data.extend(process_sitemap_content(i))
            return parsed_data
        else:
            return url.rstrip('/sitemap.xml')
    except:
        return url.rstrip('/sitemap.xml')


# def process_sitemapindex(sitemapindexes):
#     """
#     Recursive function to allow to process different levels of sitemap indexes.
#     """
#     for i in sitemapindexes:
#         process_sitemap_content(i.text)