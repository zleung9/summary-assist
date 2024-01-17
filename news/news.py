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
    def from_url(cls, url, summarize=True, gpt_client:OpenAI=None):
        news = cls()
        news.url = url
        news.fetch_article()
        if summarize:
            news.summarize(gpt_client)
        return news


    def summarize(self, client:OpenAI):
        if self.text == "":
            self.summary = ""
            return
        self._response = client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            response_format={ "type": "json_object" },
            seed=42,
            messages=[
                {"role": "system", "content": "You are a profssional news report in climate tech. You are specific about numbers, and you are designed to output JSON."},
                {"role": "user", "content": f"Here is a news article about climate tech.\n {self.text}"},
                {"role": "user", "content": "Please summarize the above text in the form of title and body. Title should be 10 words or less. Body should be 60 words or less. "},
                {"role": "user", "content": "A of the news from the original article if any."},
            ]
        )
        self._content = json.loads(self._response.choices[0].message.content)
        self.title = self._content["title"]
        self.summary = self._content["body"]

        return self.output # return the output (a property of the class)


    def fetch_article(self):
        article = Article(self.url)
        try:
            article.download()
            article.parse()
        except ArticleException as e:
            self.text = ""
            self.title = "Failed to download article"

        self.text = article.text