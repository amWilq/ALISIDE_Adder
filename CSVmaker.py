import requests
from bs4 import BeautifulSoup
import json
import os


def TworzenieGlownegoPlikuCSV():
    with open('test.json')as f:
        dataJSON = json.load(f)

    file = open("to_fix.json", "w")
    file = open("to_fix.json", "r+")
    file.truncate(0)
    file.close()

    url = dataJSON['DANE_ALISIDE']["yupoo_link"]
    text = url

    head, sep, tail = text.partition('x.yupoo.com')

    response = requests.get(url)
    data = response.text
    soup = BeautifulSoup(data, 'lxml')

    count = 0
    for link in soup.findAll('a', class_='album__main'):
        with open('to_fix.json', 'a') as ff:

            q = (link.get('href'))
            new_url = head + "x.yupoo.com" + q
            response = requests.get(new_url)
            data = response.text
            soup = BeautifulSoup(data, 'lxml')
            rows1 = (soup.find('span', class_="showalbumheader__gallerytitle"))
            rows = (soup.find('a', rel="nofollow noopener"))
            x = rows1.text

            try:
                v = rows.text
            except Exception as e:
                print(e)
                v = "https://pl.aliexpress.com/"

            count += 1
            content = ({count - 1: ({'LINKS': q, 'NAME': v, 'PHOTOS': x})})

            print(count - 1)

            json.dump(content, ff, indent=2, sort_keys=True)

            WhenStop = (dataJSON["DANE_ALISIDE"]["ileproduktow"])
            if count == int(WhenStop):
                break

    f.close()
    print("Plik csv zawierający linki znajdziesz w " + os.getcwd())


def fix_json():
    f1 = open("to_fix.json", "r")
    f2 = open("DATA.json", "w")

    for line in f1:
        f2.write(line.replace('}{', '  ,'))

    try:
        f1.close()
        os.remove("to_fix.json")
    except Exception as e:
        print(e)


TworzenieGlownegoPlikuCSV()

fix_json()
