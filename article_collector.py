import json, requests
from datetime import date
import argparse

'''
TASK

GOAL:
Collect 125 articles from the NewsAPI.org about the movie Killers of the Flower Moon.

PARAMETERS:
API_KEY and QUERY STRING are hard coded into the script. Change them before running the script.
'''

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~ ARGPARSE ~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
def get_args():
    parser = argparse.ArgumentParser(description='Collect articles from NewsAPI.org')
    parser.add_argument('-o', '--output_file', type=str, help='Query string for NewsAPI.org')
    args = parser.parse_args()
    return args

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~ HYPER-PARAMETERS ~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
API_KEY = 'd2abbe0513984b9b9482468339ca750b'

#NEWS_QUERY_URL = "https://newsapi.org/v2/everything?qInTitle={}&from={}&to={}&language=en&apiKey={}"    # Search by keywords in title
NEWS_QUERY_URL = "https://newsapi.org/v2/everything?q={}&from={}&to={}&language=en&apiKey={}"          # Search by keywords in title and body

QUERY_STRING = "(Killers OR Killer) AND Flower AND Moon"

END_DATE = date.today()                 # Today's date
START_DATE = END_DATE.replace(month=10) # One month age

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~ FUNCTIONS ~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Takes QUERY_STRING and makes it readable by NewsAPI.org
def format_string(string):
    for i in string:
        if i == " ":
            string = string.replace(i, "%20")
    return string

# Function to fetch news from newsapi.org
def fetch_latest_news(output_file):
    query_formatted = format_string(QUERY_STRING)

    # Generate HTTP request
    query_string = NEWS_QUERY_URL.format(query_formatted, START_DATE, END_DATE, API_KEY)

    # Send HTTP request
    response = requests.get(query_string)

    if response.status_code != 200:
        raise Exception('Error fetching news from newsapi.org')
    
    data = response.json()

    # Dump data is external file for analysis
    with open(f'output/{output_file}.json', 'w') as f:
        json.dump(data, f, indent=4)

    # Return list of dictionaries for each article 
    return data["articles"]

# Main
def main():
    args = get_args()
    fetch_latest_news(args.output_file)

# Usage: python3 article_collector.py -o output_file
if __name__ == '__main__':
    main()
