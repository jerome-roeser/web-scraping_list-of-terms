# -*- coding: utf-8 -*-
"""
ChatGPT suggestion

@author: jerome.roeser1
"""

import requests
from bs4 import BeautifulSoup

# Set of websites to scrape
websites = ['https://www.example1.com', 'https://www.example2.com']

# List of words to search for
words = ['apple', 'banana', 'orange']

# Iterate through each website
for website in websites:
    # Send a GET request to the website
    response = requests.get(website)

    # Parse the HTML content of the website
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all links on the website
    links = soup.find_all('a')

    # Iterate through each link
    for link in links:
        # Check if the link contains any of the words in the list
        for word in words:
            if word in link.text:
                # Print the URL of the link
                print(link['href'])
