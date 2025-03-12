# BlinkNews 📰

BlinkNews is an AI-powered news aggregation platform that combines real-time news coverage with artificial intelligence to provide concise, informative summaries of current events.

## Features

- **Real-time News Updates**: Automatically fetches and updates news from various trusted sources
- **AI-Powered Summaries**: Uses Google's Gemini AI to generate concise, readable summaries
- **Category-based Navigation**: Browse news across different categories (General, Business, Technology, etc.)
- **Smart Caching**: Implements efficient caching to reduce API calls and improve performance
- **Responsive Design**: Modern, clean interface that works across all devices
- **Search Functionality**: Search through articles with category filtering
- **Background Processing**: Asynchronous processing for fetching and summarizing articles

## Tech Stack

- **Backend**: Python with Flask
- **Frontend**: HTML5, CSS3, JavaScript
- **Database**: SQLite3
- **AI Services**: Google Gemini AI
- **News Data**: NewsAPI
- **Styling**: Bootstrap 5
- **Additional**: python-dotenv for environment management

## Prerequisites

- Python 3.10 or higher
- NewsAPI key
- Google Gemini API key
- pip (Python package manager)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Pineapple4623/blink-news.git
cd blink-news
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root:
```
NEWS_API_KEY=your_news_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here
```

## Running the Application

```bash
flask run
```

The application will be available at `http://127.0.0.1:5000/`

## Project Structure

```
blink-news/
├── app.py              # Main application file
├── database.py         # Database operations
├── news_service.py     # NewsAPI integration
├── summary_service.py  # Gemini AI integration
├── requirements.txt    # Python dependencies
├── static/            
│   ├── css/           # Stylesheets
│   └── js/            # JavaScript files
└── templates/         # HTML templates
    ├── base.html
    ├── index.html
    ├── article.html
    └── category.html
```

## API Keys

You'll need to obtain API keys from:
- [NewsAPI](https://newsapi.org/) for fetching news articles
- [Google AI Studio](https://ai.google.dev/) for the Gemini AI model

## Features in Detail

### News Fetching
- Automatic fetching of news articles every 30 minutes
- Background processing to avoid blocking the main application
- Smart caching to reduce API calls

### AI Summarization
- Intelligent article summarization using Google's Gemini AI
- Fallback summarization method when API is unavailable
- Configurable summary length and style

### User Interface
- Clean, newspaper-style design
- Category-based navigation
- Responsive grid layout for articles
- Loading states and error handling
- Search functionality with filters

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [NewsAPI](https://newsapi.org/) for providing news data
- [Google Gemini AI](https://ai.google.dev/) for AI capabilities
- [Bootstrap](https://getbootstrap.com/) for the frontend framework

## Contact

GitHub: [@Pineapple4623](https://github.com/Pineapple4623)

Project Link: [https://github.com/Pineapple4623/blink-news](https://github.com/Pineapple4623/blink-news)