# news_service.py
import requests
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

NEWS_API_KEY = os.getenv('NEWS_API_KEY')
NEWS_API_URL = 'https://newsapi.org/v2/'

def fetch_top_headlines(category='general', country='us', page_size=20, page=1):
    """Fetch top headlines from NewsAPI"""
    
    if not NEWS_API_KEY:
        raise ValueError("NEWS_API_KEY is not set in environment variables")
    
    params = {
        'category': category,
        'country': country,
        'pageSize': page_size,
        'page': page,
        'apiKey': NEWS_API_KEY
    }
    
    try:
        response = requests.get(f'{NEWS_API_URL}top-headlines', params=params)
        response.raise_for_status()  # Raise an exception for HTTP errors
        
        data = response.json()
        
        # Process and normalize the data
        articles = []
        for article in data.get('articles', []):
            # Convert the publish date string to a datetime object
            published_at = article.get('publishedAt')
            if published_at:
                try:
                    published_at = datetime.fromisoformat(published_at.replace('Z', '+00:00'))
                except ValueError:
                    published_at = datetime.now()
            
            # Normalize the article data
            processed_article = {
                'title': article.get('title', 'No Title'),
                'source': article.get('source', {}).get('name', 'Unknown Source'),
                'author': article.get('author', 'Unknown Author'),
                'published_at': published_at,
                'url': article.get('url', ''),
                'url_to_image': article.get('urlToImage', ''),
                'content': article.get('content', article.get('description', 'No content available')),
                'category': category
            }
            
            articles.append(processed_article)
        
        return articles
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching news: {e}")
        return []

def search_news(query, category=None, language='en', sort_by='publishedAt', page_size=20, page=1):
    """Search for news articles by keyword and optionally filter by category"""
    
    if not NEWS_API_KEY:
        raise ValueError("NEWS_API_KEY is not set in environment variables")
    
    # For category-specific searches, use top-headlines endpoint
    if category and category.lower() != 'general':
        params = {
            'q': query,
            'category': category.lower(),
            'language': language,
            'pageSize': page_size,
            'page': page,
            'apiKey': NEWS_API_KEY
        }
        endpoint = 'top-headlines'
    else:
        # For general searches or no category, use everything endpoint
        params = {
            'q': query,
            'language': language,
            'sortBy': sort_by,
            'pageSize': page_size,
            'page': page,
            'apiKey': NEWS_API_KEY
        }
        endpoint = 'everything'
    
    try:
        response = requests.get(f'{NEWS_API_URL}{endpoint}', params=params)
        response.raise_for_status()
        
        data = response.json()
        
        # Process and normalize the data
        articles = []
        for article in data.get('articles', []):
            # Convert the publish date string to a datetime object
            published_at = article.get('publishedAt')
            if published_at:
                try:
                    published_at = datetime.fromisoformat(published_at.replace('Z', '+00:00'))
                except ValueError:
                    published_at = datetime.now()
            
            # Use provided category or default to General
            article_category = category if category else 'General'
            
            # Normalize the article data
            processed_article = {
                'title': article.get('title', 'No Title'),
                'source': article.get('source', {}).get('name', 'Unknown Source'),
                'author': article.get('author', 'Unknown Author'),
                'published_at': published_at,
                'url': article.get('url', ''),
                'url_to_image': article.get('urlToImage', ''),
                'content': article.get('content', article.get('description', 'No content available')),
                'category': article_category
            }
            
            articles.append(processed_article)
        
        return articles
    
    except requests.exceptions.RequestException as e:
        print(f"Error searching news: {e}")
        return []