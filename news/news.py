import json
from newspaper import Article
from newspaper.article import ArticleException
from openai import OpenAI
import pandas as pd

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
        self.summary = ""  # summary of news
        self.title = ""  # title of news
        self.date = ""  # date of news
        self.text = ""  # full text of the article
        self.tags = ""  # tags of the article
        self.category = ""  # category of the article

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
            article.parse()
        except ArticleException as e:
            self.text = ""
            self.title = "Failed to download article"

        self.text = article.text


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

    def messages(self, n_words=60):
        """
        Generates a list of prompt messages for summarizing a news article.

        Parameters:
        ----------
        n_words : int
            Number of words to summarize to

        Returns:
        ----------
        list
            A list of prompt messages in the format of dictionaries with 'role' and 'content' keys.
        """
        prompt =  [
            {"role": "system", "content": "You are a professional news reporter in climate tech. You are specific about numbers, and you are designed to output JSON."},
            {"role": "user", "content": f"Here is a news article about climate tech.\n {self.text}"},
            {"role": "user", "content": f"Please summarize the above text into fields: 'title' and 'body'. Title should be 10 words or less. Body should be {n_words} words or less."},
            {"role": "user", "content": "Add any additional information from the original article if any."},
        ]
        return prompt
    
    def generate_response(self, *args, **kwargs):
        """
        Generates a response using the GPT API.

        Parameters:
        ----------
        *args : list
            Positional arguments to pass to the GPT API.
        **kwargs : dict
            Keyword arguments to pass to the GPT API.

        Returns:
        ----------
        object
            The response object from the GPT API.
        """
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
