'''https://gist.github.com/marcosan93/81514e6b3bad0232de8c8f225f3af74b
https://towardsdatascience.com/how-to-collect-data-from-any-website-cb8fad9e9ec5

soup.findAll("div", class_="feeditemcontent cxfeeditemcontent")

So, If I want to get all div tags of class header <div class="header">
'''
from bs4 import BeautifulSoup as bs
import time
import requests
import random
import os
booksum_cleaned_summaries = ['adambede', 'anneofgreengables', 'alicesadventuresinwonderland']
directory = "/Users/psin/Desktop/cos401/cos401_final_proj/booksum/scripts/finished_summaries/sparknotes/thehouseofthesevengables/"
if not os.path.exists(directory):
    os.mkdir(directory)
book_name = "twg_"
# List of URLs
# 13
urls = [f"https://www.sparknotes.com/lit/sevengables/section{i}/" for i in range(1,12)]
# urls = ["https://www.sparknotes.com/lit/the-westing-game/chapter-summaries/"]

# List for Randomizing our request rate
rate = [i/10 for i in range(10)]
ch_count = -1
# Iterating through the URLS
for url in urls:
    keep_looping_pages = True
    page_num = 1
    # class which contains all summary and analysis text
    # content can span multiple pages, so loop thru page urls
    content = []
    filename = directory + "placeholder.txt"
    while(keep_looping_pages):
        page_url = url + f'page/{page_num}/'
        # Accessing the Webpage
        page = requests.get(page_url)
        if page.status_code != 200:
            keep_looping_pages = False
            continue
        else:
            page_num += 1
        
        # Getting the webpage's content in pure html
        soup = bs(page.content, features="lxml")     

        # main_class = soup.find("div", class_="mainTextContent main-container")
        main_class = soup.find("div", class_="studyGuideText hack-to-hide-first-h2")    

        # remove all block quotes
        try:
            for tag in main_class.find_all("blockquote"):
                tag.extract()
        except:
            print("No block quotes")

        for tag in main_class.findAll(['p', 'h3']):
            # get rid of bold and italics formatting
            formatting = tag.findAll(['em', 'strong'])
            for f_tag in formatting:
                f_tag.unwrap()

            # replace hyperlinks with just the text they were tied to
            a_tags = tag.findAll('a')
            for tag2 in a_tags:
                tag2.replace_with(tag2.text)

            tag_str = str(tag.text)

            # if encounter style tag -- it applies to text above it, so pop
            # the previous item on the list
            # stop when we get to the Analysis section

            if tag.has_attr('style'):
                # print("popped ===", tag_str)
                content.pop()
            elif tag.name == 'h3' and 'Analysis' in tag_str:
                # print("analysis ===", tag_str)
                content.append("REMOVE ANALYSIS")
            elif not tag_str.startswith("Chapters"):
                # print("appended ===", tag_str)
                content.append(tag_str)
            else:
                print("elsed ===", tag_str)

        # Randomizing our request rate  
        time.sleep(random.choice(rate))
    
    idx = 0
    # combine all paragraphs that occur after summary heading, until encounter next section or end of list
    # print("before while loop ===", content)
    while idx < len(content):
        item = content[idx]
        # print("item ===", item)
        if item == "REMOVE ANALYSIS":
            break
        if item.startswith("Summary"):
            # summary_des = item.replace(':', '')
            # summary_des = summary_des.replace(' ', '_')
            summary_des = "section_" + str(ch_count) + "_part_0"
            filename = directory + summary_des + ".txt"
            f = open(filename, "w")
            f.close()
            ch_count += 1
        else:
            f = open(filename, "a")
            f.write(item)
            f.close()
        idx += 1