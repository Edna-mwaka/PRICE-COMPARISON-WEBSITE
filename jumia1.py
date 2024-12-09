import requests
from bs4 import BeautifulSoup
import csv


def scrape_jumia(product_name, max_pages=1):
    base_url = "https://www.jumia.co.ke/catalog/?q="
    search_query = product_name.replace(" ", "+")  # Prepare search query
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
    }

    product_data = []

    for page in range(1, max_pages + 1):  # Scrape multiple pages if needed
        url = f"{base_url}{search_query}&page={page}"
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, "html.parser")

        # Find product elements on the current page
        products = soup.find_all("article", class_="prd _fb col c-prd")

        for item in products:
            try:
                name = item.find("h3", class_="name").text.strip()
                price_str = (
                    item.find("div", class_="prc")
                    .text.strip()
                    .replace("KSh", "")
                    .replace(",", "")
                )
                print(f"Raw price string: {price_str}")  # Debug print
                # Convert to integer, taking the first part if there's a range
                price = int(price_str.split()[0])
                link = "https://www.jumia.co.ke" + item.find("a", href=True)["href"]
                rating_tag = item.find("div", class_="stars _s")
                rating = rating_tag.text.strip() if rating_tag else "No Ratings"

                product_data.append(
                    {"Name": name, "Price": price, "Rating": rating, "Link": link}
                )
            except AttributeError as e:
                print(f"AttributeError: {e}")  # Debug print
                continue  # Skip products with missing data
            except ValueError as e:
                print(f"ValueError: {e}")  # Debug print
                continue  # Skip products with invalid price data

    # Save the data to a CSV file
    csv_filename = f"{product_name.replace(' ', '_')}_jumia.csv"
    with open(csv_filename, "w", newline="") as csv_file:
        fieldnames = ["Name", "Price", "Rating", "Link"]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(product_data)

    print(f"Data has been saved to {csv_filename}")
