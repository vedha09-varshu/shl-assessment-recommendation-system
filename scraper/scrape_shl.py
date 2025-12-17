import requests
from bs4 import BeautifulSoup
import csv
import os
import time

BASE_URL = "https://www.shl.com"
CATALOG_URL = "https://www.shl.com/solutions/products/product-catalog/"

OUTPUT_DIR = "data/raw"
OUTPUT_FILE = "shl_assessments.csv"

def get_assessment_links():
    response = requests.get(CATALOG_URL)
    soup = BeautifulSoup(response.text, "html.parser")

    links = set()
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if "individual-test-solutions" in href:
            if href.startswith("/"):
                links.add(BASE_URL + href)
            else:
                links.add(href)

    return list(links)

def scrape_assessment(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    name = soup.find("h1").get_text(strip=True)

    desc_div = soup.find("div", class_="product-description")
    description = desc_div.get_text(strip=True) if desc_div else ""

    return {
        "name": name,
        "url": url,
        "description": description
    }

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    links = get_assessment_links()
    print("🔗 Found links:", len(links))

    rows = []
    for i, link in enumerate(links):
        try:
            data = scrape_assessment(link)
            rows.append(data)
            print(f"{i+1}. Scraped: {data['name']}")
            time.sleep(0.4)
        except Exception as e:
            print("❌ Error:", e)

    output_path = os.path.join(OUTPUT_DIR, OUTPUT_FILE)

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["name", "url", "description"])
        writer.writeheader()
        writer.writerows(rows)

    print(" CSV saved to:", output_path)
    print(" Total assessments:", len(rows))

if __name__ == "__main__":
    main()
