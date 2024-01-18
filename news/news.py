import json
from newspaper import Article
from newspaper.article import ArticleException
from openai import OpenAI
import pandas as pd

class News:
    def __init__(self):
        self.url = "" # url of news
        self.summary = "" # summary of news
        self.title = "" # title of news
        self.date = "" # date of news
        self.text = "" # full text of the article
        self.tags = "" # tags of the article
        self.category = "" # category of the article

    @property
    def output(self):
        return {
            "Title": self.title,
            "Body": self.summary,
            "Date": self.date,
            "Source": self.url,
            "Topic": self.tags,
            "Category": self.category
        }

    @classmethod
    def from_url(cls, url, summarize=True, reporter:"GPTReporter"=None):
        news = cls()
        news.url = url
        news.fetch_article()
        if summarize:
            if reporter is None:
                raise ValueError("Reporter must be provided if summarize is True")
            reporter.summarize(news)
        return news


    def fetch_article(self):
        article = Article(self.url)
        try:
            article.download()
            article.parse()
        except ArticleException as e:
            self.text = ""
            self.title = "Failed to download article"

        self.text = article.text


class GPTReporter:
    def __init__(self, name, api_key=""):
        self.name = name
        self.client = OpenAI(api_key=api_key)
        self.model = "gpt-3.5-turbo-1106"
        self.format = { "type": "json_object" }
        self.text = ""
        self._response = None
        self._content = None
        self.collection = []

    def messages(self, n_words=60):
        prompt =  [
            {"role": "system", "content": "You are a profssional news report in climate tech. You are specific about numbers, and you are designed to output JSON."},
            {"role": "user", "content": f"Here is a news article about climate tech.\n {self.text}"},
            {"role": "user", "content": f"Please summarize the above text into field: 'title' and 'body'. Title should be 10 words or less. Body should be {n_words} words or less. "},
            {"role": "user", "content": "Add  of the news from the original article if any."},
        ]
        return prompt
    
    def generate_response(self, *args, **kwargs):
        return self.client.chat.completions.create(*args, **kwargs)
    
    def summarize(self, news:News, n_words=60, collect=False):
        """Summarize a news article using GPT API. 
        If collect is True, then the output is appended to the reporter's collection.
        Parameters
        ----------
        news : News
            A news object
        n_words : int
            Number of words to summarize to
        collect : bool
            Whether to collect the output in the reporter's collection
        """
        self.text = news.text
        if self.text == "":
            return
        self._response = self.generate_response(
            model=self.model,
            response_format=self.format,
            seed=42,
            messages=self.messages(n_words=n_words)
        )
        self._content = json.loads(self._response.choices[0].message.content)
        
        news._content = self._content
        news.title = news._content["title"]
        news.summary = news._content["body"]

        if collect:
            self.collection.append(news.output)
    
    def export(self, csv_path, episode=""):
        """Save the reporter's collection to a csv file"""
        assert self.collection, "Collection is empty"
        assert episode, "Episode must be provided"
        df = pd.DataFrame(self.collection)
        df["Episode"] = episode
        df.to_csv(csv_path, index=False)
