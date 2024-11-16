import os
import google.generativeai as genai
import mysql.connector
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Database configuration
DB_CONFIG = {
    "host": "localhost",
    "user": "your_username",
    "password": "your_password",
    "database": "summix"
}

# Configure Gemini AI SDK
genai.configure(api_key=os.environ["API_KEY"])

# Function to summarize text using Gemini AI
def summarize_text(text):
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")  # Specify the model
        response = model.generate_content(f"Summarize this news article: {text}")
        return response.text  # Extract the summary text from the response
    except Exception as e:
        print(f"Error summarizing text: {e}")
        return "Failed to generate summary."

# Function to connect to the database
def connect_to_database():
    return mysql.connector.connect(**DB_CONFIG)

# Function to scrape articles from a single news source
def scrape_articles(source):
    source_id, base_url, crawl_pattern, content_config = source

    print(f"Scraping articles from: {base_url}")
    response = requests.get(base_url)
    if response.status_code != 200:
        print(f"Failed to fetch {base_url}: {response.status_code}")
        return []

    soup = BeautifulSoup(response.content, "html.parser")
    articles = []
    
    # Find article links based on the crawl pattern
    for link in soup.select(crawl_pattern):
        article_url = urljoin(base_url, link.get("href"))
        if article_url not in articles:
            articles.append(article_url)
    
    return articles

# Function to fetch article content
def fetch_article_content(url, content_config):
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to fetch {url}: {response.status_code}")
        return None, None

    soup = BeautifulSoup(response.content, "html.parser")
    title = soup.select_one(content_config["title"]).get_text(strip=True)
    content = soup.select_one(content_config["content"]).get_text(strip=True)

    return title, content

# Main crawler logic
def crawl_news():
    db_connection = connect_to_database()
    cursor = db_connection.cursor()

    # Fetch news sources from the database
    cursor.execute("SELECT id, base_url, crawl_pattern, content_config FROM news_sources")
    sources = cursor.fetchall()

    for source in sources:
        articles = scrape_articles(source)
        for article_url in articles:
            cursor.execute("SELECT id FROM articles WHERE url = %s", (article_url,))
            if cursor.fetchone():
                continue  # Skip if the article is already in the database

            title, content = fetch_article_content(article_url, eval(source[3]))
            if title and content:
                summary = summarize_text(content)  # Generate summary using Gemini AI
                cursor.execute(
                    "INSERT INTO articles (source_id, url, title, content, summary, published_date) VALUES (%s, %s, %s, %s, %s, NOW())",
                    (source[0], article_url, title, content, summary)
                )
                print(f"Added article: {title}")
    
    db_connection.commit()
    cursor.close()
    db_connection.close()

if __name__ == "__main__":
    crawl_news()
