"""
Facebook Basic Navigator with LLM Extraction
Navigates, scrolls, expands posts, and extracts structured data
"""
import asyncio
import json
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode, LLMConfig
from crawl4ai.extraction_strategy import LLMExtractionStrategy
from pydantic import BaseModel, Field
from typing import List, Optional
from langchain_core.tools import tool


# Define the data structure for comments
class Comment(BaseModel):
    """Structure for a single comment"""
    author: str = Field(description="Name of the person who commented")
    text: str = Field(description="The comment text content")


# Define the data structure for each Facebook post
class FacebookPost(BaseModel):
    """Structure for a single Facebook post"""
    post_time: Optional[str] = Field(description="When the post was published (e.g., '2 hours ago', 'January 15 at 3:00 PM')")
    content: str = Field(description="The full text content of the post")
    likes_number: Optional[str] = Field(description="Number of likes/reactions (e.g., '1.2K', '450')")
    comments_number: Optional[str] = Field(description="Number of comments (e.g., '234', '45')")
    shares_number: Optional[str] = Field(description="Number of shares (e.g., '3', '10', '25')")
    comments: Optional[List[Comment]] = Field(default=[], description="List of visible comments under the post")


class FacebookPosts(BaseModel):
    """List of Facebook posts"""
    posts: List[FacebookPost] = Field(description="List of all posts found on the page")


