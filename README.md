# Summix: News Scraper & Summarizer

**Summix** is a Python-based news scraper and summarizer application. It collects the latest articles from various news websites, processes them using Gemini AI, and generates concise summaries. Summix also produces daily, weekly, and monthly news digests, helping you stay informed effortlessly.  


## Features

- **News Scraping**: Collects the latest news articles from specified news sources.
- **AI Summarization**: Uses Gemini AI to generate short, readable summaries of news articles.
- **Automated Summaries**: Provides daily, weekly, and monthly summaries of the top news stories.
- **Customizable News Sources**: Easily add or configure news websites for scraping.
- **Database Integration**: Stores scraped news articles and summaries for future reference.
- **Secure API Usage**: API key management via environment variables.  


## Requirements  
- Python 3.9+  
- Gemini AI API key  
- MySQL database  

---

## Installation  

### 1. Clone the repository  
```bash  
git clone https://github.com/cedonulfi/summix.git  
cd summix  
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set up environment variables
Export your Gemini AI API key as an environment variable:
```bash
export API_KEY=<YOUR_API_KEY>
```

### 4. Configure the database
Import the SQL schema into your MySQL database:
```bash
mysql -u your_username -p your_database < schema.sql
```
Update DB_CONFIG in news_crawler.py with your database credentials.

---

## Usage
Run the news crawler
```bash
python news_crawler.py  
```

This will:
- Scrape news articles from configured sources.
- Summarize article content using Gemini AI.
- Store the data in the database.

---

## Configuration

### Add News Sources
Populate the news_sources table with information about the news websites you want to scrape. Fields include:
- base_url: The homepage URL of the news site.
- crawl_pattern: CSS selector for finding article links.
- content_config: JSON configuration for extracting title and content.

### Example news_sources entry:
```bash
INSERT INTO news_sources (name, base_url, crawl_pattern, content_config) VALUES (  
    'Example News',  
    'https://example.com',  
    'a.article-link',  
    '{"title": "h1.article-title", "content": "div.article-content"}'  
);
```

### Output
Summarized articles are stored in the articles table with their titles, URLs, and summaries. Daily, weekly, and monthly summaries are saved in the summaries table.

---

## Dependencies
- beautifulsoup4: For HTML parsing and web scraping.
- mysql-connector-python: For database interaction.
- requests: For making HTTP requests.
- google-generativeai: For integrating with Gemini AI.
Install all dependencies via requirements.txt.

---

## Contribution
Contributions are welcome! Submit a pull request or open an issue to suggest features or report bugs.

---

## License
This project is licensed under the MIT License.

---

### Stay Updated
Summix is constantly evolving to provide smarter and faster news summarization. Follow this repository for updates!
