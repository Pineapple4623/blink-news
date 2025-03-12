# app.py
from flask import Flask, render_template, request, redirect, url_for, jsonify, abort
import database
# import news_service
import summary_service
import os
from datetime import datetime, timedelta
from threading import Thread
import queue
import time
# Instead of: import news_service
import news_service


# Initialize Flask app
app = Flask(__name__)

# Initialize database
database.init_db()

# Load environment variables
NEWS_API_KEY = os.getenv('NEWS_API_KEY')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

# Queue for background tasks
task_queue = queue.Queue()

def process_background_tasks():
    """Background worker to process tasks"""
    while True:
        try:
            task = task_queue.get()
            if task is None:  # Shutdown signal
                break
            category = task['category']
            fetch_and_store_articles(category)
            database.update_last_fetched_time(category)
        except Exception as e:
            print(f"Error processing background task: {e}")
        finally:
            task_queue.task_done()

# Start background worker
background_worker = Thread(target=process_background_tasks, daemon=True)
background_worker.start()

def should_refresh_category(category):
    """Check if category needs refresh (older than 30 minutes)"""
    conn = database.get_db_connection()
    result = conn.execute(
        "SELECT last_fetched_at FROM categories WHERE name = ?", 
        (category,)
    ).fetchone()
    conn.close()

    if not result or not result['last_fetched_at']:
        return True

    last_fetched = datetime.fromisoformat(result['last_fetched_at'])
    return datetime.utcnow() - last_fetched > timedelta(minutes=30)

@app.context_processor
def inject_now():
    return {'now': datetime.utcnow()}


@app.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    limit = 9
    offset = (page - 1) * limit
    
    # Check if refresh is needed
    if should_refresh_category('General') or 'refresh' in request.args:
        task_queue.put({'category': 'general'})
    
    # Get latest articles from database
    articles = database.get_articles(limit=limit, offset=offset)
    
    # If no articles in database or refresh requested, fetch from API
    if (not articles or 'refresh' in request.args) and NEWS_API_KEY:
        fetch_and_store_articles()
        articles = database.get_articles(limit=limit, offset=offset)
    
    categories = database.get_categories()
    
    return render_template('index.html', 
                          articles=articles, 
                          categories=categories, 
                          current_page=page,
                          current_category='General',
                          apis_configured=(NEWS_API_KEY and GEMINI_API_KEY))

@app.route('/category/<category>')
def category(category):
    page = request.args.get('page', 1, type=int)
    limit = 9
    offset = (page - 1) * limit
    
    # Check if refresh is needed
    if should_refresh_category(category) or 'refresh' in request.args:
        task_queue.put({'category': category.lower()})
    
    # Get articles by category
    articles = database.get_articles(category=category, limit=limit, offset=offset)
    
    # If no articles in database or refresh requested, fetch from API
    if (not articles or 'refresh' in request.args) and NEWS_API_KEY:
        fetch_and_store_articles(category=category.lower())
        articles = database.get_articles(category=category, limit=limit, offset=offset)
    
    categories = database.get_categories()
    
    return render_template('category.html', 
                          articles=articles, 
                          categories=categories, 
                          current_page=page,
                          current_category=category)

@app.route('/article')
def article():
    url = request.args.get('url')
    if not url:
        return redirect(url_for('index'))
    
    article = database.get_article_by_url(url)
    
    if not article:
        abort(404)
    
    categories = database.get_categories()
    
    return render_template('article.html', 
                          article=article, 
                          categories=categories)

@app.route('/search')
def search():
    query = request.args.get('q', '')
    category = request.args.get('category')
    page = request.args.get('page', 1, type=int)
    limit = 9
    offset = (page - 1) * limit
    
    if not query:
        return redirect(url_for('index'))
    
    # Search in database first
    articles = database.search_articles(query, category=category, limit=limit, offset=offset)
    
    # If not enough results and API key is set, search via API
    if len(articles) < limit and NEWS_API_KEY:
        api_articles = news_service.search_news(query, category=category.lower() if category else None, page_size=limit)
        
        # Store new articles and add summaries
        for article_data in api_articles:
            # Check if article already exists
            existing = database.get_article_by_url(article_data['url'])
            if not existing:
                # Generate summary
                summary = summary_service.summarize_article(
                    article_data['title'],
                    article_data['content']
                )
                
                # Save to database
                database.save_article(
                    title=article_data['title'],
                    source=article_data['source'],
                    author=article_data['author'],
                    published_at=article_data['published_at'],
                    url=article_data['url'],
                    url_to_image=article_data['url_to_image'],
                    category=category if category else article_data['category'],
                    content=article_data['content'],
                    summary=summary
                )
        
        # Refresh search results
        articles = database.search_articles(query, category=category, limit=limit, offset=offset)
    
    categories = database.get_categories()
    
    template = 'category.html' if category else 'index.html'
    return render_template(template, 
                          articles=articles, 
                          categories=categories, 
                          search_query=query,
                          current_page=page,
                          current_category=category if category else 'General')

@app.route('/refresh')
def refresh():
    """Refresh all categories"""
    categories = database.get_categories()
    for category in categories:
        task_queue.put({'category': category['name'].lower()})
    
    # Redirect back to previous page or home
    return_to = request.args.get('return_to', 'index')
    if return_to == 'category':
        category = request.args.get('category', 'General')
        return redirect(url_for('category', category=category))
    return redirect(url_for('index'))

def fetch_and_store_articles(category='general'):
    """Fetch articles from NewsAPI and store them with summaries"""
    try:
        # Fetch latest articles
        articles = news_service.fetch_top_headlines(category=category)
        
        # Process and store each article
        for article_data in articles:
            try:
                # Check if article already exists
                existing = database.get_article_by_url(article_data['url'])
                if not existing:
                    # Generate summary
                    summary = summary_service.summarize_article(
                        article_data['title'],
                        article_data['content']
                    )
                    
                    # Save to database
                    database.save_article(
                        title=article_data['title'],
                        source=article_data['source'],
                        author=article_data['author'],
                        published_at=article_data['published_at'],
                        url=article_data['url'],
                        url_to_image=article_data['url_to_image'],
                        category=article_data['category'].capitalize(),
                        content=article_data['content'],
                        summary=summary
                    )
            except Exception as e:
                print(f"Error processing article: {e}")
                continue
    except Exception as e:
        print(f"Error fetching articles for category {category}: {e}")

if __name__ == '__main__':
    # Ensure API keys are set
    if not NEWS_API_KEY:
        print("Warning: NEWS_API_KEY not set. News fetching will be disabled.")
    if not GEMINI_API_KEY:
        print("Warning: GEMINI_API_KEY not set. AI summarization will be disabled.")
    
    try:
        # Run the Flask app
        app.run(debug=True)
    finally:
        # Cleanup: stop background worker
        task_queue.put(None)
        background_worker.join(timeout=5)