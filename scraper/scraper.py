import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urljoin

# Website
url = "https://www.nepalhomes.com/"

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/151.0.0.0 Safari/537.36"
    )
}

# Request
response = requests.get(
    url,
    headers=headers,
    timeout=30
)

print("Status Code:", response.status_code)

# Parse HTML
soup = BeautifulSoup(response.text, "html.parser")

print("Page Title:", soup.title.get_text(strip=True))

# Store property links
properties = []

for link in soup.find_all("a", href=True):

    href = link.get("href")
    title = link.get_text(" ", strip=True)

    # NepalHomes project/property pages
    if href.startswith("/project/"):

        full_url = urljoin(url, href)

        properties.append({
            "Title": title,
            "URL": full_url
        })

# Remove duplicates
df = pd.DataFrame(properties).drop_duplicates(
    subset="URL"
)

print("\nProperty listings found:", len(df))

print("\nProperty listings:")
print(df.head(20))

# Save
df.to_csv(
    "scraper/scraped_data.csv",
    index=False
)

print("\nData saved to scraper/scraped_data.csv")