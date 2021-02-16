def TworzenieGlownegoPlikuCSV():
    import requests
    from bs4 import BeautifulSoup
    import csv
    import json
    import os

    with open('UZUPELNIJ.json')as f:
        data = json.load(f)
    for state in data["DANE"]:
        break
    f = open("bf3_strona.csv", "w", newline="", encoding="utf-8")
    writer = csv.writer(f, delimiter=' ', quoting=csv.QUOTE_MINIMAL)

    url = state['yupoo_link']
    text = url
    WhenStop = state['ileproduktow']

    head, sep, tail = text.partition('x.yupoo.com')
    print("Pobieram zdjecia z strony " + head + "x.yupoo.com")



    response = requests.get(url)
    data = response.text
    soup = BeautifulSoup(data, 'lxml')
    writer.writerow(["LINKS", "NAME", "PHOTOS"])

    row1 = []
    row2 = []
    row3 = []

    for link in soup.findAll('a', class_='album__main'):
        q = (link.get('href'))
        row1.append(q)
    count = 0
    for link in soup.findAll('a', class_='album__main'):
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
        except:
            v = "https://pl.aliexpress.com/"

        row2.append(v)
        row3.append(x)
        print(x)
        count += 1
        if count == int(WhenStop):
            break

    for c in range(len(row3)):
        writer.writerow([row1[c], row2[c], row3[c]])


    f.close()
    print("Plik csv zawierający linki znajdziesz w " + os.getcwd())
    print("Zaczynam pobieranie zdjęć.")
    import subprocess

    print("Uruchamiam PobieranieZdjec.py\n [...]")
    subprocess.Popen("python PobieranieZdjec.py", shell=True)


TworzenieGlownegoPlikuCSV()