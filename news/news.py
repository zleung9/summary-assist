import json
from newspaper import Article
from newspaper.article import ArticleException
from openai import OpenAI
import pandas as pd
from news.prompts import prompt_for_summary

class News:
    """A news article object.
    Attributes:
        url (str): The URL of the news article.
        summary (str): The summary of the news article.
        title (str): The title of the news article.
        date (str): The date of the news article.
        text (str): The full text of the news article.
        tags (str): The tags associated with the news article.
        category (str): The category of the news article.
    """

    def __init__(self):
        self.url = ""  # url of news
        self.summary = ""  # long summary of news
        self.body = ""  # short summary of news
        self.title = ""  # title of news
        self.date = ""  # date of news
        self.text = ""  # full text of the article
        self.tags = ""  # tags of the article
        self.category = ""  # category of the article
        self.country = ""  # country where the news occurred
        self.investors = [] # investors involved in the news
        self.company = ""  # main company the news is about

    @property
    def output(self):
        return {
            "Title": self.title,
            "Body": self.body,
            "Date": self.date,
            "Source": self.url,
            "Topic": self.tags,
            "Category": self.category
        }

    @classmethod
    def from_url(cls, url, summarize=True, reporter: "GPTReporter" = None):
        """Create a news object from a URL.
        Parameters
        ----------
        url : str
            The URL of the news article.
        summarize : bool
            Whether to summarize the article.
        reporter : GPTReporter
            A reporter object to summarize the article.
        
        Returns
        -------
        News
            A news object.
        """
        news = cls()
        news.url = url
        news.fetch_article()
        if summarize:
            if reporter is None:
                raise ValueError("Reporter must be provided if summarize is True")
            reporter.summarize(news)
        return news

    def fetch_article(self):
        """Fetches the article from the specified URL and parses it.

        This method downloads the article content from the URL using the `Article` class,
        and then parses the downloaded content to extract the relevant information.

        If the download or parsing process encounters an exception, the `text` attribute
        of the object will be set to an empty string, and the `title` attribute will be
        set to "Failed to download article".

        After successful download and parsing, the `text` attribute of the object will
        contain the extracted text content of the article.

        Note: Make sure to set the `url` attribute of the object before calling this method.

        """
        article = Article(self.url)
        try:
            article.download()
        except ArticleException as e:
            self.text = ""
            self.title = "Failed to download article"
        else:
            article.parse()
            self.text = article.text
            if not self.text:
                self.title = "Failed to parse article"


class GPTReporter:
    """A reporter object that uses the GPT API to summarize news articles.

    Attributes:
    ----------
    name : str
        The name of the reporter.
    api_key : str, optional
        The API key for accessing the GPT API, by default "".
    client : OpenAI
        The OpenAI client object for making API requests.
    model : str
        The GPT model to use for summarization.
    format : dict
        The format of the response from the GPT API.
    text : str
        The text of the news article to summarize.
    _response : object
        The response object from the GPT API.
    _content : dict
        The content of the response from the GPT API.
    collection : list
        A collection of summarized news articles. The format of each news depends on the News class.

    Methods:
    -------
    messages(n_words=60)
        Generates a list of prompt messages for summarizing a news article.
    generate_response(*args, **kwargs)
        Generates a response using the GPT API.
    summarize(news: News, n_words=60, collect=False)
        Summarizes a news article using the GPT API.
    """

    def __init__(self, name, api_key=""):
        self.name = name
        if api_key:
            self.client = OpenAI(api_key=api_key)
        else:
            self.cilent = None
        self.model = "gpt-3.5-turbo-1106"
        self.format = { "type": "json_object" }
        self.text = ""
        self._response = None
        self._content = None
        self.collection = []
    

    def generate_response(self, text, prompt=None, seed=42):
        """Summarize a news article using GPT API. 
        If collect is True, then the output is appended to the reporter's collection.
        Parameters
        ----------
        text : News
            text of the news article to summarize
        n_words : int
            Number of words to summarize to
        collect : bool
            Whether to collect the output in the reporter's collection
        """
        try:
            prompt = prompt(text)
        except:
            prompt = [{"role": "user", "content": "Summarize the news article."}]
 
        self._response = self.client.chat.completions.create(
            model=self.model,
            response_format=self.format,
            seed=seed,
            messages=prompt
        )
        self._content = json.loads(self._response.choices[0].message.content)
        return self._content


    def summarize(self, news: News, collect=False, seed=42):
        """Summarize a news article using GPT API.
        Parameters
        ----------
        news : News
            The news article to summarize.
        collect : bool
            Whether to collect the output in the reporter's collection.
        """
        if news.text == "":
            return
        # long_summary is a json that has： "title", "summary" and "country"
        self._content = self.generate_response(news.text, prompt_for_summary, seed=seed)
        news.title = self._content["title"]
        news.summary = self._content["summary"]
        news.country = self._content["country"]
        news.body = self._content["body"]
        news.investors = self._content["investors"]
        news.company = self._content["company"]
        # self._content_short = self.generate_response(news.summary, prompt_for_short_summary)
        # news.body = self._content_short
        
        self.text = news.text

        if collect:
            self.collection.append(news.output)


    def export_csv(self, csv_path, episode=""):
            """
            This method converts the reporter's collection into a pandas DataFrame and adds an "Episode" column with the provided episode number. The DataFrame is then saved to the specified csv file.The csv file will have the following columns:
            "Title", "Body", "Date", "Source", "Topic", "Category", "Episode"

            Parameters
            ----------
            csv_path : str
                The path to the csv file where the collection will be saved.
            episode : str, optional
                The episode number associated with the collection. Default is an empty string.

            Raises
            ------
            AssertionError
                If the collection is empty or if the episode is not provided.

            """
            assert self.collection, "Collection is empty"
            assert episode, "Episode must be provided"
            df = pd.DataFrame(self.collection)
            df["Episode"] = episode
            df.to_csv(csv_path, index=False)

    def export_markdown(self, collection:list=[], csv_path:str=""):
        """
        Publishes all the news in markdown format.

        Parameters
        ----------
        collection : list
            A list of dictionaries representing news articles. Default empty and the reporter's collection is used.
            Each dictionary should at least have the following keys:
            - "Title" : str
                The title of the article.
            - "Body" : str
                The body/content of the article.
            - "Source" : str
                The URL/source of the article.
        csv_path : str
            The path to the csv file where the collection is saved by the reporter.export() method.

        Returns
        -------
            str: The generated markdown output containing the formatted news articles.
        """
        if not collection:
            collection = self.collection
            md_path = None
        if csv_path:
            df = pd.read_csv(csv_path)
            collection = df.to_dict(orient="records")
            md_path = csv_path.replace(".csv", ".md")

        markdown_output = ""
        for entry in collection:
            title = entry["Title"].replace("$", "\$")
            body = entry["Body"].replace("$", "\$")
            url = entry["Source"]
            single_output = f"**{title}.** ([_link_]({url}))\n{body}\n\n"
            markdown_output += single_output
        
        if md_path:
            with open(md_path, "w") as f:
                f.write(markdown_output)
        else:
            return markdown_output
