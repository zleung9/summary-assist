import json
from news.news import News, GPTReporter
import argparse


def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--url", default="")
    parser.add_argument("-f", "--file", default="")
    parser.add_argument("-s", "--summarize", default=True)
    parser.add_argument("-c", "--config", default="config.json")
    args = parser.parse_args()
    return args


def parse_file(file_path):
    """Parse a file of urls into a list of urls"""
    with open(file_path, "r") as f:
        urls_raw = "".join(f.readlines())
        urls = ["http" + a.strip() for a in urls_raw.split("http")]
    return urls


def main():
    args = parse_args()
    with open(args.config, 'r') as json_file:
        config = json.load(json_file)
    reporter = GPTReporter("LiquidMetalClimate", api_key=config["api_key"])

    if args.file:
        news_collection = []
        for url in parse_file(args.file):
            if url == "\n": continue
            news = News.from_url(url, summarize=args.summarize, reporter=reporter)
            print(news.title)
            news_collection.append(f"####\n{news.title}\n\n{news.summary}\n\n{news.url}\n\n")
        with open(args.file, "a") as f:
            f.write("\n\n")
            for entry in news_collection:
                f.write(f"\n{entry}")
    elif args.url:
        news = News.from_url(args.url, summarize=args.summarize, reporter=reporter)
        print("\n" + news.title)
        print("\n" + news.summary)
        print("\n" + news.url)


if __name__ == "__main__":
    main()
    