import cloudscraper
from selenium import webdriver
from urllib.parse import urlparse
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import os


def get_bakat_name(link):
    bakat_name = []
    for i in range(len(link)):
        bakat_name.append(link[i].split("/")[-1])
        if "-" in bakat_name[i]:
            bakat_name[i] = bakat_name[i].replace("-", "_")
    return bakat_name


def get_full_html(link_each, bakat_name):

    # --- Step 1: Create scraper to bypass protection ---
    scraper = cloudscraper.create_scraper(
        browser={"browser": "chrome", "platform": "windows"}
    )

    # Get initial response
    resp = scraper.get(link_each)

    # --- Step 2: Setup Selenium in headless mode ---
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=chrome_options)

    try:
        # --- Step 3: Extract base domain and load it first ---
        parsed = urlparse(link_each)
        base_url = f"{parsed.scheme}://{parsed.netloc}"
        driver.get(base_url)
        time.sleep(2)

        # --- Step 4: Add cookies safely ---
        for cookie in resp.cookies:
            cookie_dict = {
                "name": cookie.name,
                "value": cookie.value
            }
            try:
                driver.add_cookie(cookie_dict)
            except Exception:
                pass  # Ignore invalid cookies

        # --- Step 5: Navigate to target link_each ---
        driver.get(link_each)
        time.sleep(5)

        # --- Step 6: Parse and save full HTML ---
        html_content = driver.page_source
        soup = BeautifulSoup(html_content, "lxml")

        # Define output file path
        file_path_out = f"data/html_all/{bakat_name}_all_pro.html"

        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(file_path_out), exist_ok=True)

        with open(file_path_out, "w", encoding="utf-8") as f:
            f.write(soup.prettify())

        print(f"✅ Full HTML saved to {file_path_out}")
        return soup

    finally:
        driver.quit()


if __name__ == "__main__":

    # Run the function for different links
    link = [
        "https://shop.orange.eg/ar/tariff-plans/alo",
        "https://www.orange.eg/ar/Tariff-Plans/FREEmax",
        "https://www.orange.eg/ar/Tariff-Plans/kart-el-kebir-bundles",
        "https://www.orange.eg/ar/Tariff-Plans/PREMIER"
    ]

    bakat_name = get_bakat_name(link)
    # print(bakat_name)

    for i in range(len(link)):
        get_full_html(link[i], bakat_name[i])