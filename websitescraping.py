import json
from tools.scraper_1_all_pro import get_bakat_name, get_full_html
from tools.scraper_2_all_pro_html_only import get_specific_html
from tools.scraper_3_imp_pro import get_imp_html
from tools.scraper_4_gemeni_json_gen import get_json_insights
from langchain_core.tools import tool

@tool
def website_scraper(url: str) -> str:
    """
    A tool to scrape websites and extract structured JSON insights.
    """
    # Run the function for different links
    link = [
        url,
    ]

    response = []
    bakat_name = get_bakat_name(link)
    # print(bakat_name)

    # Run the function for different links to get full HTML
    for i in range(len(link)):
        get_full_html(link[i], bakat_name[i])
    
    # Run the function for different links to get specific HTML (with no css or js)
    for i in range(len(bakat_name)):
        get_specific_html(bakat_name[i])
    
    # Run the function for different links to get important HTML only
    for i in range(len(bakat_name)):
        get_imp_html(bakat_name[i])
    
    # Run the function for different links to get full page insights
    for i in range(len(link)):
        result = get_json_insights(bakat_name[i])
        response.append(result)
    return "dataDir : " + json.dumps({"dir": response})
