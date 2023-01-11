import pandas as pd
import requests
from datetime import date, timedelta,datetime

# function http_client starts new session and setup the requests headers
def http_client():
    session = requests.Session()
    session.headers.update(
        {
            "User-Agent" : ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"
                            "AppleWebKit/537.36 (KHTML, like Gecko) "
                            "Chrome/106.0.0.0 Safari/537.36"),
            "Accept-Language" : "en-US, en:q=0.5"
        }
    )
    return session


# function make_request sends requests and returns response
def make_request(client,URL):
    try:
        response = client.get(URL)
    except requests.RequestException:
        raise Exception(f"HTTP Error")
        return
    if(response.status_code == 200):
        return response


# function monthly_pageviews takes article_id(which is headline of article from wiki),
# wiki_country which can be any wiki country, default is en
# and year
# it loops through all months for selected years and returns dataframe with pageviews for selected article for each month
def monthly_pageviews(client,article_id,wiki_country="en",year=2022):
    curl = f"https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/{wiki_country}.wikipedia/all-access/all-agents/{article_id}/monthly/{year}010100/{year}123100"
    req = make_request(client=client,URL=curl)
    json_data = req.json()

    all_data = []
    for x in range(0,len(json_data["items"])):
        current_data_date = json_data["items"][x]["timestamp"]
        current_data_pageviews = json_data["items"][x]["views"]
        current_data = {"date" : current_data_date,
                        "pageviews" : current_data_pageviews,
                        "article" : article_id,
                        "country" : wiki_country}
        print(current_data)
        all_data.append(current_data)

    df = pd.DataFrame(all_data)

    return df


# function daily_pageviews takes article_id(which is headline of article from wiki),
# wiki_country which can be any wiki country, default is en
# and year
# it loops through all months for selected years and returns dataframe with pageviews for selected article daily
def daily_pageviews(client,article_id,wiki_country="en",year=2022):
    curl = f"https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/{wiki_country}.wikipedia/all-access/all-agents/{article_id}/daily/{year}010100/{year}123100"
    req = make_request(client=client,URL=curl)
    json_data = req.json()

    all_data = []
    for x in range(0,len(json_data["items"])):
        current_data_date = json_data["items"][x]["timestamp"]
        current_data_pageviews = json_data["items"][x]["views"]
        current_data = {"date" : current_data_date,
                        "pageviews" : current_data_pageviews,
                        "article" : article_id,
                        "country" : wiki_country}
        print(current_data)
        all_data.append(current_data)

    df = pd.DataFrame(all_data)

    return df

# function to iterate between two dates
def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)


# function most viewed articles returns list of the most topular articles for each day specified in data range(since,until)
# you can specify wiki_country for these top articles and you can choose how many top articles you want to get per day (max. 1000)
def most_viewed_articles(client,wiki_country="us",since="2021/01/02",until="2022/01/28",num_of_articles=10):
    if(num_of_articles > 1000):
        num_of_articles = 1000
        print("can't crawl more than 1000 top articles.\default value is set to 1000")

    since_split = since.split("/")
    until_split = until.split("/")
    since_year,since_month,since_day = [since_split[0],since_split[1],since_split[2]]
    until_year,until_month,until_day = [until_split[0],until_split[1],until_split[2]]


    start_date = date(int(since_year),int(since_month),int(since_day))
    end_date = date(int(until_year),int(until_month),int(until_day))

    all_data = []
    for single_date in daterange(start_date, end_date):
        single_date = single_date.strftime("%Y/%m/%d")
        print(f"scraping top {num_of_articles} for on {single_date}")
        curl = f"https://wikimedia.org/api/rest_v1/metrics/pageviews/top-per-country/{wiki_country.upper()}/all-access/{single_date}"

        req = make_request(client=client,URL=curl)
        json_data = req.json()

        current_article_year = json_data["items"][0]["year"]
        current_article_month = json_data["items"][0]["month"]
        current_article_day = json_data["items"][0]["day"]
        for x in range(0, num_of_articles):
            current_article_name = json_data["items"][0]["articles"][x]["article"]
            current_article_rank = json_data["items"][0]["articles"][x]["rank"]
            current_article_views = json_data["items"][0]["articles"][x]["views_ceil"]
            current_article_data = {"year" : current_article_year,
                                    "month" : current_article_month,
                                    "day" : current_article_day,
                                    "article" : current_article_name,
                                    "views" : current_article_views,
                                    "rank" : current_article_rank}
            all_data.append(current_article_data)
            print(current_article_data)


    df = pd.DataFrame(all_data)
    return df

client = http_client()
monthly = monthly_pageviews(client=client,article_id="Australian_Open")
daily = daily_pageviews(client=client,article_id="Australian_Open",year=2023)
top_articles_usa = most_viewed_articles(client=client,since="2021/01/01",until="2022/01/01")

