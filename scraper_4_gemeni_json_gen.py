import json
from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain_community.chat_models import ChatDeepSeek
from tools.scraper_1_all_pro import get_bakat_name
import os

def get_json_insights(bakat_name_each):
    
    # Load API key from environment variable
    from dotenv import load_dotenv
    load_dotenv()
    
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY not found in environment variables. Please create a .env file.")
    
    # Step 1 — Initialize the Gemini model
    model = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.2,
        google_api_key=api_key
    )

    # Alternative: DeepSeek
    # model = ChatDeepSeek(
    #     model="deepseek-chat",
    #     temperature=0.2,
    #     api_key=os.getenv("DEEPSEEK_API_KEY")
    # )

    # Step 2 — Load HTML file
    file_path_in = f"data/html_only_imp/{bakat_name_each}_imp_pro.html"
    with open(file_path_in, "r", encoding="utf-8") as file:
        html_content = file.read()

    # Step 3 — Define the prompt for Gemini
    prompt = f"""
    keeping the same language (don't translate arabic words to english and english remains english):

    You are an intelligent web data extractor.

    Convert the following HTML into a **structured, insightful JSON** format.
    Focus on extracting meaningful information, such as:
    - Plan or product names
    - Prices or costs
    - Descriptions, features, and benefits
    - Duration, data, or call limits (if present)
    - Any other relevant insights

    Return only valid JSON. Do not include explanations or markdown formatting.

    HTML:
    {html_content}
    """

    # Step 4 — Generate JSON output
    response = model.invoke(prompt)

    # Step 5 — Clean and parse model output
    raw_output = response.content.strip()

    try:
        data = json.loads(raw_output)
    except json.JSONDecodeError:
        print("⚠️ Cleaning Gemini output...")
        cleaned = raw_output.split("```json")[-1].split("```")[0].strip()
        data = json.loads(cleaned)
        
    # Step 6 — Save to JSON file with timestamp
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path_out = f"data/website_scraped_data_{bakat_name_each}_{timestamp}.json"
    
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(file_path_out), exist_ok=True)
    
    with open(file_path_out, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    return f"✅ Insightful JSON successfully saved as: {file_path_out}"


if __name__ == "__main__":

    # Run the function for different links
    link = [
        "https://www.orange.eg/ar/Tariff-Plans/FREEmax",
        "https://shop.orange.eg/ar/tariff-plans/alo",
        "https://www.orange.eg/ar/Tariff-Plans/kart-el-kebir-bundles",
        "https://www.orange.eg/ar/Tariff-Plans/PREMIER"
    ]

    bakat_name = get_bakat_name(link)
    # print(bakat_name)

    for i in range(len(link)):
        get_json_insights(bakat_name[i])