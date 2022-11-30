import os
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By


def open_page(url):
    # open page
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--incognito')
    options.add_argument('--headless')
    driver = webdriver.Chrome("chromedriver", chrome_options=options)

    driver.get("http://www.facebook.com")
    sleep(5)

    driver.find_element(By.ID, "email").send_keys(os.environ['FB_EMAIL'])
    driver.find_element(By.ID, "pass").send_keys(os.environ['FB_PASSWORD'])
    driver.find_element(By.NAME, "login").click()
    sleep(5)
    driver.get(url)
    sleep(5)

    # scroll
    for i in range(10):
        driver.execute_script(f"window.scrollTo(0, {4000 * i})")
        sleep(2)

    content = driver.page_source

    return content


def get_price(pcl):
    return pcl[0].get_text()


def get_link(p):
    return "https://www.facebook.com{}".format(p.parent.parent.parent['href']).split('?')[0]


def check_if_exist(p):
    return len(p.findChild()) > 0 and len(p.findChild().findChild()) > 0 and len(
        p.findChild().findChild().findChild()) > 0 and len(
        p.findChild().findChild().findChild().findChild().findChild()) > 0 and len(
        p.findChild().findChild().findChild().findChild().findChild().findChild()) > 0 and len(
        p.findChild().findChild().findChild().findChild().findChild().findChild().findChild()) > 0 and len(
        p.findChild().findChild().findChild().findChild().findChild().findChild().findChild().findChild()) > 0 and len(
        p.findChild().findChild().findChild().findChild().findChild().findChild().findChild().findChild().findChild()) > 0


def get_image_div(p):
    return (p.findChild().findChild().findChild().findChild().findChild().findChild()
    .findChild().findChild().findChild().findChild().findChild().findChild()
    .findChild().findChild()['src'])


def get_text_div(p):
    return list(
        list(p.findChild().findChild().findChild().findChild().findChild().findChild().findChild())[1])
