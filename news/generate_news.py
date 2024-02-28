import os
from news.reporter import News, GPTReporter
import argparse

package_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(package_dir)

def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--url", default="", help="URL of the news article")
    parser.add_argument("-f", "--file", default="", help="Path to the file containing a list of URLs")
    parser.add_argument("-z", "--summarize", default=True, action="store_true", help="Flag indicating whether to summarize the news article. Default is True")
    parser.add_argument("-p", "--publish", default=False, action="store_true", help="Flag indicating whether to publish the news article. Default is False")
    parser.add_argument("-s", "--seed", default=42, help="Seed for the random number generator. Default is 42.")
    parser.add_argument("-t", "--test", default=False, action="store_true", help="Wether to update test database. Default is False")
    args = parser.parse_args()
    return args


def parse_file(file_path):
    """Parse a file of urls into a list of urls"""
    with open(file_path, "r") as f:
        urls_raw = f.read()
        urls = ["http" + a.strip() for a in urls_raw.split("http") if a.strip() and not a.startswith("#")]
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



def publish():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", default="", help="Path to the generated csv file.")
    args = parser.parse_args()
    assert args.file.endswith(".csv"), "File must be a csv file"

    reporter = GPTReporter("LiquidMetalClimate")
    reporter.export_markdown(csv_path=args.file)

def translate():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", default="", help="Path to the generated md file.")
    args = parser.parse_args()
    assert args.file.endswith(".md"), "File must be a md file"
    
    reporter = GPTReporter("LiquidMetalClimate", api_key=check_openai_api_key())
    reporter.translate(md_path=args.file)


def main():
    openai_api_key = check_openai_api_key()
    args = parse_args()

    reporter = GPTReporter("LiquidMetalClimate", api_key=openai_api_key)
    if args.file:
        # save collection to file
        episode = input(
            "Please enter an Episode number or press [Enter] to skip.\n"
        )

        for url in parse_file(args.file):
            if url == "\n": continue
            news = News.from_url(url, summarize=False)
            reporter.summarize(news, collect=True)
            print(news.title)
        
        suffix = f"_EP{episode}" if episode else ""
        file_name = args.file.replace(".txt", f"{suffix}.csv")
        reporter.export_csv(file_name, episode=int(episode))
        reporter.export_notion(episode=int(episode), test=args.test)

        if args.publish:
            reporter.export_markdown(csv_path=file_name)

    elif args.url:
        news = News.from_url(args.url, summarize=args.summarize, reporter=reporter)
        # reporter.generate_response(news.text)
        print(f"\nTitle: {news.title}")
        print(f"\nDate: {news.date}")
        print(f"\nCompany: {news.company}")
        print(f"\nInvestors: {news.investors}")
        print(f"\nBody: {news.body}")
        print(f"\nSummary:{news.summary}")
        print(f"\nCountry: {news.country}")
        print(f"\nURL: {news.url}")

if __name__ == "__main__":
    main()
