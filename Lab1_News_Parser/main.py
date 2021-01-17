from selenium import webdriver
import time
from selenium.webdriver.chrome.options import Options
import json
from argparse import ArgumentParser
import os


def parse_args():
    parser = ArgumentParser("Scrapper for bbc.com")
    parser.add_argument(
        "--driver-path",
        "-dp",
        type=str,
        default="../../chromedriver",
        help="Path to driver",
    )
    parser.add_argument(
        "--headless",
        action="store_true",
        default=True,
        help="Launch driver in background mode (no gui)",
    )
    parser.add_argument(
        "--save-path",
        "-sp",
        type=str,
        help="Path to the folder for saving the results into",
        default="./",
    )
    parser.add_argument(
        "--min-news",
        "-mn",
        type=int,
        help="Collect N news if possible (we can run out of available page news). The actual number can be bigger as we'll iterate the whole news page",
    )
    parser.add_argument(
        "--topic-indices",
        "-ti",
        nargs="+",
        type=int,
        metavar="N",
        help="Indices of topics to aggregate news from (1-indexed)",
        default=[4, 5, 6, 7, 8, 10, 11],
    )
    return parser.parse_args()


def main():
    args = parse_args()
    options = Options()
    options.headless = args.headless
    options.add_argument("--window-size=1920,1200")
    driver = webdriver.Chrome(options=options, executable_path=args.driver_path)
    driver.get("https://www.bbc.com/news")
    time.sleep(2)
    # Skip pop-up window
    driver.find_element_by_xpath('//*[@id="sign_in"]/div/button').click()
    corpus = {"catalog": []}
    # Iterate over chosen news categories
    for topic_idx in args.topic_indices:  # 12):
        category_corpus = []
        # Find corresponding button in navigation menu
        topic_ref = driver.find_element_by_xpath(
            f'//*[@id="orb-modules"]/header/div[2]/div/div[1]/nav/ul/li[{topic_idx}]'
        )
        category = topic_ref.text
        try:
            topic_ref.find_element_by_tag_name("a").click()
        except:
            time.sleep(1)
            topic_ref.find_element_by_tag_name("a").click()
        topic_url = driver.current_url
        while len(category_corpus) < args.min_news:
            # Find ids of all posts on a page. We can't use news_refs directly as we reload our page
            news_refs = driver.find_elements_by_xpath('//*[contains(@id, "post_")]')
            post_ids = [ref.get_attribute("id") for ref in news_refs]
            for id in post_ids:
                document = {}
                try:
                    # Find the article by id, switch page and find tags and text blocks
                    ref = driver.find_element_by_xpath(f'//*[@id="{id}"]')
                    ref.find_element_by_tag_name("h3").click()
                    tags = driver.find_element_by_css_selector(
                        'section[data-component="tag-list"]'
                    ).find_elements_by_tag_name("li")
                    text_blocks = driver.find_element_by_tag_name(
                        "article"
                    ).find_elements_by_css_selector('div[data-component="text-block"]')
                except:
                    time.sleep(1)
                    if driver.current_url != topic_url:
                        driver.back()
                    continue
                document["article_id"] = driver.current_url
                document["title"] = driver.title.replace(" - BBC News", "")
                document["category"] = category.lower()
                document["tags"] = ",".join([tag.text for tag in tags])
                document["text"] = " ".join([block.text for block in text_blocks])
                print(document)
                driver.back()
                category_corpus.append(document)
            print(topic_url.split("/")[-1])
            # If current page is last (50), break
            if topic_url.split("/")[-1] == "50":
                break
            # Else switch page to the next
            try:
                page_url = driver.find_element_by_xpath(
                    '//*[@id="lx-stream"]/div[2]/div/div[3]/a[1]'
                ).get_attribute("href")
            except:
                page_url = driver.find_element_by_xpath(
                    '//*[@id="lx-stream"]/div[3]/div/div[3]/a[1]'
                ).get_attribute("href")
            driver.get(page_url)
            topic_url = page_url
            time.sleep(2)
        with open(os.path.join(args.save_path, f"{category}.json"), "w") as f:
            json.dump(category_corpus, f)
        corpus["catalog"].extend(category_corpus)
    with open(os.path.join(args.save_path, "corpus.json"), "w") as fp:
        json.dump(corpus, fp, indent=4, sort_keys=True, ensure_ascii=False)


if __name__ == "__main__":
    main()
