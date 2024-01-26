# Installation

Clone the git repository to your local computer.
```
>>> git clone git@github.com:zleung9/summary-assist.git
```
Enter the local rerpository and install it in the developer mode. 
```
>>> pip install -e .
```


# API key
Before using this tool. Please set your OPENAI_API_KEY environment variable:
```
>>> export OPENAI_API_KEY=<your_key>
```

# Getting started

### Single mode
Run the command below. 
```
 >>> generate_news -u "Your url for the news page"
 ```
 The rsult will be displayed in terminal as title, body and url.


Example: 
```
>>> generate_news -u https://batteryindustry.tech/enovix-and-group14-announce-collaboration-to-develop-best-in-class-silicon-batteries-2/
```
Output: 
```
Enovix and Group14 Technologies Collaborate on Advanced Silicon Battery

Enovix and Group14 Technologies are collaborating to develop a silicon battery using Group14’s SCC55® for 100% of the anode material within Enovix’s battery architecture. The collaboration aims to advance lithium-ion silicon batteries' performance and efficiency. Enovix’s 100% active silicon batteries provide an increase in capacity of up to 50% compared to devices on the market today, with improvements on its technology roadmap intended to widen the gap.

https://batteryindustry.tech/enovix-and-group14-announce-collaboration-to-develop-best-in-class-silicon-batteries-2/
```

### Batch mode
Create a text file and place all the urls into the file. Each url should occupy one line. Then run the following command. The result will be stored in a csv file with the same name.

Example: 
```
>>> generate_news -f "file_with_urls.txt"
```
Output will be stored in a `file_with_urls.csv` in the same folder.

### publish
Convert the content in the `csv` file into Markdown file and get ready to publish to web.

Example: 
```
>>> publish_news -f "file_with_urls.csv"
```
Output will be stored in a `file_with_urls.md` in the same folder.

Or you could add `-p` flag to publish to Markdown directly:
```
>>> generate_news -f "file_with_urls.txt" -p
```


### Options
type `generate_news -h` for more options.
```
-h, --help            show this help message and exit
-u URL, --url URL     URL of the news article
-f FILE, --file FILE  Path to the file containing a list of URLs
-s SUMMARIZE, --summarize SUMMARIZE
                     Flag indicating whether to summarize the news article. Default is True
-p PUBLISH, --publish PUBLISH
                     Flag indicating whether to publish the news article. Default is False
-n NUM_WORDS, --num_words NUM_WORDS
                     Number of words to include in the summary
```
