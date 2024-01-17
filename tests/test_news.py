import sys
sys.path.append('..')
import unittest
from unittest.mock import Mock, patch
from news.news import GPTReporter, News
import json

class TestGPTReporter(unittest.TestCase):
    def setUp(self):
        self.reporter = GPTReporter("LiquidMetalClimate")
        self.news = News()

    @patch('news.news.GPTReporter.generate_response')
    def test_summarize(self, mock_response):
        mock_response.return_value = Mock(choices=[Mock(message=Mock(content='{"title": "Test Title", "body": "Test Body"}'))])
        self.news.text = "Test Text"
        self.reporter.summarize(self.news)
        self.assertEqual(self.news.title, "Test Title")
        self.assertEqual(self.news.summary, "Test Body")

    def test_summarize_empty_text(self):
        self.news.text = ""
        self.reporter.summarize(self.news)
        self.assertEqual(self.news.summary, "")


class TestNews(unittest.TestCase):
    
    def setUp(self):
        self.news = News()
        with open("../config.json", 'r') as json_file:
            config = json.load(json_file)
        self.reporter = GPTReporter("LiquidMetalClimate", api_key=config["api_key"])

    @patch('news.news.News.fetch_article')
    def test_from_url(self, mock_fetch_article):
        self.news = News.from_url(
            "https://www.bbc.com/news/science-environment-56837908",
            summarize=False,
            reporter=self.reporter
        )
        mock_fetch_article.assert_called_once()

if __name__ == '__main__':
    unittest.main()