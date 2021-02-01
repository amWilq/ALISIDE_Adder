from selenium import webdriver
import time
from selenium.webdriver.common.by import By
import pandas as pd
from admitad import api, items
import os
from selenium.common.exceptions import NoSuchElementException
import json
import subprocess

with open('UZUPELNIJ.json')as f:
    data = json.load(f)
for state in data["DANE"]:
    break

print("Uruchamiam CSVmaker.py\n [...]")
subprocess.run("python CSVmaker.py", shell=True)
print("Uruchamiam PobieranieZdjec.py\n [...]")
subprocess.Popen("python PobieranieZdjec.py", shell=True)

url = state['yupoo_link']
text = url


browser = webdriver.Chrome(os.getcwd() + "\\Chromedriver")
ilosc_produktow = range(0, int((state['ileproduktow'])))
df = pd.read_csv(os.getcwd() + "\\bf3_strona.csv", sep=' ')
opis = pd.read_csv(os.getcwd() + "\\opis.csv", sep=' ')
browser.get("https://aliside.com/login")
SzukajXPATH=browser.find_element_by_xpath

def spinner():
    time.sleep(2)
    try:
        SzukajXPATH('/html/body/app-root/app-admin-layout/div/div[3]/app-create-product/div[2]/app-product-form/div/div/form/div/div[10]/btn-loading/button/div')
        print("Błąd, czekam.")
        time.sleep(120)
    except NoSuchElementException:
        pass
    finally:
        try:
            SzukajXPATH("/html/body/app-root/app-admin-layout/div/div[3]/app-create-product/div[2]/app-product-form/div/div/form/div/div[10]/btn-loading/button").click()
            SzukajXPATH("/html/body/app-root/app-admin-layout/div/div[3]/app-create-product/div[2]/app-product-form/div/div/form/div/div[10]/btn-loading/button").click()
        except:
            pass


def capttcha():
    try:
        SzukajXPATH('/html/body/app-root/app-admin-layout/div/div[3]/app-create-product/div[2]/app-product-form/div/div/form/div/div[10]/ngx-recaptcha2')
        print('UZUPLENIJ CAPTCHE I KLIKNIJ ENTER: ')
    except NoSuchElementException:
            pass


def sprawdzenie_czy_jest_kategoria():
    time.sleep(4)
    try:
        SzukajXPATH('// *[ @ id = "catalogs"] / div / div / tag / div / div / div')

    except NoSuchElementException:
        print("Błąd, czekam.")
        time.sleep(90)
    finally:
        print("Druga próba szukania kategorii")
        SzukajXPATH('// *[ @ id = "catalogs"] / div / div / tag / div / div / div')


def error1():
    time.sleep(4)
    try:
        SzukajXPATH('/html/body/app-root/app-admin-layout/div/div[3]/app-single-product/div[3]/div')
        print("Błąd, czekam.")
        time.sleep(120)
    except NoSuchElementException:
        pass


def error():
    time.sleep(4)
    try:
        SzukajXPATH('/html/body/app-root/app-admin-layout/div/div[3]/app-single-catalog/app-page-loader/div')
        print("Błąd, czekam.")
        time.sleep(120)
    except NoSuchElementException:
        pass


def logowanie():
    username_textbox = browser.find_element_by_id("email")
    username_textbox.send_keys((state['email']))
    pasword_textbox = browser.find_element_by_id("password")
    pasword_textbox.send_keys((state['haslo']))
    browser.find_element_by_class_name("form-button").click()
    print("Zalogowano poprawnie.")


logowanie()


def przejscie_do_dodawania():
    browser.get("https://aliside.com/user/catalogs/1538531b-817f-458f-a33b-03d5b8ef906e")


def uzupelnienie_danych(x):

    client_id = state['client_id']
    client_secret = (state['client_secret'])
    scope = ''.join(set([items.DeeplinksManage.SCOPE]))
    client = api.get_oauth_client_client(
        client_id,
        client_secret,
        scope
    )
    res = client.DeeplinksManage.create(1136372, 6115, ulp=df['NAME'][x], subid='excel')
    szukaj = browser.find_element
    head, sep, tail = text.partition('x.yupoo.com')
    SzukajXPATH("/html/body/app-root/app-admin-layout/div/div[3]/app-single-catalog/div[1]/div/div[2]/div/div/div/p").click()
    szukaj(By.ID, "description").send_keys(opis['OPIS'])
    szukaj(By.ID, "note").send_keys(head + "x.yupoo.com" + df['LINKS'][x])
    szukaj(By.ID, "link").send_keys(res)
    szukaj(By.ID, "name").send_keys(df['PHOTOS'][x])
    szukaj(By.XPATH, "/html/body/app-root/app-admin-layout/div/div[3]/app-create-product/div[2]/app-product-form/div/div/form/div/div[8]/label[3]/span[1]").click()
    time.sleep(5)


def klikniecie_zapisz():
    try:
        SzukajXPATH("/html/body/app-root/app-admin-layout/div/div[3]/app-create-product/div[2]/app-product-form/div/div/form/div/div[10]/btn-loading/button").click()
        print("Zapisano produkt nr: ", [x])
    except:
        pass


def klikniecie_zapisz_prze_captcha():
    try:
        SzukajXPATH("/html/body/app-root/app-admin-layout/div/div[3]/app-create-product/div[2]/app-product-form/div/div/form/div/div[11]/btn-loading/button").click()
        print("Zapisano produkt nr: ", [x])
    except:
        pass


def przechodzenie_do_dodawania_zdj():
    SzukajXPATH('/html/body/app-root/app-admin-layout/div/div[3]/app-single-catalog/div[4]/div[1]/app-product-catalog-thumbnail').click()
    print("Przechodzę do dodawania zdjeć.")


def klikniece_dodaj_zdj():
    time.sleep(3)
    SzukajXPATH('/html/body/app-root/app-admin-layout/div/div[3]/app-single-product/div[1]/div/div[2]/div').click()


def dodawanie_zdj(x):
    time.sleep(3)
    z = 0
    for filename in range(50):

        z = z+1
        try:
            path = (os.getcwd() + "\\"+str(x) + "\\"+str(z)+"big" + ".jpg")
            SzukajXPATH('/html/body/input').send_keys(path)
        except:
            pass
    time.sleep(30)


def pelene_uzupelenie_dachyncj(x):
    error()
    przejscie_do_dodawania()
    error()
    uzupelnienie_danych(x)
    sprawdzenie_czy_jest_kategoria()
    capttcha()
    klikniecie_zapisz()
    klikniecie_zapisz_prze_captcha()
    spinner()
    klikniecie_zapisz()
    error()
    error1()
    przechodzenie_do_dodawania_zdj()
    error()
    error1()
    klikniece_dodaj_zdj()
    dodawanie_zdj(x)
    error()


for x in ilosc_produktow:
    pelene_uzupelenie_dachyncj(x)
