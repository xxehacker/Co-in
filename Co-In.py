import asyncio
import os
from crawl4ai import AsyncWebCrawler
from crawl4ai.async_configs import BrowserConfig, CrawlerRunConfig
from plugins.internals_links import Internal_links
from core.banner import Banner
from core.colors import Colors
from urllib.parse import urlparse
from core.arguments import parse_arguments
from asyncio import sleep
from datetime import datetime

if not os.path.isdir("output"):
    os.mkdir("output")

markdown_content = []
output_file_name = ""

async def safe_crawl(crawler, link, run_config):
    retries = 3
    for attempt in range(retries):
        try:
            result = await crawler.arun(url=link, config=run_config)
            if result.success:
                return result.markdown
            else:
                print(f"Crawl failed for {link} on attempt {attempt + 1}: {result.error_message}")
        except Exception as e:
            print(f"Error crawling {link} on attempt {attempt + 1}: {e}")
            await sleep(2)
    return None

async def main(url, usersupplied_output_file_name):
    global output_file_name

    if not (url.startswith("http") or url.startswith("https")):
        url = "https://" + url

    links = await Internal_links(url)
    if not links:
        print("No internal links found.")
        return

    parsed_url = urlparse(url)
    domain_name = parsed_url.netloc
    if not usersupplied_output_file_name:
        output_file_name = f"output/{domain_name}.md"
    else:
        output_file_name = f"output/{usersupplied_output_file_name}.md"

    # Markdown Metadata
    markdown_content.append(f"# Information About: [{url}]({url})\n")
    markdown_content.append(f"### Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    markdown_content.append(f"**Total Links Found:** {len(links)}\n")
    markdown_content.append("---\n")

    # Crawler configuration
    run_config = CrawlerRunConfig(
        word_count_threshold=10,
        excluded_tags=["form", "header"],
        exclude_external_links=True,
        process_iframes=False,
        remove_overlay_elements=True,
    )

    browser_config = BrowserConfig(
        headless=True
    )

    try:
        async with AsyncWebCrawler(config=browser_config) as crawler:
            for link in links:
                link = str(link)
                if link.startswith("http") or link.startswith("https"):
                    markdown_content.append(f"## 📌 Information: [{link}]({link})\n")
                    markdown = await safe_crawl(crawler, link, run_config)
                    if markdown:
                        markdown_content.append("<details><summary>View Content</summary>\n\n")
                        markdown_content.append("```markdown\n")
                        markdown_content.append(markdown)
                        markdown_content.append("```\n\n</details>\n")
                        markdown_content.append("---\n")
    except Exception as e:
        print(f"An error occurred: {e}")

    # Save markdown content
    try:
        with open(output_file_name, "w", encoding="utf-8") as f:
            f.write("\n".join(markdown_content))
        print(f"Markdown content saved to {output_file_name}")
    except Exception as e:
        print(f"An error occurred while saving: {e}")

    # Read and print markdown content
    try:
        with open(output_file_name, "r", encoding="utf-8") as f:
            content = f.read()
            print(Colors.GREEN + content + Colors.ENDC)
    except FileNotFoundError:
        print(f"Error: {output_file_name} file not found.")
    except Exception as e:
        print(f"Error reading file: {e}")

if __name__ == "__main__":
    Banner()
    args = parse_arguments()

    if args.url is None:
        print("Please provide a URL.")
        exit()
    else:
        url = args.url

    usersupplied_output_file_name = args.output
    asyncio.run(main(url, usersupplied_output_file_name))