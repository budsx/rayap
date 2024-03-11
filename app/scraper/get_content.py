from bs4 import BeautifulSoup
import requests

verifyMessages = ["you are human", "are you human", "i'm not a robot", "recaptcha"]


def get_content(articles, filter_words):
    processedArticles = []
    count = 1
    for index, article in enumerate(articles):
        if index <= count:
            processedArticle = extract_article(article, filter_words)
            processedArticles.append(processedArticle)
            break
    return processedArticles


def extract_article(article, filter_words):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate",
        "DNT": "1",
    }
    try:
        response = requests.get(article["link"], headers=headers, timeout=1)
        if response.status_code == 200:
            print("response success")
            content = response.text

            favicon = extractFavicon(content)

            soup = BeautifulSoup(content, "html.parser")
            article_content = soup.get_text(separator="\n")

            if not article_content:
                return {**article, "content": "", "favicon": favicon}

            has_verify_message = any(w in article_content.lower() for w in verifyMessages)
            if has_verify_message:
                return {**article, "content": "", "favicon": favicon}

            cleanedText = clean_text(article_content, filter_words)

            if len(cleanedText.split(" ")) < 100:  # Example threshold: 100 words
                return {**article, "content": "", "favicon": favicon}

            return {**article, "content": cleanedText, "favicon": favicon}
        else:
            print("Response fail")
            return {**article, "content": "", "favicon": ""}
    except Exception as error:
        print(f"Error: {error}")
        return {**article, "content": "", "favicon": ""}


def extractFavicon(content):
    soup = BeautifulSoup(content, "html.parser")
    link = soup.find("link", rel=["icon", "shortcut icon"])
    return link["href"] if link else ""


def clean_text(text, filter_words):
    unwantedKeywords = [
        "subscribe now",
        "sign up",
        "newsletter",
        "subscribe now",
        "sign up for our newsletter",
        "exclusive offer",
        "limited time offer",
        "free trial",
        "download now",
        "join now",
        "register today",
        "special promotion",
        "promotional offer",
        "discount code",
        "early access",
        "sneak peek",
        "save now",
        "don't miss out",
        "act now",
        "last chance",
        "expires soon",
        "giveaway",
        "free access",
        "premium access",
        "unlock full access",
        "buy now",
        "learn more",
        "click here",
        "follow us on",
        "share this article",
        "connect with us",
        "advertisement",
        "sponsored content",
        "partner content",
        "affiliate links",
        "click here",
        "for more information",
        "you may also like",
        "we think you'll like",
        "from our network",
        *filter_words,
    ]
    return "\n".join(
        line
        for line in map(str.strip, text.split("\n"))
        if len(line.split(" ")) > 4
        and not any(keyword in line.lower() for keyword in unwantedKeywords)
    )
