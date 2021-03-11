import time
import pandas as pd
import os
from selenium.common.exceptions import NoSuchElementException
import json
import subprocess
import shutil
import epnCabinet as epn
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


with open('test.json')as f:
    data = json.load(f)

print("Uruchamiam CSVmaker.py [...]")
subprocess.run("python CSVmaker.py", shell=True)
subprocess.Popen("python PobieranieZdjec.py", shell=True)

url = data['DANE_ALISIDE']["yupoo_link"]
text = url


browser = webdriver.Chrome(os.getcwd() + "\\Chromedriver")
ilosc_produktow = range(int(data["DANE_ALISIDE"]["OdKtoregoProduktuDodawac"]),
                        (int(data["DANE_ALISIDE"]["ileproduktow"])))

df = pd.read_csv(os.getcwd() + "\\bf3_strona.csv", sep=' ')
opis = pd.read_csv(os.getcwd() + "\\opis.csv", sep=' ')
browser.get("https://aliside.com/login")
SzukajXPATH = browser.find_element_by_xpath


def spinner():
    time.sleep(2)
    try:
        SzukajXPATH('/html/body/app-root/app-admin-layout/div/div[3]/app-create-product/div[2]/'
                    'app-product-form/div/div/form/div/div[10]/btn-loading/button/div')
        print("Błąd, czekam.")
        time.sleep(120)
    except NoSuchElementException:
        pass
    finally:
        try:
            SzukajXPATH("/html/body/app-root/app-admin-layout/div/div[3]/app-create-product/div[2]/"
                        "app-product-form/div/div/form/div/div[10]/btn-loading/button").click()
            SzukajXPATH("/html/body/app-root/app-admin-layout/div/div[3]/app-create-product/div[2]/"
                        "app-product-form/div/div/form/div/div[10]/btn-loading/button").click()
        except NoSuchElementException:
            pass


def capttcha():
    try:
        time.sleep(1)
        SzukajXPATH('/html/body/app-root/app-admin-layout/div/div[3]/app-create-product/'
                    'div[2]/app-product-form/div/div/form/div/div[10]/ngx-recaptcha2')
        print('CAPTCHA, ODŚWIEŻAM STORNĘ [..]')
        browser.refresh()
    except NoSuchElementException:
            pass

    while True:
        t = SzukajXPATH('//*[@id="catalogs"]/div/div/tag-input-form/form/input')
        if t.get_attribute("aria-label") == "Wpisz nazwe katalogu":
            break
        else:
            browser.refresh()


def error():
    while True:
        try:
            SzukajXPATH('// *[ @ id = "catalogs"] / div / div / tag - input - form / form / input')
            time.sleep(6)
        except NoSuchElementException:
            break

    while True:
        try:
            SzukajXPATH('/html/body/app-root/app-admin-layout/div/div[3]/app-single-product/div[3]/div')
            time.sleep(6)

        except NoSuchElementException:
            break

    while True:
        try:
            SzukajXPATH('/html/body/app-root/app-admin-layout/div/div[3]/app-single-catalog/app-page-loader/div')
            time.sleep(5)

        except NoSuchElementException:
            break

    while True:
        try:
            SzukajXPATH('/ html / body / app - root / app - admin - layout / div / div[3] /'
                        ' app - single - catalog / app - page - loader / div')
            SzukajXPATH('/ html / body / app - root / app - admin - layout / div / div[3] / '
                        'app - single - catalog / app - page - loader')
            SzukajXPATH('/ html / body / app - root / app - admin - layout / div / div[ 3] / '
                        'app - single - catalog / app - page - loader / div / div')
            time.sleep(5)

        except NoSuchElementException:
            break


def logowanie():
    username_textbox = browser.find_element_by_id("email")
    username_textbox.send_keys((data["DANE_ALISIDE"]['email']))
    pasword_textbox = browser.find_element_by_id("password")
    pasword_textbox.send_keys((data["DANE_ALISIDE"]['haslo']))
    browser.find_element_by_class_name("form-button").click()
    print("Zalogowano poprawnie.")


logowanie()


def przejscie_do_dodawania():
    LinkDoDodawania = (data["DANE_ALISIDE"]['LinkDoDodawania'])
    spinner()
    browser.get(LinkDoDodawania)
    error()
    SzukajXPATH("/html/body/app-root/app-admin-layout/div/div[3]/"
                "app-single-catalog/div[1]/div/div[2]/div/div/div/p").click()


