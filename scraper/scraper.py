import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urljoin
import re
import time

# ============================================================
# 1. WEBSITE
# ============================================================

base_url = "https://www.nepalhomes.com/"

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/151.0.0.0 Safari/537.36"
    )
}

# ============================================================
# 2. GET HOMEPAGE
# ============================================================

response = requests.get(
    base_url,
    headers=headers,
    timeout=30
)

print("Homepage Status:", response.status_code)

soup = BeautifulSoup(
    response.text,
    "html.parser"
)

# ============================================================
# 3. GET PROPERTY LINKS
# ============================================================

property_links = []

for link in soup.find_all("a", href=True):

    href = link.get("href")

    if href.startswith("/project/"):

        full_url = urljoin(
            base_url,
            href
        )

        if full_url not in property_links:

            property_links.append(
                full_url
            )

print(
    "Property links found:",
    len(property_links)
)

# ============================================================
# 4. SCRAPE PROPERTY DETAILS
# ============================================================

properties = []

for i, property_url in enumerate(
    property_links,
    start=1
):

    print(
        f"Scraping {i}/{len(property_links)}"
    )

    try:

        page = requests.get(
            property_url,
            headers=headers,
            timeout=30
        )

        if page.status_code != 200:

            print(
                "Skipped:",
                page.status_code
            )

            continue

        property_soup = BeautifulSoup(
            page.text,
            "html.parser"
        )

        # Complete visible text
        text = property_soup.get_text(
            " ",
            strip=True
        )

        # ----------------------------------------------------
        # TITLE
        # ----------------------------------------------------

        title = "N/A"

        title_tag = property_soup.find(
            "h1"
        )

        if title_tag:

            title = title_tag.get_text(
                " ",
                strip=True
            )

        elif property_soup.title:

            title = property_soup.title.get_text(
                " ",
                strip=True
            )

        # ----------------------------------------------------
        # PRICE
        # ----------------------------------------------------

        price = "N/A"

        price_patterns = [
            r"Rs\.\s*[\d.,]+\s*(?:Cr|Crore|Lakh|Lac)?",
            r"Rs\s*[\d.,]+\s*(?:Cr|Crore|Lakh|Lac)?",
        ]

        for pattern in price_patterns:

            match = re.search(
                pattern,
                text,
                re.IGNORECASE
            )

            if match:

                price = match.group(
                    0
                )

                break

        # ----------------------------------------------------
        # LOCATION
        # ----------------------------------------------------

        location = "N/A"

        locations = [
            "Kathmandu",
            "Lalitpur",
            "Bhaktapur",
            "Pokhara",
            "Chitwan",
            "Budhanilkantha",
            "Bhaisepati",
            "Tokha",
            "Sunakothi",
            "Dhapakhel",
            "Budhanilkantha"
        ]

        for loc in locations:

            if loc.lower() in text.lower():

                location = loc

                break

        # ----------------------------------------------------
        # BEDROOM
        # ----------------------------------------------------

        bedroom = "N/A"

        bedroom_patterns = [
            r"(\d+)\s*Bedroom",
            r"(\d+)\s*Bedrooms",
            r"Bedroom\s*[:\-]?\s*(\d+)",
            r"Bed\s*[:\-]?\s*(\d+)"
        ]

        for pattern in bedroom_patterns:

            match = re.search(
                pattern,
                text,
                re.IGNORECASE
            )

            if match:

                bedroom = match.group(1)

                break

        # ----------------------------------------------------
        # BATHROOM
        # ----------------------------------------------------

        bathroom = "N/A"

        bathroom_patterns = [
            r"(\d+)\s*Bathroom",
            r"(\d+)\s*Bathrooms",
            r"Bathroom\s*[:\-]?\s*(\d+)",
            r"Bath\s*[:\-]?\s*(\d+)"
        ]

        for pattern in bathroom_patterns:

            match = re.search(
                pattern,
                text,
                re.IGNORECASE
            )

            if match:

                bathroom = match.group(1)

                break

        # ----------------------------------------------------
        # AREA
        # ----------------------------------------------------

        area = "N/A"

        area_patterns = [
            r"([\d,.]+)\s*(?:Sq\.?\s*Ft|Sq\.?\s*Feet)",
            r"([\d,.]+)\s*(?:Aana|Aana[s]?)",
            r"([\d,.]+)\s*(?:Ropani)",
            r"([\d,.]+)\s*(?:Sq\.?\s*M)"
        ]

        for pattern in area_patterns:

            match = re.search(
                pattern,
                text,
                re.IGNORECASE
            )

            if match:

                area = match.group(
                    0
                )

                break

        # ----------------------------------------------------
        # PROPERTY TYPE
        # ----------------------------------------------------

        property_type = "N/A"

        property_types = [
            "House",
            "Apartment",
            "Flat",
            "Land",
            "Office",
            "Shop"
        ]

        for ptype in property_types:

            if ptype.lower() in text.lower():

                property_type = ptype

                break

        # ----------------------------------------------------
        # SAVE
        # ----------------------------------------------------

        properties.append({

            "Title": title,

            "Property_Type": property_type,

            "Price": price,

            "Location": location,

            "Bedroom": bedroom,

            "Bathroom": bathroom,

            "Area": area,

            "URL": property_url

        })

        time.sleep(1)

    except Exception as e:

        print(
            "Error:",
            e
        )


# ============================================================
# 5. DATAFRAME
# ============================================================

df = pd.DataFrame(
    properties
)

print("\n====================================")
print("SCRAPING COMPLETED")
print("====================================")

print(
    "Properties scraped:",
    len(df)
)

print("\nDataset Preview:")

print(
    df.to_string(index=False)
)

# ============================================================
# 6. SAVE CSV
# ============================================================

df.to_csv(
    "scraper/scraped_data.csv",
    index=False,
    encoding="utf-8-sig"
)

print(
    "\nSaved to: scraper/scraped_data.csv"
)