import selenium.webdriver as webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

links = set()
def scrape_website(website):
    print("Launching chrome browser...")

    chrome_driver_path = "./chromedriver.exe"
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=Service(chrome_driver_path), options=options)

    try:
        driver.get(website)
        print("Page loaded...")
        #html = driver.page_source
        #time.sleep(10)

        wait = WebDriverWait(driver, 30)

        # wait.until(
        # EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="product-card"]'))
        # )

        wait.until(
            lambda d: len(
            d.find_elements(By.CSS_SELECTOR, '[data-testid="product-card"]')
        ) >= 25
        )

        html = driver.execute_script("return document.documentElement.outerHTML")

        get_product_links(html, driver)
        return html
    finally:
        driver.quit()

def extract_body_content(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    body_content = soup.body
    if body_content:
        return str(body_content)
    return ""

def clean_body_content(body_content):
    soup = BeautifulSoup(body_content, "html.parser")

    for script_or_style in soup(["script", "style"]):
        script_or_style.extract()

    cleaned_content = soup.get_text(separator="\n")
    cleaned_content = "\n".join(line.strip() for line in cleaned_content.splitlines() if line.strip())
    
    return cleaned_content

def split_dom_content(dom_content, max_length = 6000):
    return [
        dom_content[i : i + max_length] for i in range(0, len(dom_content), max_length)
        ]

def get_product_links(html, driver):
    

    anchor_tags = driver.find_elements(By.TAG_NAME, 'a')

    for a in anchor_tags:
        href = a.get_attribute("href")
        if href and "/product/" in href:
            links.add(href)
            print(href)