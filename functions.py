#this file is used to store the functions used in Dubizle Datascraping and data sorting 
#----------------------------------------
#library Updates
import datetime
import pandas as pd
import os
import numpy as np
from bs4 import BeautifulSoup
from selenium import webdriver
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


#----------------------------------------
#GlobalVariables

# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
#----------------------------------------
#Here is an example of a Python function that takes a URL, uses BeautifulSoup to web scrape the page, and returns the BeautifulSoup object:

def scrape_page_chrome(url):
    # Send a request to the website
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(url)
    content = driver.page_source
    soup = BeautifulSoup(content)
    return soup


def scrape_page(url):
    # Send a request to the website
    response = requests.get(url)
    # Parse the HTML content of the page
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup



#url = "https://www.example.com"
#soup = scrape_page(url)

#----------------------------------------
#an example of a Python function that takes a BeautifulSoup soup object and shows 3 examples of the text content of every class

def show_class_examples(soup):
    class_list = get_all_classes(soup)
    for class_name in class_list:
        elements = soup.find_all(class_=class_name)
        print(f'Examples of class {class_name}')
        for i, element in enumerate(elements):
            if i<3:
                print(element.get_text())
            else:
                break

#soup = BeautifulSoup(html_string, 'html.parser')
#show_class_examples(soup)

#----------------------------------------
#example of a Python function that takes a BeautifulSoup soup object and returns a list of all the classes in that object

def get_all_classes(soup):
    classes = []
    for tag in soup.find_all():
        if tag.get('class'):
            classes.extend(tag['class'])
    return list(set(classes))

#soup = BeautifulSoup(html_string, 'html.parser')
#class_list = get_all_classes(soup)

#----------------------------------------
#a Python function that takes in a BeautifulSoup object and a list of class names and creates a pandas DataFrame with the text content of all elements for every class in the list, storing each class text content in a column

def soup_to_dataframe(soup, class_list):
    df = pd.DataFrame()
    for class_name in class_list:
        elements = soup.find_all(class_=class_name)
        data = [element.get_text() for element in elements]
        while len(data) < 20:
            data.append(np.nan)
        df[class_name] = data
    return df


#----------------------------------------
#a Python function that takes a BeautifulSoup soup object and shows examples of the text content of every class using a pandas dataframe

def show_class_examples_df(soup,number):
    class_list = get_all_classes(soup)
    data = []
    for class_name in class_list:
        elements = soup.find_all(class_=class_name)
        for element in elements:
            data.append([class_name, element.get_text()])
    df = pd.DataFrame(data, columns=["Class","Text"])
    for class_name in class_list:
        print(f"Examples of class {class_name}")
        print(df[df['Class'] == class_name].head(number))


#----------------------------------------
#a Python function that uses BeautifulSoup to scrape multiple pages from a URL by clicking the next button and appends the BeautifulSoup objects to a list
def scrape_multiple_pages(url):
    soup_list = []
    while True:
        # Send a request to the website
        response = requests.get(url)
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.content, 'html.parser')
        soup_list.append(soup)
        # Find the next button
        next_button = soup.find('button', {'class': 'pages-list'})
        if next_button:
            # Update the URL to the next page
            url = next_button['href']
        else:
            break
    return soup_list


#----------------------------------------
# a Python function that takes in a list of BeautifulSoup objects and returns a single BeautifulSoup object containing all the text content from each page
def merge_soup_list(soup_list):
    # Concatenate all the text content from the soup objects
    text = '\n'.join([soup.get_text() for soup in soup_list])
    # Create a new soup object from the concatenated text
    soup = BeautifulSoup(text, 'html.parser')
    return soup

#----------------------------------------

import requests
from bs4 import BeautifulSoup

def scrape_multiple_pages_next_button(url):
    soup_list = []
    while True:
        # Send a request to the website
        response = requests.get(url)
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.content, 'html.parser')
        soup_list.append(soup)
        # Find the next button
        next_button = soup.find('a', string='Next')
        if next_button:
            # Update the URL to the next page
            url = next_button['href']
        else:
            break
    return soup_list

#----------------------------------------

# Python function that takes in a BeautifulSoup object and a class name, and returns the text content of all elements with that class

def get_text_by_class(soup, class_name):
    elements = soup.find_all(class_=class_name)
    return [element.get_text() for element in elements]

#----------------------------------------
#a Python function that takes in a BeautifulSoup object and a class name, and prints the text content of all elements with that class
def print_text_by_class(soup, class_name):
    elements = soup.find_all(class_=class_name)
    for element in elements:
        print(element.get_text())
#----------------------------------------

# a Python function that takes in a BeautifulSoup object and a class name, and returns a DataFrame containing the text content of all elements with that class:

def class_to_dataframe(soup, class_name):
    elements = soup.find_all(class_=class_name)
    data = [[class_name, element.get_text()] for element in elements]
    df = pd.DataFrame(data, columns=["Class","Text"])
    return df

#----------------------------------------
#Python function that takes in a BeautifulSoup object and a class name, and returns a DataFrame containing the text content of all div elements with that class:



def div_class_to_dataframe(soup, class_name):
    elements = soup.find_all("div", class_=class_name)
    data = [[element.get_text()] for element in elements]
    df = pd.DataFrame(data, columns=["Text"])
    return df

#----------------------------------------
# Python function that takes in a BeautifulSoup object and an id name, and returns a DataFrame containing the text content of all div elements with that id:


def div_id_to_dataframe(soup, id_name):
    elements = soup.find_all("div", id=id_name)
    data = [[element.get_text()] for element in elements]
    df = pd.DataFrame(data, columns=["Text"])
    return df
