import requests
from bs4 import BeautifulSoup
import pandas as pd

# Define the URL of the website you want to scrape
url = 'https://frontier.com/search/?referrerPageUrl=https%3A%2F%2Ffrontier.com%2Fshop%2Ftv&=&query=&tabOrder=.%2Findex.html%2Cpromotions%2Cproducts%2Cfaqs%2Cblogs%2Csupport%2Cvideos&facetFilters=%7B%7D&filters=%7B%7D&verticalUrl=Products.html'  

# Send an HTTP GET request to the URL
response = requests.get(url)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the HTML content of the page
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Extract data from the webpage (replace this with your specific scraping logic)
    # Example: Extract all the links on the page
    print(soup)
    links = soup.find_all('a')
    text_data = soup.get_text()
    print(text_data)
    print(links)

    
    # Print the links
    Links = []
    Text = []
    for link in links:
        print(link)
        print(link.get('href'))
        if(str(link.get('href')).find('/') != -1):
            Links.append(link.get('href'))
            text_data=""
            response = requests.get(url+link.get('href'))
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                text_data = soup.get_text()
            Text.append(text_data)
    df1=pd.DataFrame(columns=["Links","Text"])
    df1["Links"]=pd.Series(Links)
    df1["Text"]=pd.Series(Text)
    df1.to_csv(r"C:\Users\sarvesh_s\Documents\NLP EDA\Frontier-POC\output.csv",index=False)
else:
    print(f"Failed to retrieve the web page. Status code: {response.status_code}")
