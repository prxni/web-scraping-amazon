from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np

def get_title(soup):

    try:
        # Outer Tag Object
        title = soup.find("span", attrs={"id":'productTitle'})
        
        # Inner NavigatableString Object
        title_value = title.text

        # Title as a string value
        title_string = title_value.strip()

    except AttributeError:
        title_string = ""

    return title_string

# Function to extract Product Price
def get_price(soup):
    try:
        price_container = soup.find("div", attrs={"class": "a-section a-spacing-none aok-align-center aok-relative"})
        price_whole = price_container.find("span", attrs={"class": "a-price-whole"}).text.strip()
        return f"₹{price_whole}"  # Example: "₹10,698"
    except AttributeError:
        return ""

# Function to extract Product Rating
def get_rating(soup):

    try:
        rating = soup.find("span", attrs={'class':'a-declarative'}).find("span",attrs={'class':'a-size-base a-color-base'}).string.strip()
    
    except AttributeError:
        try:
            rating = soup.find("span", attrs={'class':'a-icon-alt'}).string.strip()
        except:
            rating = ""	

    return rating

# Function to extract Number of User Reviews
def get_review_count(soup):
    try:
        review_count = soup.find("span", attrs={'id':'acrCustomerReviewText'}).string.strip()

    except AttributeError:
        review_count = ""	

    return review_count

# Function to extract Availability Status
def get_availability(soup):

    try:
        available = soup.find("div", attrs={'id':'availability'})
        available = available.find("span").string.strip()

    except AttributeError:
        available = "Not Available"	

    return available


if __name__ == '__main__':

    mainURL="https://www.amazon.in/s?k=phones&ref=nb_sb_noss"

    HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Referer': 'https://www.google.com/',
    'DNT': '1',
    'Connection': 'keep-alive'
}

    webpage = requests.get(mainURL, headers=HEADERS)

    soup = BeautifulSoup(webpage.content, "html.parser")

    links = soup.find_all("a", attrs={'class':'a-link-normal s-line-clamp-2 s-link-style a-text-normal'})

    links_list = []
    
    for link in links:
        links_list.append(link.get('href'))

    

    d = {"title":[], "price":[], "rating":[], "reviews":[],"availability":[]}

    for link in links_list:
        new_webpage = requests.get("https://www.amazon.in" + link, headers=HEADERS)
        new_soup = BeautifulSoup(new_webpage.content, "html.parser")
        d['title'].append(get_title(new_soup))
        d['price'].append(get_price(new_soup))
        d['rating'].append(get_rating(new_soup))
        d['reviews'].append(get_review_count(new_soup))
        d['availability'].append(get_availability(new_soup))
    
    amazon_df = pd.DataFrame.from_dict(d)
    amazon_df['title'] = amazon_df['title'].replace('', np.nan) 
    amazon_df = amazon_df.dropna(subset=['title'])
    amazon_df.to_csv("output.csv", header=True, index=False)