async def facebook_basic_scroll(
    page_url="https://www.facebook.com/Telecomegypt",
    scroll_count=5,
    scroll_wait=3,
    headless=False,
    session_dir="./facebook_session_c4a",
    session_id="facebook_c4a_session",
    save_debug_files=True
):
    """
    Simple script: Navigate to Facebook and scroll
    
    Args:
        page_url: Facebook page URL to scrape
        scroll_count: Number of times to scroll
        scroll_wait: Seconds to wait between scrolls
        headless: Run browser in headless mode
        session_dir: Directory for browser session data
        session_id: Session identifier
        save_debug_files: Whether to save debug HTML/markdown files (default: True)
    """
    
    print(f"\n🔍 Facebook Basic Navigator")
    print("=" * 60)
    print(f"📍 URL: {page_url}")
    print(f"📜 Scrolls: {scroll_count}")
    print("=" * 60)
    
    # Configure browser
    browser_config = BrowserConfig(
        headless=headless,
        user_data_dir=session_dir,
        use_persistent_context=True,
        use_managed_browser=True,
        viewport_width=1366,
        viewport_height=768,
        enable_stealth=True,  # Disabled due to import error
        verbose=True
    )
    
    # Incremental scroll script with button clicking at each step
    scroll_script = """
    # Wait for page to load
    WAIT `div[role="main"]` 15
    
    # Initialize tracking variables
    EVAL `
    window.__CLICKED_BUTTONS__ = new Set();
    window.__TOTAL_CLICKS__ = 0;
    window.__SCROLL_STEP__ = 0;
    console.log('🚀 Starting incremental scroll with See More clicking');
    `
    WAIT 5
    
    # Function to find and click See More buttons with tracking
    EVAL `
    window.clickSeeMoreButtons = function(stepNumber) {
        const buttons = document.querySelectorAll('div[role="button"]');
        const seeMoreButtons = [];
        let newButtonsClicked = 0;
        
        // Find all "See More" buttons
        for (let btn of buttons) {
            const text = btn.textContent.trim();
            if (text.includes('See More') || text.includes('See more') || 
                text.includes('عرض المزيد') || text.includes('See More') ||
                text.includes('المزيد') || text.includes('عرض كامل')) {
                
                // Create unique identifier for button
                const rect = btn.getBoundingClientRect();
                const buttonId = text + '_' + Math.round(rect.top) + '_' + Math.round(rect.left);
                
                // Only add if not already clicked
                if (!window.__CLICKED_BUTTONS__.has(buttonId)) {
                    seeMoreButtons.push({btn: btn, id: buttonId});
                }
            }
        }
        
        console.log('📍 Step ' + stepNumber + ': Found ' + seeMoreButtons.length + ' new See More buttons');
        
        // Click new buttons sequentially with visual feedback
        seeMoreButtons.forEach((btnData, index) => {
            setTimeout(() => {
                try {
                    const btn = btnData.btn;
                    const btnId = btnData.id;
                    
                    // Check if button is still visible and clickable
                    const rect = btn.getBoundingClientRect();
                    if (rect.width > 0 && rect.height > 0) {
                        // Add visual feedback
                        btn.style.border = '3px solid orange';
                        btn.style.backgroundColor = 'lightyellow';
                        
                        // Smooth scroll button into view if needed
                        if (rect.top < 100 || rect.top > window.innerHeight - 100) {
                            btn.scrollIntoView({behavior: 'smooth', block: 'center', inline: 'nearest'});
                        }
                        
                        setTimeout(() => {
                            btn.click();
                            window.__CLICKED_BUTTONS__.add(btnId);
                            window.__TOTAL_CLICKS__++;
                            newButtonsClicked++;
                            
                            // Change color after successful click
                            btn.style.border = '3px solid green';
                            btn.style.backgroundColor = 'lightgreen';
                            
                            console.log('✅ Step ' + stepNumber + ': Clicked button ' + (index + 1) + 
                                       '/' + seeMoreButtons.length + ' (Total: ' + window.__TOTAL_CLICKS__ + ')');
                        }, 200);
                        
                    } else {
                        console.log('⚠️ Button not visible, skipping');
                    }
                } catch(e) {
                    console.log('❌ Failed to click button: ' + e.message);
                }
            }, index * 800); // Much slower clicking (800ms between clicks) for maximum reliability
        });
        
        return seeMoreButtons.length;
    };
    `
    WAIT 2
    
    # Initial click on visible buttons before scrolling
    EVAL `
    window.__SCROLL_STEP__ = 0;
    const initialButtons = window.clickSeeMoreButtons(0);
    console.log('🎯 Initial pass: Processing ' + initialButtons + ' buttons');
    `
    WAIT 8
    """
    
    # Generate incremental scroll steps with button clicking
    for i in range(scroll_count):
        scroll_script += f"""
    # === SCROLL STEP {i+1} ===
    
    # Smooth scroll down gradually with JavaScript (slower)
    EVAL `
    (function() {{
        const currentY = window.pageYOffset;
        const targetY = currentY + 400;  // Scroll only 400px at a time (slower)
        
        console.log('📜 Step {i+1}: Smooth scrolling from ' + currentY + ' to ' + targetY);
        
        // Smooth scroll with slower animation
        window.scrollTo({{
            top: targetY,
            behavior: 'smooth'
        }});
        
        // Mark scroll as complete (longer wait for animation)
        setTimeout(() => {{
            console.log('✅ Step {i+1}: Scroll completed at ' + window.pageYOffset);
        }}, 2000);
    }})();
    `
    WAIT {max(5, scroll_wait + 3)}
    
    # Click newly visible "See More" buttons
    EVAL `
    window.__SCROLL_STEP__++;
    const buttonsFound = window.clickSeeMoreButtons(window.__SCROLL_STEP__);
    console.log('📊 Step ' + window.__SCROLL_STEP__ + ' Summary:');
    console.log('  - Buttons found: ' + buttonsFound);
    console.log('  - Total clicked so far: ' + window.__TOTAL_CLICKS__);
    `
    WAIT 7
    """
    
    # Final comprehensive pass and cleanup
    scroll_script += """
    # === FINAL COMPREHENSIVE PASS ===
    
    # Wait for any loading to complete
    WAIT 3
    
    # Final pass to catch any remaining buttons
    EVAL `
    console.log('🔍 Final comprehensive pass...');
    const finalButtons = window.clickSeeMoreButtons('FINAL');
    console.log('📊 FINAL STATISTICS:');
    console.log('  - Final pass buttons: ' + finalButtons);
    console.log('  - Total buttons clicked: ' + window.__TOTAL_CLICKS__);
    console.log('  - Unique button IDs tracked: ' + window.__CLICKED_BUTTONS__.size);
    `
    WAIT 10
    
    # Count total posts for verification
    EVAL `
    (function() {
        const posts = document.querySelectorAll('div[role="article"]');
        const postsWithContent = document.querySelectorAll('div[role="article"] div[data-ad-preview]');
        console.log('� POST STATISTICS:');
        console.log('  - Total posts found: ' + posts.length);
        console.log('  - Posts with content: ' + postsWithContent.length);
        console.log('  - See More buttons clicked: ' + window.__TOTAL_CLICKS__);
        window.__TOTAL_POSTS__ = posts.length;
    })();
    `
    WAIT 2
    
    # Scroll back to top for extraction
    EVAL `
    (function() {
        console.log('📜 Scrolling back to top for content extraction...');
        const currentY = window.pageYOffset;
        console.log('🔝 Starting from position: ' + currentY);
        
        window.scrollTo({ 
            top: 0, 
            behavior: 'smooth' 
        });
        
        // Wait for scroll to complete then verify
        setTimeout(() => {
            console.log('✅ Scrolled to position: ' + window.pageYOffset);
        }, 2000);
    })();
    `
    WAIT 6
    
    # Final wait for content to stabilize
    WAIT 3
    """
    
    # Configure LLM extraction
    print(f"\n🤖 Setting up LLM extraction...")
    
    # Load API key from environment variable
    import os
    from dotenv import load_dotenv
    load_dotenv()
    
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY not found in environment variables. Please create a .env file.")
    
    # DeepSeek - More reliable for structured extraction
    # llm_config = LLMConfig(
    #     provider="deepseek/deepseek-chat",
    #     api_token=os.getenv("DEEPSEEK_API_KEY")
    # )
    
    llm_config = LLMConfig(
        provider="gemini/gemini-2.5-pro",
        api_token=api_key
    )

    # llm_config = LLMConfig(
    #     provider="groq/llama-3.3-70b-versatile",
    #     api_token=os.getenv("GROQ_API_KEY")
    # )
    extraction_strategy = LLMExtractionStrategy(
        llm_config=llm_config,
        schema=FacebookPosts.model_json_schema(),
        extraction_type="schema",
        input_format="markdown",  # Use markdown - has timestamps at the end
        instruction="""
        You are analyzing Facebook posts in MARKDOWN format.
        
        CRITICAL UNDERSTANDING:
        The markdown has posts at the TOP and timestamps scattered at the BOTTOM.
        Posts appear in chronological order: NEWEST first (top) → OLDEST last (bottom).
        Timestamps at bottom are UNORDERED/SCATTERED - you MUST sort them first!
        
        YOUR TASK:
        1. Find all post content blocks (long text paragraphs in Arabic or English)
        2. Find all timestamps at the bottom ("5h", "2d", "September 24 at 2:04 PM", etc.)
        3. SORT timestamps by recency (newest → oldest)
        4. Match sorted timestamps to posts BY POSITION: 1st post → newest timestamp, 2nd post → 2nd newest timestamp, etc.
        
        For EACH post, extract these 6 fields:
        
        1. **post_time**: Match by position AFTER sorting timestamps by recency
           ✓ Timestamp formats: "5h", "2d", "3 weeks ago", "September 24 at 2:04 PM", "13 hours ago"
           ✓ Located at the END of the markdown file but don't include "see more" , "learn more" , "shop now", anything that is not a timestamp
           ✓ SORTING RULES (newest to oldest):
             - "X minutes ago" or "X hours ago" = MOST RECENT (newest)
             - "X days ago" or "Yesterday" = RECENT
             - "X weeks ago" = LESS RECENT  
             - Absolute dates (like "September 20", "Oct 3") = OLDER
             - Compare absolute dates: more recent date = newer
           ✓ After sorting: 1st (newest) timestamp → Post 1 (newest post)
           ✓ Extract EXACTLY as written (no modifications)
           ✓ If you can't match, use null
        
        2. **content**: The main post text (Arabic or English)
           ✓ Long text paragraphs that look like social media posts
           ✓ Usually starts with meaningful content in Arabic or English
           ✓ Do NOT include: "See more", "Learn More", timestamps, page names, comments
           ✓ Get the FULL expanded text
           ✓ Just the actual post message
           ✓ STOP before "All reactions:" - that's where post content ends
        
        3. **likes_number**: Reaction/like count
           ✓ Pattern: "All reactions:\n162 ..." → Extract "162"
           ✓ Pattern: "All reactions:\n322 Mahmoud Sayed, فاطمه ثابت and 320 others" → Extract "322"
           ✓ Look AFTER "All reactions:" line
           ✓ The FIRST number on the next line is the likes count
           ✓ Can be: "170", "1.2K", "450", "322", etc.
           ✓ Extract just the number (with K if present)
        
        4. **comments_number**: Comment count
           ✓ Pattern: "All reactions:\n162 ...\n82\n3" → The SECOND number is comments → "82"
           ✓ Pattern: "All reactions:\n322 ...\n183\n6" → Comments = "183"
           ✓ Look for numbers BETWEEN likes and shares
           ✓ Usually appears as a standalone number after the reactions line
           ✓ Located BEFORE the "Like Comment Share" buttons
           ✓ Extract just the number (with K if present)
           ✓ CAREFUL: Don't confuse with shares (which comes after)
        
        5. **shares_number**: Share count
           ✓ Pattern: "All reactions:\n162 ...\n82\n3" → The THIRD number is shares → "3"
           ✓ Pattern: "All reactions:\n322 ...\n183\n6" → Shares = "6"
           ✓ This is the LAST number before "Like Comment Share" buttons
           ✓ Usually a smaller number than likes/comments
           ✓ Located right BEFORE "Like Comment Share" text
           ✓ Extract just the number
        
        6. **comments**: List of visible comments (array of objects)
           ✓ Look AFTER "Like Comment Share" and "View more comments" sections
           ✓ Pattern for each comment:
             - Author name appears in bold or as a link (e.g., "Osama Elsharkawii", "نجلاء نيل")
             - Comment text follows (e.g., "لوسمحت ممكن رقم خدمة العملاء للنت الارضي")
             - May have "Top fan" badge before author
             - May have "Author" badge if it's from Telecom Egypt
           ✓ Extract as array: [{"author": "Name", "text": "Comment text"}, ...]
           ✓ STOP extracting comments when you see next post (starts with "Telecom Egypt" heading)
           ✓ Ignore: "Reply", timestamps like "2h", "Follow" buttons
           ✓ Maximum 5-10 comments per post (don't extract all, just visible ones)
           ✓ If no comments visible, use empty array []
        
        MATCHING STRATEGY (CRITICAL - SORT FIRST!):
        Step 1: Count posts (by content blocks)
        Step 2: Find timestamps at the bottom
        Step 3: SORT timestamps by recency (newest → oldest):
          - Example unsorted: ["2 days ago", "September 20", "5 hours ago"]
          - Example sorted: ["5 hours ago", "2 days ago", "September 20"]
        Step 4: Match by position AFTER sorting:
          * Post #1 (newest) → Sorted Timestamp #1 (NEWEST)
          * Post #2 → Sorted Timestamp #2 (2nd newest)
          * Post #3 (oldest) → Sorted Timestamp #3 (oldest)
        
        OUTPUT ORDER:
        Return posts in the SAME order as in the markdown (newest first)
        
        EXAMPLE MATCHING:
        If markdown has:
        ```
        [Post content 1 - newest]
        كل ابتسامة طفل...
        
        [Post content 2]  
        مبروك للفائزين...
        
        [Post content 3 - oldest]
        نحن سعداء...
        
        [Timestamps at bottom - UNORDERED/scattered]
        2 days ago
        September 20
        5 hours ago
        ```
        
        First SORT timestamps: ["5 hours ago", "2 days ago", "September 20"]
        Then MATCH:
        Post 1 → "5 hours ago" (newest)
        Post 2 → "2 days ago"
        Post 3 → "September 20" (oldest)
        
        Result:
        ```json
        {
          "posts": [
            {
              "post_time": "5 hours ago",
              "content": "كل ابتسامة طفل...",
              "likes_number": "162",
              "comments_number": "82",
              "shares_number": "3",
              "comments": [
                {
                  "author": "Osama Elsharkawii",
                  "text": "لوسمحت ممكن رقم خدمة العملاء للنت الارضي"
                },
                {
                  "author": "Telecom Egypt",
                  "text": "اهلا وسهلا بحضرتك يا فندم , طرق التواصل معانا من خلال : نقدر نتابع من خلال خدمة الشات..."
                }
              ]
            },
            {
              "post_time": "2 days ago",
              "content": "مبروك للفائزين...",
              "likes_number": "322",
              "comments_number": "183",
              "shares_number": "6",
              "comments": [
                {
                  "author": "نجلاء نيل",
                  "text": "حضرتكم بكام شريحة esim"
                }
              ]
            },
            {
              "post_time": "September 20",
              "content": "نحن سعداء...",
              "likes_number": "378",
              "comments_number": "186",
              "shares_number": "5",
              "comments": []
            }
          ]
        }
        ```
        
        CRITICAL PATTERN RECOGNITION:
        Each post has this structure in markdown:
        ```
        [Post content text here]
        اللي عايز أحسن حاجة بيدور على أصل الحاجة...
        
        All reactions:
        162 فاطمه ثابت, نجلاء نيل and 160 others  ← LIKES = 162
        82                                              ← COMMENTS = 82
        3                                               ← SHARES = 3
        Like
        Comment
        Share
        View more comments  ← Comments section starts here
        
        [Comment 1]
        Osama Elsharkawii · 
        Follow
        لوسمحت ممكن رقم خدمة العملاء للنت الارضي
          * 2h
          * Reply
        
        [Comment 2 - Author reply]
        Author
        Telecom Egypt
        اهلا وسهلا بحضرتك يا فندم...
          * 2h
          * Reply
        
        [Next post starts here]
        ## Telecom Egypt
        ```
        Like
        Comment
        Share
        ```
        
        Return JSON array with all posts in order.
        """,
        apply_chunking=False,  # Disable - we're using CSS selector to filter posts
        verbose=True,
        extra_args={
            "temperature": 0,
        },
        # ✅ Use cleaned HTML (default behavior, but explicit is better)
        # The css_selector in CrawlerRunConfig will pre-filter the HTML
    )
    
    # Configure crawler with LLM extraction
    crawler_config = CrawlerRunConfig(
        page_timeout=90000,
        wait_until="domcontentloaded",
        c4a_script=scroll_script,
        extraction_strategy=extraction_strategy,
        session_id=session_id,
        cache_mode=CacheMode.BYPASS,
        verbose=False,
        # ✅ CRITICAL: Extract only post containers to keep structure
        # Facebook uses data-ad-rendering-role="story_message" for post content
        # ✅ REDUCE HTML SIZE - Remove unnecessary tags (NOT 'a' - has timestamps!)
        excluded_tags=["script", "style", "svg", "path", "form", "blockquote", "button","img","link","meta"],
        exclude_external_links=False,  # Keep links - timestamps are in <a> tags!
        # ✅ Remove comment sections and repetitive elements
        excluded_selector='form[role=presentation], blockquote, [aria-label*=comment], [aria-label*=Write], [aria-label*=View more], [aria-label*=Learn More], [aria-label*=Subscribe]',
    )
    
    # Start crawling
    async with AsyncWebCrawler(config=browser_config) as crawler:
        
        print(f"\n🚀 Opening page...")
        
        try:
            result = await crawler.arun(
                url=page_url,
                session_id=session_id,
                config=crawler_config
            )
            
            current_url = getattr(result, "url", "")
            
            # Check if session expired
            if "login" in current_url.lower():
                print("❌ Redirected to login - session expired!")
                print("💡 Run: python facebook_c4a_login.py")
                return {"success": False, "error": "Session expired"}
            
            print(f"✅ Page loaded!")
            print(f"📍 Current URL: {current_url}")
            
            # Extract structured data with LLM
            print(f"\n🤖 Extracting structured data with LLM...")
            
            # ========================================
            # SAVE ALL FORMATS FOR DEBUGGING (OPTIONAL)
            # ========================================
            if save_debug_files:
                print(f"\n   💾 Saving all formats for analysis...")
                
                # 1. Full Raw HTML
                full_html = getattr(result, 'html', '')
                with open("debug_1_full_html.html", "w", encoding="utf-8") as f:
                    f.write(full_html)
                print(f"      ✅ Saved: debug_1_full_html.html ({len(full_html):,} chars)")
                
                # 2. Cleaned HTML (what gets processed)
                cleaned_html = getattr(result, 'cleaned_html', '')
                with open("debug_2_cleaned_html.html", "w", encoding="utf-8") as f:
                    f.write(cleaned_html)
                print(f"      ✅ Saved: debug_2_cleaned_html.html ({len(cleaned_html):,} chars)")
                
                # 2b. Save EXACTLY what the LLM receives as input
                with open("debug_2b_LLM_EXACT_INPUT.html", "w", encoding="utf-8") as f:
                    f.write("<!-- THIS IS THE EXACT HTML SENT TO THE LLM FOR EXTRACTION -->\n")
                    f.write("<!-- File: debug_2_cleaned_html.html (same content) -->\n")
                    f.write("<!-- The LLM uses this HTML + your instruction to extract data -->\n\n")
                    f.write(cleaned_html)
                print(f"      ⭐ Saved: debug_2b_LLM_EXACT_INPUT.html (EXACT LLM INPUT)")
                
                # 3. Markdown output (if available)
                markdown_obj = getattr(result, 'markdown', None)
                if markdown_obj:
                    # Raw markdown
                    raw_markdown = getattr(markdown_obj, 'raw_markdown', None) or str(markdown_obj)
                    with open("debug_3_raw_markdown.md", "w", encoding="utf-8") as f:
                        f.write(raw_markdown)
                    print(f"      ✅ Saved: debug_3_raw_markdown.md ({len(raw_markdown):,} chars)")
                    
                    # Markdown with citations (if available)
                    markdown_with_citations = getattr(markdown_obj, 'markdown_with_citations', '')
                    if markdown_with_citations:
                        with open("debug_3b_markdown_citations.md", "w", encoding="utf-8") as f:
                            f.write(markdown_with_citations)
                        print(f"      ✅ Saved: debug_3b_markdown_citations.md ({len(markdown_with_citations):,} chars)")
                    
                    # Fit markdown (filtered, if available)
                    fit_markdown = getattr(markdown_obj, 'fit_markdown', '')
                    if fit_markdown:
                        with open("debug_3c_fit_markdown.md", "w", encoding="utf-8") as f:
                            f.write(fit_markdown)
                        print(f"      ✅ Saved: debug_3c_fit_markdown.md ({len(fit_markdown):,} chars)")
                
                # Show HTML size reduction analysis
                full_html_size = len(getattr(result, 'html', ''))
                cleaned_html_size = len(getattr(result, 'cleaned_html', ''))
                print(f"\n   📊 HTML Size Analysis:")
                print(f"      • Full HTML: {full_html_size:,} chars")
                print(f"      • Cleaned HTML (sent to LLM): {cleaned_html_size:,} chars")
                if full_html_size > 0:
                    reduction = 100 - (cleaned_html_size/full_html_size*100)
                    print(f"      • Size reduction: {reduction:.1f}%")
            
            # 4. Extracted content (LLM output)
            extracted_content = getattr(result, 'extracted_content', None)
            if extracted_content:
                # Parse the JSON response
                extracted_data = json.loads(extracted_content)
                
                print(f"\n   ✅ LLM returned data!")
                print(f"   📝 Type: {type(extracted_data)}")
                
                # Save debug files only if requested
                if save_debug_files:
                    # Save raw LLM extraction response
                    with open("extracted_raw_data.json", "w", encoding="utf-8") as f:
                        f.write(extracted_content)
                    print(f"      ✅ Saved: extracted_raw_data.json ({len(extracted_content):,} chars)")
                    
                    # Save formatted/parsed response
                    output_file = "facebook_posts_extracted.json"
                    with open(output_file, 'w', encoding='utf-8') as f:
                        json.dump(extracted_data, f, ensure_ascii=False, indent=2)
                    print(f"      ✅ Saved: {output_file} (formatted)")
                    
                    print(f"\n✅ SUCCESS! All debug files saved!")
                    print(f"\n   📁 Debug files created:")
                    print(f"      1. debug_1_full_html.html          - Complete page HTML")
                    print(f"      2. debug_2_cleaned_html.html       - Cleaned & filtered HTML")
                    print(f"      ⭐ debug_2b_LLM_EXACT_INPUT.html   - EXACT INPUT TO LLM ⭐")
                    print(f"      3. debug_3_raw_markdown.md         - Markdown conversion")
                    print(f"      4. extracted_raw_data.json         - LLM raw output")
                    print(f"      5. {output_file}         - Final formatted result")
                else:
                    output_file = None
                    print(f"   ℹ️  Debug files disabled (save_debug_files=False)")
                
                # Show preview of raw response
                if save_debug_files:
                    print(f"\n   🔍 Raw response preview:")
                    preview = json.dumps(extracted_data, ensure_ascii=False, indent=2)[:500]
                    print(preview)
                
                return {
                    "success": True,
                    "url": current_url,
                    "extracted_data": extracted_data,
                    "output_file": output_file,
                    "result": result
                }
            else:
                print(f"⚠️  No content extracted by LLM")
                return {
                    "success": False,
                    "error": "No content extracted",
                    "url": current_url,
                    "result": result
                }
            
        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()
            
            return {
                "success": False,
                "error": str(e)
            }

