from bs4 import BeautifulSoup
import os
import cloudscraper
from tools.scraper_1_all_pro import get_bakat_name


def get_specific_html(bakat_name_each):
    
    # Read the HTML file
    file_path_in = f"data/html_all/{bakat_name_each}_all_pro.html"
    with open(file_path_in, "r", encoding="utf-8") as f:
        html_content = f.read()

    # Parse HTML
    soup = BeautifulSoup(html_content, "html.parser")

    # --- Remove all <style> tags ---
    for style_tag in soup.find_all('style'):
        style_tag.decompose()

    # Remove all <link> tags that load CSS
    for link_tag in soup.find_all('link', rel='stylesheet'):
        link_tag.decompose()

    # Remove all <script> tags (JS)
    for script_tag in soup.find_all('script'):
        script_tag.decompose()

    # Remove inline CSS from any tag
    for tag in soup.find_all(True, style=True):
        del tag['style']

    # Remove <picture>, <img>, and <svg> tags
    for tag_name in ['picture', 'img', 'svg']:
        for tag in soup.find_all(tag_name):
            tag.decompose()

    # Define output file path
    file_path_out = f"data/html_only/{bakat_name_each}_html_only.html"

    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(file_path_out), exist_ok=True)

    # Save cleaned HTML to a new file
    with open(file_path_out, "w", encoding="utf-8") as f:
        f.write(str(soup))


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
        get_specific_html(bakat_name[i])