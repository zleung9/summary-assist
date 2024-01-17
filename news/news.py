import json
from newspaper import Article
from newspaper.article import ArticleException
from openai import OpenAI

class News:
    def __init__(self):
        self.url = "" # url of news
        self.summary = "" # summary of news
        self.title = "" # title of news
        self.date = "" # date of news
        self.text = "" # full text of the article
        self.tags = [] # tags of the article
        self.category = "" # category of the article

    @property
    def output(self):
        return {
            "title": self.title,
            "summary": self.summary,
            "date": self.date,
            "url": self.url,
            "tags": self.tags,
            "category": self.category
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

    @property
    def messages(self):
        prompt =  [
            {"role": "system", "content": "You are a profssional news report in climate tech. You are specific about numbers, and you are designed to output JSON."},
            {"role": "user", "content": f"Here is a news article about climate tech.\n {self.text}"},
            {"role": "user", "content": "Please summarize the above text in the form of title and body. Title should be 10 words or less. Body should be 60 words or less. "},
            {"role": "user", "content": "A of the news from the original article if any."},
        ]
        return prompt
    
    def generate_response(self, *args, **kwargs):
        return self.client.chat.completions.create(*args, **kwargs)
    
    def summarize(self, news:News):
        self.text = news.text
        if self.text == "":
            return
        self._response = self.generate_response(
            model=self.model,
            response_format=self.format,
            seed=42,
            messages=self.messages
        )
        self._content = json.loads(self._response.choices[0].message.content)
        
        news._content = self._content
        news.title = news._content["title"]
        news.summary = news._content["body"]
