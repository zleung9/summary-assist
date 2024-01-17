import requests

# Create a session
s = requests.Session()

# Change the User-Agent to mimic a regular browser
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}
s.headers.update(headers)

# Perform the login and get the session cookies
login_payload = {
    'username': 'your_username',
    'password': 'your_password'
}
login_req = s.post('https://www.example.com/login', data=login_payload)

# Now, use the session to download the page
page_url = 'https://www.reuters.com/business/autos-transportation/nearly-half-new-passenger-cars-eu-electrified-acea-2023-12-20/'
page_req = s.get(page_url)

# The page HTML is in page_req.text
print(page_req.text)