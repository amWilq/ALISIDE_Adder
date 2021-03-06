from retrying import retry
import os
import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd
import json

with open('test.json')as f:
    dataJSON = json.load(f)

@retry(stop_max_attempt_number=5)
def TworzeniePlikowTESTY(X):

    try:
        with open((str(X) + 'TESTY.csv'), 'w', newline='') as file:
            writer = csv.writer(file, delimiter=',')
            df = pd.read_csv(os.getcwd() + "\\bf3_strona.csv", sep=' ')
            TEXT = (df['LINKS'][X])

            url = dataJSON['DANE_ALISIDE']["yupoo_link"]
            text = url

            head, sep, tail = text.partition('x.yupoo.com')
            url = head + "x.yupoo.com" + TEXT

            response = requests.get(url, timeout=None)
            data = response.content
            soup = BeautifulSoup(data, 'lxml')
            szukaj = soup.select('.image__landscape')
            writer.writerow([X])
            for x in szukaj:
                q = x['data-src']
                writer.writerow(['https:' + q])
            szukaj = soup.select('.image__portrait')
            for x in szukaj:
                q = x['data-src']
                writer.writerow(['https:' + q])
    except Exception:
        pass


@retry(stop_max_attempt_number=5)
def zdjecia(x):
    import pandas as pd
    import requests
    import os

    try:
        def create_directory(directory):
            if not os.path.exists(directory):
                os.makedirs(directory)

        def download_save(url, folder):
            try:
                create_directory(folder)
                c = requests.Session()
                c.get('https://photo.yupoo.com/')
                c.headers.update({'referer': 'https://photo.yupoo.com/'})
                res = c.get(url, timeout=None)
                with open(f'{folder}/{url.split("/")[-2]}.jpg', 'wb') as f:
                    f.write(res.content)
            except Exception:
                pass

        dfzdj = pd.read_csv(os.getcwd() + '\\' + str(x) + "TESTY.csv")
        licznik = 0
        try:
            for col in dfzdj.columns:

                for url in dfzdj[col].tolist():
                    licznik += 1
                    if str(url).startswith("http"):
                        download_save(url, col)
                print("Pobrano " + str(licznik) + " zdjęć.")

        except Exception:
            pass
        try:
            path = (os.getcwd() + '\\' + col)
            files = os.listdir(path)
            for index, file in enumerate(files):
                os.rename(os.path.join(path, file), os.path.join(path, ''.join([str(index), 'big.jpg'])))
        except Exception:
            pass
    except Exception:
        pass

ilosc_produktow = range(int(dataJSON["DANE_ALISIDE"]["OdKtoregoProduktuDodawac"]),(int(dataJSON["DANE_ALISIDE"]["ileproduktow"])))

for x in ilosc_produktow:
    TworzeniePlikowTESTY(x)
    zdjecia(x)
    try:
        os.remove(str(x) + 'TESTY.csv')
    except Exception:
        pass
