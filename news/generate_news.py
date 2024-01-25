import os
import json
from news.news import News, GPTReporter
import argparse

package_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(package_dir)

def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--url", default="")
    parser.add_argument("-f", "--file", default="")
    parser.add_argument("-s", "--summarize", default=True)
    parser.add_argument("-c", "--config", default="config.json")
    parser.add_argument("-n", "--num_words", default=60)
    args = parser.parse_args()
    return args


def parse_file(file_path):
    """Parse a file of urls into a list of urls"""
    with open(file_path, "r") as f:
        urls_raw = f.read()
        urls = ["http" + a.strip() for a in urls_raw.split("http") if a.strip()]
    return urls

def check_openai_api_key():
    """Check if OpenAI API key is set"""
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        raise Exception(
            "Please set your OPENAI_API_KEY environment variable: export $OPENAI_API_KEY=<your key>"
            "\nOr add it to a .env file in the root directory of this project."
        )
    else:
        return openai_api_key

def main():
    openai_api_key = check_openai_api_key()
    args = parse_args()

    reporter = GPTReporter("LiquidMetalClimate", api_key=openai_api_key)
    if args.file:
        # save collection to file
        episode = input(
            "To save to csv file, please enter an Episode number or press [Enter] to skip.\n"
        )

        for url in parse_file(args.file):
            if url == "\n": continue
            news = News.from_url(url, summarize=False)
            reporter.summarize(news, n_words=args.num_words, collect=True)
            print(news.title)
        
        if episode:
            reporter.export_csv(args.file.replace(".txt", f"_EP{episode}.csv"), episode=episode)

    elif args.url:
        news = News.from_url(args.url, summarize=args.summarize, reporter=reporter)
        print("\n" + news.title)
        print("\n" + news.summary)
        print("\n" + news.url)


def publish():
    args = parse_args()
    assert args.file.endswith(".csv"), "File must be a csv file"

    reporter = GPTReporter("LiquidMetalClimate")
    reporter.export_markdown(csv_path=args.file)


if __name__ == "__main__":
    publish()

