import argparse
import requests
from bs4 import BeautifulSoup

"""
A web scraping script that all URLs from a set of websites 
that contain one of the words in a given list/set of words.

All inputs are file-based:
Input for websites: default: domains.txt [List of Websites]
Input for terms to search: default: terms.txt [List of Terms]

Output: output.txt [List of URLs on Websites that contain one or more of Terms in Title]

@author: jerome roeser
"""


PATH_DOMAINS_LOCAL = 'domains.txt'
DEFAULT_INPUT = 'terms.txt'
DEFAULT_OUTPUT = 'output.txt'


def get_domains(file):
    """
    This function loads the entries from a file containing the listed urls
    to parse. It returns a list of the urls with the "/sitemap.xml" suffix.
    """
    with open(file, 'r') as f:
        domains = f.readlines()
    return [domain.rstrip() + '/sitemap.xml' for domain in domains]


def get_terms(file):
    """
    This function loads the entries from a file containing the terms to be 
    checked. It returns a clean list terms.
    """
    with open(file, 'r') as f:
        terms = f.readlines()
    return [term.rstrip() for term in terms]


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
    This function processes an url until an <urlset> tagged sitemap document is found. 
    Takes care of the case of multiple nested sitemap files (i.e. sitemap indexes). 
    The function returns a list of all <loc> tags in an <urlset> document that 
    can be processed or a string of the domain if it can't be analyzed for 
    any reason - such has no sitemap.xml document or a wrong domnain name due
    to typo for instance.
    """
    try:
        r = requests.get(url).content
        sitemap_content = BeautifulSoup(r, features='lxml-xml')
        parsed_data = []
        if sitemap_content.select('urlset'):
            # print('urlset...!')
            # print(f'send {url} to process_urlset')
            return process_urlset(sitemap_content)
        elif sitemap_content.select('sitemapindex'):
            sitemapindexes = process_urlset(sitemap_content)
            for i in sitemapindexes:
                parsed_data.extend(process_sitemap_content(i))
            return parsed_data
        else:
            return url.rstrip('/sitemap.xml')
    except:
        return url.rstrip('/sitemap.xml')


def main(path_domains, path_terms, path_output):
    """
    Returns a dictionnary with the terms to be searched as keys and as values a dictionnary 
    with the websites as keys and the corresponding links as values.
    An output file is created which lists for every term the links referring to  
    this term for each domain. 
    The website that cannot be scraped, i.e. if they have no sitemap.xml url 
    or there are non-existing, are listed separately as well.

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
                    links[term][domain] = [
                        loc for loc in locs if term.lower() in loc.lower()]
                    [out_file.write('\t->\t' + loc + '\n')
                     for loc in locs if term.lower() in loc.lower()]
                else:
                    failed.add(process_sitemap_content(domain))
            out_file.write('\n')
        out_file.write('List of websites that couldn\'t be scraped:\n')
        out_file.write(str(failed))
    return links, failed


if __name__ == '__main__':
    print('Scraping websites...')

    parser = argparse.ArgumentParser(description="""
             A web scraping script that gets all URLs from a set of websites 
             that contain one of the words in a given list/set of words by 
             parsing the sitemap.xml file if present.
             Takes as input i) a .txt file with a list of domains (1 per line) and
             ii) a .txt file with a list of terms (1 per line). 
             Output: an output.txt file
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

    result = main(path_domains, path_terms, path_output)
    print('\n...Done!\n')
    if len(result[1]) != 0:
        print(
            f'Unfortunately, {len(result[1])} website(s) need(s) to be analyzed manually/separately')
        print('Check the end of the output file for more details')
