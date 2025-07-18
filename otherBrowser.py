# This is a basic python program to open a given https:// URL in your default browser
import http.client
from urllib.parse import urlparse
import webbrowser

def fetch_url(url):
    parsed = urlparse(url)
    conn = http.client.HTTPSConnection(parsed.netloc)
    conn.request("GET", parsed.path or "/")
    resp = conn.getresponse()
    data = resp.read().decode()
    print(data[:1000])  # Print first 1000 characters

if __name__ == "__main__":
    url = input("Enter URL (with https://): ")
    webbrowser.open(url)