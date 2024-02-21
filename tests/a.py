from selenium import webdriver
from newspaper import Article
from newspaper import Config

# Path to your webdriver (replace with your path)
webdriver_path = '/path/to/your/webdriver'

# Create a new instance of the Firefox driver
driver = webdriver.Firefox(executable_path=webdriver_path)

url = "https://www.mining.com/web/eu-trade-chief-to-press-on-with-us-battery-minerals-talks-despite-differences/"

# Go to the URL
driver.get(url)

# Get the HTML of the page
html = driver.page_source

# Now you can use 'newspaper' to parse the HTML
article = Article(url)
article.set_html(html)
article.parse()

# Don't forget to close the driver
driver.quit()