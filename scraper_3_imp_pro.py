import os
from bs4 import BeautifulSoup
import cloudscraper
from tools.scraper_1_all_pro import get_bakat_name


def get_imp_html(bakat_name_each):

    # Read the HTML file
    file_path_in = f"data/html_only/{bakat_name_each}_html_only.html"
    with open(file_path_in, "r", encoding="utf-8") as f:
        html_content = f.read()

    # Parse HTML
    soup = BeautifulSoup(html_content, "html.parser")

    # Check for different possible containers

    # Orange
    if soup.find("app-free-max"):
        content = soup.find("app-free-max")
    elif soup.find("app-root"):
        content = soup.find("app-root")
    elif soup.find("div", class_="premier-tariffs-layout"):
        content = soup.find("div", class_="premier-tariffs-layout")
    elif soup.find("div", id="PageContent"):
        content = soup.find("div", id="PageContent")
    elif soup.find("div", id="MainContainer"):
        content = soup.find("div", id="MainContainer")
    
    # Vodafone
    elif soup.find("div", id="main-content"):
        content = soup.find("div", id="main-content")
    elif soup.find("div", class_="vf-main-content"): 
        content = soup.find("div", class_="vf-main-content")
    
    # We
    elif soup.find("div", role="main"):
        content = soup.find("div", role="main") 
    
    # Etisalat
    elif soup.find("main", class_="position-relative"):
        content = soup.find("main", class_="position-relative")


    # Define output file path
    file_path_out = f"data/html_only_imp/{bakat_name_each}_imp_pro.html"

    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(file_path_out), exist_ok=True)

    # Save cleaned HTML to a new file
    with open(file_path_out, "w", encoding="utf-8") as f:
        f.write(str(content))


if __name__ == "__main__":

    # Run the function for different links
    link = [
        "https://shop.orange.eg/ar/tariff-plans/alo",
        "https://www.orange.eg/ar/Tariff-Plans/FREEmax",
        "https://www.orange.eg/ar/Tariff-Plans/kart-el-kebir-bundles",
        "https://www.orange.eg/ar/Tariff-Plans/PREMIER"
    ]

    bakat_name = get_bakat_name(link)

    # Run the function for different links
    for i in range(len(bakat_name)):
        get_imp_html(bakat_name[i])