# database.py
import sqlite3
from datetime import datetime

def get_db_connection():
    conn = sqlite3.connect('news_summaries.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    
    # Create articles table
    conn.execute('''
    CREATE TABLE IF NOT EXISTS articles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        source TEXT NOT NULL,
        author TEXT,
        published_at TEXT NOT NULL,
        url TEXT NOT NULL UNIQUE,
        url_to_image TEXT,
        category TEXT NOT NULL,
        content TEXT NOT NULL,
        summary TEXT NOT NULL,
        created_at TEXT NOT NULL
    )
    ''')
    
    # Drop and recreate categories table to ensure proper schema
    conn.execute('DROP TABLE IF EXISTS categories')
    
    # Create categories table with last_fetched_at column
    conn.execute('''
    CREATE TABLE IF NOT EXISTS categories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        last_fetched_at TEXT
    )
    ''')
    
    # Insert default categories
    categories = ['General', 'Business', 'Technology', 'Entertainment', 'Sports', 'Science', 'Health']
    for category in categories:
        try:
            conn.execute('INSERT INTO categories (name) VALUES (?)', (category,))
        except sqlite3.IntegrityError:
            # Category already exists
            pass
    
    conn.commit()
    conn.close()

def save_article(title, source, author, published_at, url, url_to_image, category, content, summary):
    conn = get_db_connection()
    
    # Format the datetime objects
    if isinstance(published_at, datetime):
        published_at = published_at.isoformat()
    
    created_at = datetime.now().isoformat()
    
    try:
        conn.execute('''
        INSERT INTO articles (title, source, author, published_at, url, url_to_image, category, content, summary, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (title, source, author, published_at, url, url_to_image, category, content, summary, created_at))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        # Article already exists (URL is unique)
        return False
    finally:
        conn.close()

def get_articles(category=None, limit=10, offset=0):
    conn = get_db_connection()
    
    if category and category.lower() != 'general':
        articles = conn.execute('''
        SELECT * FROM articles 
        WHERE category = ? 
        ORDER BY published_at DESC 
        LIMIT ? OFFSET ?
        ''', (category, limit, offset)).fetchall()
    else:
        articles = conn.execute('''
        SELECT * FROM articles 
        ORDER BY published_at DESC 
        LIMIT ? OFFSET ?
        ''', (limit, offset)).fetchall()
    
    conn.close()
    return articles

def get_article_by_url(url):
    conn = get_db_connection()
    article = conn.execute('SELECT * FROM articles WHERE url = ?', (url,)).fetchone()
    conn.close()
    return article

def search_articles(query, category=None, limit=10, offset=0):
    conn = get_db_connection()
    
    if category and category.lower() != 'general':
        articles = conn.execute('''
        SELECT * FROM articles 
        WHERE (title LIKE ? OR content LIKE ? OR summary LIKE ?)
        AND category = ?
        ORDER BY published_at DESC 
        LIMIT ? OFFSET ?
        ''', (f'%{query}%', f'%{query}%', f'%{query}%', category, limit, offset)).fetchall()
    else:
        articles = conn.execute('''
        SELECT * FROM articles 
        WHERE title LIKE ? OR content LIKE ? OR summary LIKE ?
        ORDER BY published_at DESC 
        LIMIT ? OFFSET ?
        ''', (f'%{query}%', f'%{query}%', f'%{query}%', limit, offset)).fetchall()
    
    conn.close()
    return articles

def get_categories():
    conn = get_db_connection()
    categories = conn.execute('SELECT * FROM categories').fetchall()
    conn.close()
    return categories


def delete_articles_by_category(category):
    """Deletes all articles of a specific category to force fetching fresh data."""
    conn = get_db_connection()
    conn.execute("DELETE FROM articles WHERE category = ?", (category,))
    conn.commit()
    conn.close()


def update_last_fetched_time(category_name):
    """Updates the last fetched time for a given category."""
    conn = get_db_connection()
    now_iso = datetime.utcnow().isoformat()
    conn.execute("UPDATE categories SET last_fetched_at = ? WHERE name = ?", (now_iso, category_name))
    conn.commit()
    conn.close()
