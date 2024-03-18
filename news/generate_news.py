import os
from news.reporter import News, OpenaiReporter, GeminiReporter
import argparse

package_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(package_dir)

def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--url", default="", help="URL of the news article")
    parser.add_argument("-f", "--file", default="", help="Path to the file containing a list of URLs")
    parser.add_argument("-z", "--summarize", default=True, action="store_true", help="Flag indicating whether to summarize the news article. Default is True")
    parser.add_argument("-b", "--publish", default=False, action="store_true", help="Flag indicating whether to publish the news article. Default is False")
    parser.add_argument("-s", "--seed", default=42, help="Seed for the random number generator. Default is 42.")
    parser.add_argument("-m", "--model", default="openai", help="The model to use for generating the response. Default is openai.")
    parser.add_argument("-p", "--show_prompt", action="store_true", help="Flag indicating whether to show the prompt. Default is False.")
    args = parser.parse_args()
    return args


def parse_file(file_path):
    """Parse a file of urls into a list of urls"""
    with open(file_path, "r") as f:
        urls_raw = f.read()
        urls = ["http" + a.strip() for a in urls_raw.split("http") if a.strip() and not a.startswith("#")]
    return urls


def get_reporter(name, model="openai"):
    if model == "openai":
        return OpenaiReporter(name)
    elif model == "google":
        return GeminiReporter(name)
    else:
        raise ValueError(f"Model {model} not recognized")


def publish():
    args = parse_args()
    assert args.file.endswith(".csv"), "File must be a csv file"
    reporter = get_reporter("LiquidMetalClimate", model=args.model)
    reporter.export_markdown(csv_path=args.file)


def translate():
    args = parse_args()
    assert args.file.endswith(".md"), "File must be a md file"
    reporter = get_reporter("LiquidMetalClimate", model=args.model)
    reporter.translate(md_path=args.file, show_prompt=args.show_prompt)


def generate():
    args = parse_args()
    reporter = get_reporter("LiquidMetalClimate", model=args.model)
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
        reporter.export_notion(episode=int(episode))

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
    generate()
