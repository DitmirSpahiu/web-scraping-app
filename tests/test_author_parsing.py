import pytest

from src.scraping.author_parser import parse_author_page


def test_parse_author_page():
    """Test parsing author details from a sample HTML snippet."""
    html = '''
    <html>
    <body>
        <h3 class="author-title">Test Author</h3>
        <p class="author-details">Born: January 1, 2000 in Test City</p>
        <div class="author-description">This is a test description.</div>
    </body>
    </html>
    '''
    data = parse_author_page(html, 'https://quotes.toscrape.com/author/TestAuthor')
    assert data['author_name'] == 'Test Author'
    assert data['author_birth_date'] == 'January 1, 2000'
    assert data['author_birth_location'] == 'Test City'
    assert data['author_description'] == 'This is a test description.'
    assert data['author_url'] == 'https://quotes.toscrape.com/author/TestAuthor'