import requests

# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import os


# for x in range (1,51):
# url='https://www.jumia.co.ke/mlp-jumia-official-stores/?page=1#catalog-listing','images'


def imagedown(url, folder):
    try:
        os.mkdir(os.path.join(os.getcwd(), folder))
    except:
        pass
    os.chdir(os.path.join(os.getcwd(), folder))
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    images = soup.find_all("img")

    for image in images:
        name = image["alt"]
        link = image["src"]

        with open(name.replace(" ", "-").replace("/", "") + ".jpg", "wb") as f:
            im = requests.get(link)
            f.write(im.content)
            print("writing:", name)


imagedown("https://www.jumia.co.ke/electronics/?tag=JMALL&sort=rating", "images")
