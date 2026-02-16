import requests
from bs4 import BeautifulSoup
import csv
import time

# ---------------------------
# CONFIG
# ---------------------------
URL = "https://books.toscrape.com/"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; EducationalScraper/1.0)"
}
OUTPUT_FILE = "scraped_data.csv"

# ---------------------------
# FETCH HTML
# ---------------------------
def fetch_html(url):
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print("Error fetching page:", e)
        return None

# ---------------------------
# PARSE HTML
# ---------------------------
def parse_html(html):
    return BeautifulSoup(html, "html.parser")

# ---------------------------
# EXTRACT DATA
# ---------------------------
def extract_data(soup):
    data = []

    # Extract books (safe extraction)
    books = soup.find_all("article", class_="product_pod")

    for book in books:
        title = book.h3.a.get("title") if book.h3 and book.h3.a else "N/A"
        link = book.h3.a.get("href") if book.h3 and book.h3.a else "N/A"
        price = book.find("p", class_="price_color")
        price = price.text if price else "N/A"

        availability = book.find("p", class_="instock availability")
        availability = availability.text.strip() if availability else "N/A"

        data.append([title, link, price, availability])

    return data

# ---------------------------
# EXTRACT TABLES (if exist)
# ---------------------------
def extract_tables(soup):
    tables_data = []

    tables = soup.find_all("table")

    for table in tables:
        rows = table.find_all("tr")
        for row in rows:
            cols = row.find_all(["td", "th"])
            cols = [col.text.strip() for col in cols]
            tables_data.append(cols)

    return tables_data

# ---------------------------
# SAVE CSV
# ---------------------------
def save_csv(filename, book_data, table_data):
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        writer.writerow(["TITLE", "LINK", "PRICE", "AVAILABILITY"])
        writer.writerows(book_data)

        writer.writerow([])
        writer.writerow(["TABLE DATA"])

        for row in table_data:
            writer.writerow(row)

# ---------------------------
# MAIN
# ---------------------------
def main():
    print("Fetching page...")
    html = fetch_html(URL)
    if not html:
        return

    print("Parsing HTML...")
    soup = parse_html(html)

    print("Extracting book data...")
    books = extract_data(soup)

    print("Extracting tables...")
    tables = extract_tables(soup)

    print("Saving CSV...")
    save_csv(OUTPUT_FILE, books, tables)

    print("Done! Data saved to", OUTPUT_FILE)

    # Ethical delay
    time.sleep(2)

if __name__ == "__main__":
    main()
