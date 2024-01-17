### Installation

Clone the git repository to your local computer.
```shell
>>> git clone git@github.com:zleung9/summary-assist.git
```
Enter the local rerpository and install it in the developer mode (for developers)
```shell
>>> pip install -e .
```


### API key
Please add your OpenAI `api_key` in the configuration file: `config.json` located in the root directory.
Example:

```json
{
    "api_key": "xxxxxxxxxxxx"
}
```

#### Getting started

1. Single url mode. Running the command below. The rsult will be displayed in terminal.
   ```shell
    >>> generate_news -u "Your url for the news page"
   ```
2. Batch mode. Create a text file and place all the urls into the file. Each url should occupy one line. Then run the following command. The result will be appended to the url file.
   ```shell
   >>> generate_news -f "Your path to the file containing the urls".
   ```