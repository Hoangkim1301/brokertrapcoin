from datetime import date
from pynytimes import NYTAPI
import os
import configparser
import pandas as pd
import json

# initiate connection w/ personal API key
def get_api_key():
    config = configparser.ConfigParser()
    config.read('config.ini')
    nytimes_api_key = config.get('nytimes', 'api_key')
    return nytimes_api_key

# article search: we can search for the currently listed articles on the NYT
# filter by keyword, title, publication date, location, source, news desk and many more
def article_search(query, begin_date, end_date):
    api = NYTAPI(
        key = get_api_key(), # Get your own key at https://developer.nytimes.com/
        parse_dates = True)
    
    search_result = api.article_search(
        query = query,
        results = 10,
        options = {
            "sort": "newest",
            "sources": ["The New York Times"]
        },
        dates = {
            "begin": begin_date,
            "end": end_date
        }
    )
    
    # for each of the articles in the list, get the information that is stored in a nested dictionary:
    headline = map(lambda x: x["headline"]["main"], search_result)
    author = map(lambda x: x["headline"]["kicker"], search_result)
    leadparagraph = map(lambda x: x["lead_paragraph"], search_result)
    #whole_paragraphs = map(lambda x: x["paragraph"], search_result)
    pubdate = map(lambda x: x["pub_date"], search_result)

    # since keywords are a branch down in the nested dictionary, we need to add an additional for loop to collect all keywords:
    keywords = map(lambda x:list(i["value"] for i in x["keywords"]), search_result)

    # transforming the data into a pandas dataframe:
    data={'headline': list(headline), 'author': list(author), 'leadparagraph':list(leadparagraph),
           'publication date': list(pubdate), "keywords": list(keywords)}
    df = pd.DataFrame(data)

    # exporting the data to csv:
    df.to_csv('NYT_data.csv')
    
    #return search_result
    
def article_archiev():
    api = NYTAPI(
        key = get_api_key(), # Get your own key at https://developer.nytimes.com/
        parse_dates = True)
    
    month = date(2024, 1, 1)
    search_result = api.archive_metadata(
        date = month
    )
    # for each of the articles in the list, get the information that is stored in a nested dictionary:
    headline = map(lambda x: x["headline"]["main"], search_result)
    author = map(lambda x: x["headline"]["kicker"], search_result)
    leadparagraph = map(lambda x: x["content"], search_result)
    #whole_paragraphs = map(lambda x: x["paragraph"], search_result)
    pubdate = map(lambda x: x["pub_date"], search_result)

    # since keywords are a branch down in the nested dictionary, we need to add an additional for loop to collect all keywords:
    keywords = map(lambda x:list(i["value"] for i in x["keywords"]), search_result)

    # transforming the data into a pandas dataframe:
    data={'headline': list(headline), 'author': list(author), 'leadparagraph':list(leadparagraph),
           'publication date': list(pubdate), "keywords": list(keywords)}
    df = pd.DataFrame(data)

    # exporting the data to csv:
    df.to_csv('NYT_data.csv')
    
#main function
if __name__ == "__main__":
    res = article_search("siemens", date(2020, 10, 5), date.today())
    #print(res)
    #article_archiev()