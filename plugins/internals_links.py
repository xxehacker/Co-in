from crawl4ai import AsyncWebCrawler

async def Internal_links(url):
    internal_links_found = []
    async with AsyncWebCrawler() as crawler:
        try:
            result = await crawler.arun(url=url)
            if result.success:
                internal_links = result.links.get("internal", [])
                print(f"Found {len(internal_links)} internal links.")
                
                if internal_links:
                    keywords = ["about", "services", "history", "contact", "team", "products"]
                    for link in internal_links:
                        href = link.get("href", "")
                        for keyword in keywords:
                            if keyword in href:
                                internal_links_found.append(href) 
                    if not internal_links_found:
                        print("No matching internal links found.")
                else:
                    print("No internal links found.")
            else:
                print("Crawl failed:", result.error_message)
        except Exception as e:
            print("An error occurred:", str(e))
    
    return internal_links_found  

