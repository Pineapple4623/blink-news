# summary_service.py
import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure the Gemini API
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
else:
    print("Warning: GEMINI_API_KEY not set in environment variables")

def summarize_article(title, content, max_length=180):
    """
    Summarize an article using Google's Gemini AI
    
    Args:
        title: Article title
        content: Article content to summarize
        max_length: Maximum length of the summary in words
        
    Returns:
        A string containing the summarized article content
    """
    if not GEMINI_API_KEY:
        return "API key not configured. Please set GEMINI_API_KEY in your environment variables."
    
    try:
        # Create a prompt for the model
        prompt = f"""You are a professional news editor tasked with creating concise, engaging summaries.
        
        Create a clear and informative summary of this news article that a general audience can easily understand.
        Focus on these aspects:
        1. The main news or key finding
        2. Important context or background
        3. Any significant implications or next steps
        
        Guidelines:
        - Write in a journalistic, objective style
        - Use simple, clear language
        - Keep the summary around {max_length} words
        - Maintain a neutral tone
        - Focus on facts, not speculation
        - Include specific numbers or data points if present
        - Avoid redundancy and filler words
        
        Article Title: {title}
        
        Article Content:
        {content}
        
        Summary:"""
        
        # Create a Gemini model instance
        model = genai.GenerativeModel('gemini-2.0-flash-lite')
        
        # Generate the summary
        response = model.generate_content(prompt)
        print("API Response:", response)
        
        # Extract and clean up the summary
        summary = response.candidates[0].content.parts[0].text.strip() if response.candidates else "Failed to generate summary."
        
        return summary
    
    except Exception as e:
        print(f"Error generating summary: {e}")
        return "Unable to generate summary at this time."

def backup_summarization(title, content, max_length=150):
    """
    A fallback summarization method in case the API fails
    Uses simple extractive summarization
    
    Args:
        title: Article title
        content: Article content to summarize
        max_length: Maximum length of the summary in characters
        
    Returns:
        A string containing a simple summary
    """
    # Simple fallback: return the first part of the content
    if len(content) <= max_length:
        return content
        
    # Find a good breaking point (end of sentence)
    cutoff = content[:max_length].rfind('.')
    if cutoff == -1:  # No period found
        cutoff = content[:max_length].rfind(' ')
    if cutoff == -1:  # No space found
        cutoff = max_length
        
    return content[:cutoff + 1]