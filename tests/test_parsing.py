import pytest

from src.scraping.parser import parse_quotes_page


def test_parse_quotes_page():
    """Test parsing quotes from a sample HTML snippet."""
    html = '''
    <html>
    <body>
        <div class="quote">
            <span class="text">"Test quote"</span>
            <small class="author">Test Author</small>
            <div class="tags">
                <a class="tag">inspirational</a>
                <a class="tag">test</a>
            </div>
            <a href="/author/TestAuthor">Author Link</a>
        </div>
    </body>
    </html>
    '''
    quotes = parse_quotes_page(html, 'https://quotes.toscrape.com')
    assert len(quotes) > 0
    quote = quotes[0]
    assert quote['quote_text'] == 'Test quote'
    assert quote['author_name'] == 'Test Author'
    assert 'inspirational' in quote['tags']
    assert 'test' in quote['tags']
    assert quote['author_url'] == 'https://quotes.toscrape.com/author/TestAuthor'
    assert quote['page_url'] == 'https://quotes.toscrape.com'