def uzupelnienie_danych(y):

    error()

    grant_type = (data["DANE_EPN"]['grant_type'])
    client_id = (data["DANE_EPN"]['client_id'])
    client_secret = (data["DANE_EPN"]['client_secret'])

    client = epn.init(grant_type=grant_type, client_id=client_id, client_secret=client_secret)

    try:
        client.session()
    except Exception as e:
        print(e)
        return

    api = client.api()

    makeDeeplink = api.post.create_creative(

        link=df['NAME'][y],
        offerId=1,  # AliExpress
        description='Test Deeplink',
        type='deeplink'
    )
    newDeeplink = makeDeeplink['data']['attributes']['code']
    shortDomains = api.get.short_domains()
    allDomains = shortDomains['data']['attributes']
    shortDeeplink = api.post.short_link(
        urlContainer=newDeeplink,
        domainCutter=allDomains[0]  # ali.pub
    )

    for link in shortDeeplink['data']['attributes']:
        LINKISKROCONE = format(link['result'])

    szukaj = browser.find_element

    head, sep, tail = text.partition('x.yupoo.com')
    szukaj(By.ID, "description").send_keys(opis['OPIS'])
    szukaj(By.ID, "note").send_keys(head + "x.yupoo.com" + df['LINKS'][y])
    szukaj(By.ID, "link").send_keys(LINKISKROCONE)
    try:
        szukaj(By.ID, "name").send_keys(df['PHOTOS'][y])
    except NoSuchElementException:
        szukaj(By.ID, "name").send_keys("Uzupełnij tytuł")

    szukaj(By.XPATH, "/html/body/app-root/app-admin-layout/div/div[3]/app-create-product/div[2]/ "
                     "app-product-form/div/div/form/div/div[8]/label[3]/span[1]").click()
    time.sleep(5)


def przechodzenie_do_dodawania_zdj():

    try:
        element_present = EC.presence_of_element_located((By.XPATH, '/html/body/app-root/app-admin-layout/'
                                                                    'div/div[3]/app-single-catalog/div[4]/'
                                                                    'div[1]/app-product-catalog-thumbnail'))
        WebDriverWait(browser, 3).until(element_present)
    except TimeoutException:
        print("Timed out waiting for page to load")
    finally:
        SzukajXPATH('/html/body/app-root/app-admin-layout/div/div[3]/app-single-catalog/div[4]/'
                    'div[1]/app-product-catalog-thumbnail').click()
        print("Przechodzę do dodawania zdjeć.")


def klikniece_dodaj_zdj():
    time.sleep(3)
    SzukajXPATH('/html/body/app-root/app-admin-layout/div/div[3]/app-single-product/div[1]/div/div[2]/div').click()


def dodawanie_zdj(a):
    time.sleep(3)
    z = 0
    for filename in range(50):   # 50 ponieważ jest to maksymalna ilość zdjęć

        z = z+1
        try:
            path = (os.getcwd() + "\\" + str(a) + "\\" + str(z) + "big" + ".jpg")
            SzukajXPATH('/html/body/input').send_keys(path)
        except Exception:
            pass

        try:
            pos = (os.getcwd() + "\\" + str(a - 1))
            shutil.rmtree(pos)
            print("Usunięto folder ze zdjeciami.")
            print("Produkt nr:", [a], "dodano poprawnie.")
        except:
            pass
    time.sleep(35)


def klikniecie_zapisz():

    while True:
        try:
            SzukajXPATH("/html/body/app-root/app-admin-layout/div/div[3]/app-create-product/div[2]/"
                        "app-product-form/div/div/form/div/div[10]/btn-loading/button").click()
            time.sleep(1)
            browser.find_element_by_xpath('/html/body/app-root/app-admin-layout/div/div[3]/app-create-product/'
                                          'div[2]/app-product-form/div/div/form/div/div[10]/btn-loading/button/div')
            print("SPINNER, PONAWIAM PRÓBĘ ZA 5SEK")
            time.sleep(5)

        except NoSuchElementException:
            break

    while True:
        try:
            SzukajXPATH("/html/body/app-root/app-admin-layout/div/div[3]/app-create-product/div[2]/"
                        "app-product-form/div/div/form/div/div[10]/btn-loading/button").click()
            time.sleep(1)
            browser.find_element_by_xpath('//*[@id="toast-container"]')
            print("ZA SZYBKO, PONAWIAM PRÓBĘ ZA 5SEK")
            time.sleep(5)

        except NoSuchElementException:
            break


def pelene_uzupelenie_dachyncj(b):
    error()
    przejscie_do_dodawania()
    error()
    capttcha()
    uzupelnienie_danych(b)
    klikniecie_zapisz()
    error()
    przechodzenie_do_dodawania_zdj()
    error()
    klikniece_dodaj_zdj()
    dodawanie_zdj(b)
    error()


for x in ilosc_produktow:
    pelene_uzupelenie_dachyncj(x)
