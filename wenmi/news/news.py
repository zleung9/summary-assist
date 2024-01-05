import json
from newspaper import Article
from newspaper.article import ArticleException
from openai import OpenAI
import argparse

class News:
    def __init__(self):
        self.url = "" # url of news
        self.summary = "" # summary of news
        self.title = "" # title of news
        self.date = "" # date of news
        self.text = "" # full text of the article
        self.tags = [] # tags of the article
        self.category = "" # category of the article


    @classmethod
    def from_url(cls, url, summarize=True, gpt_client=None):
        news = cls()
        news.url = url
        news.fetch_article()
        if summarize:
            news.summarize(gpt_client)
        return news


    def summarize(self, client):
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
                {"role": "user", "content": "Please summarize the above text in the form of title and body. Title should be 10 words or less. Body should be 60 words or less. "}
            ]
        )
        self._content = json.loads(self._response.choices[0].message.content)
        self.title = self._content["title"]
        self.summary = self._content["body"]


    def fetch_article(self):
        article = Article(self.url)
        try:
            article.download()
            article.parse()
        except ArticleException as e:
            self.text = ""
            self.title = "Failed to download article"

        self.text = article.text


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--url", default="")
    parser.add_argument("-f", "--file", default="")
    parser.add_argument("-s", "--summarize", default=True)
    parser.add_argument("-c", "--config", default="config.json")
    args = parser.parse_args()
    return args


def parse_file(file_path):
    with open(file_path, "r") as f:
        urls_raw = "".join(f.readlines())
        urls = ["http" + a.strip() for a in urls_raw.split("http")]
    return urls





if __name__ == "__main__":
    
    args = parse_args()
    with open(args.config, 'r') as json_file:
        config = json.load(json_file)
    
    client = OpenAI(api_key=config["api_key"])

    if args.file:
        collection = []
        for url in parse_file(args.file):
            if url == "\n": continue
            news = News.from_url(url, summarize=args.summarize, gpt_client=client)
            print(news.title)
            collection.append(f"####\n{news.title}\n\n{news.summary}\n\n{news.url}\n\n")
        with open(args.file, "a") as f:
            f.write("\n\n")
            for entry in collection:
                f.write(f"\n{entry}")
    elif args.url:
        news = News.from_url(args.url, summarize=args.summarize, gpt_client=client)
        print("\n" + news.title)
        print("\n" + news.summary)
        print("\n" + news.url)