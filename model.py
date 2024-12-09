from flask import Flask, render_template, redirect, url_for
import requests
from bs4 import BeautifulSoup
import sqlite3

app = Flask(__name__)


def init_db():
    conn = sqlite3.connect("products.db")
    c = conn.cursor()
    try:
        c.execute("SELECT * FROM jumia")
        c.execute("SELECT * FROM kilimall")
    except:
        c.execute("""create table jumia (name TEXT,brand VARCHAR,discription VAR,price VARCHAR,
          reviews INT,ratings VARCHAR,discount VARCHAR)""")
        c.execute("""create table kilimall (name TEXT,brand VARCHAR,discription VAR,price VARCHAR,
          reviews INT,ratings VARCHAR,discount VARCHAR)""")
    conn.commit()
    conn.close()

    def get_details(search):
        conn = sqlite3.connect("products.db")
        c = conn.cursor()
        jumia = c.execute(
            "SELECT [name],[price] FROM jumia Where [name]=(:uname)", {"uname": search}
        ).fetchall()
        list_jumia = []
        for item in jumia:
            list_jumia.append([item[0], item[1]])

        kilimall = c.execute(
            "SELECT [name],[price] FROM kilimall Where [name]=(:uname)",
            {"uname": search},
        ).fetchall()
        list_kilimall = []
        for item in kilimall:
            list_kilimall.append([item[0], item[1]])

        return list_jumia, list_kilimall


@app.route("/home1")
def home():
    return render_template("home1.html")


@app.route("/Search")
def search():
    def compare():
        name = requests.args.get("name")
        brand = requests.args.get("brand")
        price = requests.args.get("price")
        reviews = requests.args.get("reviews")
        stock = requests.args.get("stock")

        conn = sqlite3.connect("products.db")
        c = conn.cursor()
        jumia = c.execute(
            "SELECT [name],[price] FROM jumia Where [name]=(:uname)", {"uname": search}
        ).fetchall()
        list_jumia = []
        for item in jumia:
            list_jumia.append([item[0], item[1]])

        kilimall = c.execute(
            "SELECT [name],[price] FROM kilimall Where [name]=(:uname)",
            {"uname": search},
        ).fetchall()
        list_kilimall = []
        for item in kilimall:
            list_kilimall.append([item[0], item[1]])

        return list_jumia, list_kilimall

    return render_template("Search.html")

    # return render_template('Search.html')


# @app.route('/Search')
# def redirect_to_Search():
# return redirect(url_for('Search.html'))


if __name__ == "__main__":
    # init_db()
    app.run(debug=True)