@tool
def facebook_scraper_tool(page_url: str) -> str:
    """
    Synchronous wrapper for facebook_basic_scroll to use as a LangChain tool.
    Saves the extracted data to a JSON file AND returns it to the agent.
    
    Args:
        page_url: The Facebook page URL to scrape
    
    Returns:
        JSON string containing the extracted posts data
    """
    try:
        # Run the async function synchronously WITHOUT debug files
        result = asyncio.run(facebook_basic_scroll(
            page_url=page_url,
            scroll_count=20,
            scroll_wait=3,
            headless=False,
            save_debug_files=False  # Don't create debug files
        ))
        
        if result["success"]:
            # Get the extracted data
            extracted_data = result.get('extracted_data', {})
            
            # Save to JSON file with timestamp
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_filename = f"./data/facebook_scraped_data_{timestamp}.json"
            
            with open(output_filename, 'w', encoding='utf-8') as f:
                json.dump(extracted_data, f, ensure_ascii=False, indent=2)
            
            print(f"\n✅ Data saved to: {output_filename}")
            
            # Add file info to the response
            response_data = {
                "success": True,
                "saved_to_file": output_filename,
                "data": extracted_data
            }
            
            # Return the data as JSON string to the agent
            return "data:" + json.dumps(response_data, ensure_ascii=False, indent=2)
        else:
            # Return error as JSON
            error_response = {
                "success": False,
                "error": result.get('error', 'Unknown error')
            }
            return json.dumps(error_response, ensure_ascii=False, indent=2)
    
    except Exception as e:
        # Return exception as JSON
        error_response = {
            "success": False,
            "error": str(e)
        }
        return json.dumps(error_response, ensure_ascii=False, indent=2)


