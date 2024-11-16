-- Table for storing news sources
CREATE TABLE news_sources (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,          -- The name of the news source
    base_url TEXT NOT NULL,              -- Base URL of the news source
    crawl_pattern TEXT NOT NULL,         -- URL pattern to identify articles for crawling
    content_config JSON NOT NULL,        -- JSON configuration for extracting content from the page
    last_crawled DATETIME DEFAULT NULL   -- Timestamp of the last crawl
);

-- Table for storing news articles
CREATE TABLE articles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    source_id INT NOT NULL,              -- Foreign key linking to the news source
    url TEXT NOT NULL UNIQUE,            -- URL of the article
    title TEXT NOT NULL,                 -- Title of the article
    published_date DATETIME,             -- Published date of the article (if available)
    content LONGTEXT,                    -- Full content of the article
    summary TEXT,                        -- Short AI-generated summary of the article
    crawled_date DATETIME DEFAULT CURRENT_TIMESTAMP, -- Timestamp when the article was crawled
    FOREIGN KEY (source_id) REFERENCES news_sources(id) ON DELETE CASCADE -- Cascade deletion with news_sources
);

-- Optional table for news categories
CREATE TABLE categories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL            -- Name of the category
);

-- Many-to-many relationship between articles and categories
CREATE TABLE article_categories (
    article_id INT NOT NULL,             -- Foreign key linking to the article
    category_id INT NOT NULL,            -- Foreign key linking to the category
    PRIMARY KEY (article_id, category_id),
    FOREIGN KEY (article_id) REFERENCES articles(id) ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE CASCADE
);

-- Table for storing generated summaries
CREATE TABLE summaries (
    id INT AUTO_INCREMENT PRIMARY KEY,
    type ENUM('daily', 'weekly', 'monthly') NOT NULL, -- Summary type (daily, weekly, monthly)
    summary_date DATE NOT NULL,                      -- The date for which the summary is generated
    content LONGTEXT NOT NULL,                       -- The summarized content
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP    -- Timestamp when the summary was created
);
