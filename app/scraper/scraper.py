import datetime
import requests
from bs4 import BeautifulSoup
from .query_string import build_query_string
from .get_content import get_content
from .url_prettier import get_pretty_url

def news_scraper(request):
    config = {}

    config.update(request)

    # URL Google News
    query_string = build_query_string(config["vars"]) if config["vars"] else ""
    url = f"https://news.google.com/search?{query_string}&q={config['keyword']} when:{config.get('timeframe', '1d')}"

    # Request from url
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        "Accept-Encoding": "gzip",
        "Accept-Language": "en-US,en;q=0.9,es;q=0.8",
        "Upgrade-Insecure-Requests": "1",
        "Referer": "https://www.google.com/",
    }
    cookies = {
        "CONSENT": f"YES+cb.{datetime.datetime.now().isoformat().split('T')[0].replace('-', '')}-04-p0.en-GB+FX+667"
    }
    response = requests.get(url, headers=headers, cookies=cookies)
    content = response.content

    # HTML Parser BS4
    soup = BeautifulSoup(content, "html.parser")
    articles = soup.find_all("article")
    results = []
    urlChecklist = []

    for article in articles:
        link_element = article.find(
            "a", href=lambda href: href and href.startswith("./article")
        )
        link = (
            link_element.get("href").replace("./", "https://news.google.com/")
            if link_element
            else None
        )
        if link:
            urlChecklist.append(link)
        figure_element = article.find("figure")
        srcset = (
            figure_element.find("img").get("srcset").split(" ")
            if figure_element and figure_element.find("img")
            else []
        )
        image = (
            srcset[-2]
            if srcset
            else (
                figure_element.find("img").get("src")
                if figure_element and figure_element.find("img")
                else None
            )
        )
        if image and image.startswith("/"):
            image = f"https://news.google.com{image}"
        title_element = (
            article.find_all("div", {"class": "m5k28"})[0]
            .find_all("div", {"class": "B6pJDd"})[0]
            .find_all("div")[0]
            .find_all("a")
        )
        title = title_element[0].text
        source_element = article.find("div", {"data-n-tid": True})
        source = source_element.text if source_element else None
        datetime_element = article.find_all("div:last-child time")
        datetime_str = datetime_element.get("datetime") if datetime_element else None
        datetime_val = (
            datetime.datetime.strptime(datetime_str, "%Y-%m-%dT%H:%M:%S.%fZ")
            if datetime_str
            else None
        )
        time = datetime_element.text if datetime_element else None
        main_article = {
            "title": title,
            "link": link,
            "image": image,
            "source": source,
            "datetime": datetime_val,
            "time": time,
            "url": url,
        }
        results.append(main_article)

    if config["pretty_url"]:
        for result in results:
            new_link = get_pretty_url(result["link"])
            result["link"] = new_link

    if config["get_content"]:
        filterWords = config.get("filter_words", [])
        results = get_content(results, filterWords)
    
    return
