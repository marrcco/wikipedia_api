# Wikipedia API in Python
This is a Python library that provides functions for crawling monthly and daily pageviews for a specified Wikipedia article, as well as for retrieving the top articles for a given date range.

# Installation
You can install this library using pip:
pip install wikipedia-api

# Usage
## Monthly Pageviews
To retrieve the monthly pageviews for a specified Wikipedia article, use the monthly_pageviews function and provide the article ID as an argument:
```
from wikipedia_api import monthly_pageviews

article_id = '7428067'  # The article ID for "Python (programming language)"
pageviews = monthly_pageviews(article_id)
```
The monthly_pageviews function returns a dictionary where the keys are the dates in YYYYMM format and the values are the number of pageviews.

## Daily Pageviews
To retrieve the daily pageviews for a specified Wikipedia article and year, use the daily_pageviews function and provide the article ID and year as arguments:
```
from wikipedia_api import daily_pageviews

article_id = '7428067'  # The article ID for "Python (programming language)"
year = 2022
pageviews = daily_pageviews(article_id, year)
```
The daily_pageviews function returns a dictionary where the keys are the dates in YYYYMMDD format and the values are the number of pageviews.

## Most Viewed Articles
To retrieve the top articles for a given date range, use the most_viewed_articles function and provide the start and end dates in the format YYYY/MM/DD as arguments:
```
from wikipedia_api import most_viewed_articles

start_date = '2022/01/01'
end_date = '2022/01/31'
top_articles = most_viewed_articles(start_date, end_date)
```
The most_viewed_articles function returns a list of dictionaries where each dictionary contains information about a top article, including the article ID, title, and number of pageviews.

# License
This library is released under the MIT License.
