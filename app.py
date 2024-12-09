from flask import Flask, render_template, request, redirect, url_for
import csv
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Read Jumia prices from CSV


def read_jumia_prices_from_csv(search_term):
    jumia_prices = {}
    try:
        with open(f"{search_term}_jumia.csv", "r") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row["Name"] != "" and row["Price"] != "":
                    jumia_prices[row["Name"]] = [
                        row["Price"],
                        row["Rating"],
                        row["Link"],
                    ]
    except FileNotFoundError:
        logging.error(f"File {search_term}_jumia.csv not found.")
    except Exception as e:
        logging.error(f"Error reading {search_term}_jumia.csv: {e}")
    return jumia_prices


# Read Kilimall prices from CSV


def read_kilimall_prices_from_csv(search_term):
    kilimall_prices = {}
    try:
        with open(f"{search_term}_kilimall.csv", "r") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row["Brand"] != "" and row["Price"] != "":
                    kilimall_prices[row["Brand"]] = [
                        row["Price"],
                        row["Rating"],
                        row["Link"],
                    ]
    except FileNotFoundError:
        logging.error(f"File {search_term}_kilimall.csv not found.")
    except Exception as e:
        logging.error(f"Error reading {search_term}_kilimall.csv: {e}")
    return kilimall_prices


@app.route("/")
def home():
    return render_template("home1.html")


@app.route("/home1")
def home1():
    return render_template("home1.html")


@app.route("/search")
def search():
    return render_template("search.html")


@app.route("/display")
def display():
    return render_template("display.html")


@app.route("/search2", methods=["GET"])
def searchs():
    # Get search parameters from URL query string
    name = request.args.get("name")
    price = request.args.get("price")

    if not name or not price:
        return redirect(url_for("search"))

    # Scrape data for the search term
    from kilimall1 import scrape_kilimall
    from jumia1 import scrape_jumia

    try:
        scrape_jumia(name)
        scrape_kilimall(name)
    except Exception as e:
        logging.error(f"Error scraping data: {e}")
        return "Error scraping data", 500

    # Read prices from CSV
    jumia_prices = read_jumia_prices_from_csv(name)
    kilimall_prices = read_kilimall_prices_from_csv(name)

    # Process price range
    try:
        price_range = price.split(",")
        price_min = int(price_range[0].strip())
        price_max = int(price_range[1].strip())
    except ValueError as e:
        logging.error(f"Error processing price range: {e}")
        return "Invalid price range", 400

    # Filter matching products based on price
    try:
        matching_jumia_products = {
            product_name: {
                "Name": product_name,
                "Price": product_details[0],
                "Rating": product_details[1],
                "Link": product_details[2],
            }
            for product_name, product_details in jumia_prices.items()
            if price_min <= int(product_details[0]) <= price_max
        }

        matching_kilimall_products = {
            product_name: {
                "Name": product_name,
                "Price": product_details[0],
                "Rating": product_details[1],
                "Link": product_details[2],
            }
            for product_name, product_details in kilimall_prices.items()
            if price_min <= int(product_details[0]) <= price_max
        }
    except ValueError as e:
        logging.error(f"Error filtering products: {e}")
        return "Error filtering products", 500
    print(matching_jumia_products)
    print(matching_kilimall_products)
    return render_template(
        "display.html",
        jumia_products=matching_jumia_products,
        kilimall_products=matching_kilimall_products,
        search_term=name,
    )


if __name__ == "__main__":
    app.run(debug=True)
