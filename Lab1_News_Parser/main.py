from selenium import webdriver
import time
from selenium.webdriver.chrome.options import Options
import json

options = Options()
options.headless = True
options.add_argument("--window-size=1920,1200")
driver = webdriver.Chrome(options=options, executable_path="../../chromedriver")
driver.get("https://www.bbc.com/news")
time.sleep(2)
driver.find_element_by_xpath('//*[@id="sign_in"]/div/button').click()
corpus = {"catalog": []}
for topic_idx in [4, 5, 6, 7, 8, 10, 11]:  # 12):
    category_corpus = []
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
    while len(category_corpus) < 1000:
        news_refs = driver.find_elements_by_xpath('//*[contains(@id, "post_")]')
        post_ids = [ref.get_attribute("id") for ref in news_refs]
        for id in post_ids:
            document = {}
            try:
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
        if topic_url.split("/")[-1] == "50":
            break
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
    with open(f"{category}.json", "w") as f:
        json.dump(category_corpus, f)
    corpus["catalog"].extend(category_corpus)
with open("corpus.json", "w") as fp:
    json.dump(corpus, fp, indent=4, sort_keys=True, ensure_ascii=False)