#----------------------------------------
#a Python function that takes in a BeautifulSoup object and a string, and returns all classes that contain the string as part of the class names

def find_class_by_string(soup, class_string):
    classes = []
    for tag in soup.find_all():
        classes.extend(tag.get("class", []))
    return [c for c in classes if class_string in c]
#----------------------------------------

#a Python function that takes in a DataFrame, a directory, and a value and saves the DataFrame as a CSV file under the name of the value passed combined with the current date and time:

def save_dataframe(df, directory, value):
    now = datetime.datetime.now()
    filename = value + '_' + now.strftime("%Y-%m-%d_%H-%M-%S") + '.csv'
    df.to_csv(directory + '/' + filename)

#----------------------------------------
#a Python function that takes in a list of BeautifulSoup objects, a list of class names, and returns a DataFrame with the text content of all elements for each class in each object of the list, appending the results to the DataFrame for the remainder of the loop:



def soup_list_to_dataframe(soup_list, class_list):
    df = pd.DataFrame()
    for class_name in class_list:
        for i, soup in enumerate(soup_list):
            elements = soup.find_all(class_=class_name)
            data = [element.get_text() for element in elements]
            if i == 0:
                df[class_name] = data
            else:
                df = df.append(pd.DataFrame(data, columns=[class_name]))
    return df

#----------------------------------------
#a Python function that takes in a list of URLs and returns a list of BeautifulSoup objects extracted from each URL

def get_soup_from_urls(url_list):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.implicitly_wait(5)
    soup_list = []
    for url in url_list:
        driver.get(url)
        results = []
        content = driver.page_source
        soup = BeautifulSoup(content)
        soup_list.append(soup)
        print("soup for "+ url + "is appended")
    return soup_list

#----------------------------------------
#a Python function that takes in a list of DataFrames, appends them into a single DataFrame, with each DataFrame becoming a column and reset the index after concatenating the DataFrames

def soup_list_to_dataframe_list(soup_list, class_list):
    df_list = []
    for class_name in class_list:
        df = pd.DataFrame()
        for i, soup in enumerate(soup_list):
            elements = soup.find_all(class_=class_name)
            data = [element.get_text() for element in elements]
            if i == 0:
                df[class_name] = data
            else:
                df = df.append(pd.DataFrame(data, columns=[class_name]))
        df_list.append(df)
    return df_list


#----------------------------------------
#a Python function that takes in a DataFrame, a directory and a value, and saves the DataFrame as an excel file under the name of the value passed combined with the current date and time
def save_dataframe_to_excel(df, directory, value):
    now = datetime.datetime.now()
    filename = value + now.strftime("_%Y-%m-%d_%H-%M-%S") + ".xlsx"
    filepath = os.path.join(directory, filename)
    df.to_excel(filepath)

#----------------------------------------

def extract_links_from_class(soup, class_name):
    links = []
    for link in soup.find_all("a", class_=class_name):
        links.append(link.get("href"))
    return links
#----------------------------------------
def GetPages(url):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(url)
    #driver.get('https://dubai.dubizzle.com/en/property-for-sale/residential/')
    results = []
    content = driver.page_source
    soup = BeautifulSoup(content)
    class_name = 'page'
    Pages_list = extract_links_from_class(soup, class_name)
    return Pages_list

#----------------------------------------
def append_dataframes(df_list):
    result = pd.DataFrame()
    for df in df_list:
        result = pd.concat([result, df], axis=1)
    result = result.reset_index(drop=True)
    return result

#----------------------------------------
# Function that returns a dataframe of property data from a beautiful soup object
def extractDataFromSoup(soup):
    # return list of text for all listings featuring this class
    propertyFeatures = get_text_by_class(soup,'b6a29bc0')
    beds = []
    baths = []
    area = []
    # for loops to split the one list of property features in to 3 distinct lists
    for i in range(0,len(propertyFeatures)-1,3):
        beds.append(propertyFeatures[i])
    for i in range(1,len(propertyFeatures)-1,3):
        baths.append(propertyFeatures[i])
    for x in propertyFeatures:
        if 'sqft' in x:
            area.append(x)
    # Removing sqft from all area values
    area = [a.strip(' sqft') for a in area]
    # class values for address, residence type and rent price respectively
    class_list = ['_7afabd84','_9a4e3964','f343d9ce']
    # extracts data for these class values and returns dataframe
    data = soup_to_dataframe(soup, class_list)
    # if statements to solve replace nan when dataframe lengths varry
    while len(data.index) < 24:
        # Creating an empty series
        s = pd.Series([np.nan,np.nan,np.nan],index=['_7afabd84','_9a4e3964','f343d9ce'])
        # Appending empty series to df
        data = data.append(s,ignore_index=True)
    while len(beds) < 24:
        # appending a nan value to match the varrying length of arrays
        beds.append(np.nan)
    while len(baths) < 24:
        # appending a nan value to match the varrying length of arrays
        baths.append(np.nan)
    while len(area) < 24:
        # appending a nan value to match the varrying length of arrays
        area.append(np.nan)
    # Adding columns to the dataframe
    data['Beds']  =  beds
    data['Baths'] = baths
    data['Area (sqft)']  =  area
    # Returning dataframe
    return data

#---------------------







#----------------------------------------
#----------------------------------------
#----------------------------------------
#----------------------------------------
#----------------------------------------
#----------------------------------------
#----------------------------------------
#----------------------------------------
#----------------------------------------
#----------------------------------------
#----------------------------------------

#----------------------------------------
#----------------------------------------
#----------------------------------------
#----------------------------------------
