import requests, re, json
from parsel import Selector
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys  # per inserire testo in un box di testo
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

import requests, re, json
from parsel import Selector

def scrape_all_authors_from_university(university_name: str):

    params = {
        "view_op": "search_authors",                       # author results
        "mauthors": f'{university_name}',                  # search query
        "hl": "en",                                        # language
        "astart": 0                                        # page number
    }
    # f' : f-Strings: A New and Improved Way to Format Strings in Python [similar to % but more readable]
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.87 Safari/537.36",
    }

    profile_results = []

    profiles_is_present = True
    while profiles_is_present:

        html = requests.get("https://scholar.google.com/citations", params=params, headers=headers, timeout=30)
        select = Selector(html.text)

        print(f"extracting authors at page #{params['astart']}.")

        for profile in select.css(".gs_ai_chpr"):
            name         = profile.css(".gs_ai_name a::text").get()
            link         = f'https://scholar.google.com{profile.css(".gs_ai_name a::attr(href)").get()}'
            affiliations = profile.css(".gs_ai_aff").xpath('normalize-space()').get()
            email        = profile.css(".gs_ai_eml::text").get()
            # cited_by     = re.search(r"\d+", profile.xpath('//div[@class="gs_ai_cby"]').get()).group()  
            interests    = profile.css(".gs_ai_one_int::text").getall()

            profile_results.append({
                "profile_name": name,
                "profile_link": link,
                "profile_affiliations": affiliations,
                "profile_email": email,
                #"profile_city_by_count": cited_by,
                "profile_interests": interests
            })

        # if next page token is present -> update next page token and increment 10 to get the next page
        if select.css("button.gs_btnPR::attr(onclick)").get():
            # https://regex101.com/r/e0mq0C/1
            params["after_author"] = re.search(r"after_author\\x3d(.*)\\x26", select.css("button.gs_btnPR::attr(onclick)").get()).group(1)  # -> XB0HAMS9__8J
            params["astart"] += 10
        else:
            profiles_is_present = False

    return profile_results


auth = scrape_all_authors_from_university(university_name="CollegioCarloAlberto")

DF = pd.DataFrame(auth)
DF

# Extracting links and save alla papers for each affilates

# Extracting links and save alla papers for each affilates

driver     = webdriver.Chrome(service=Service(ChromeDriverManager().install())) # apro una pagina browser
papers_CCA = {}

for row in DF.iterrows():
    link   = row[1][1]
    
    driver.get(link)  # vado sul link del professore associato
    
    wait = WebDriverWait(driver, 1)
    while True:
        # click SHOW MORE
        try:
            element = wait.until(EC.element_to_be_clickable((By.ID, 'gsc_bpf_more')))
            element.click()
        except TimeoutException:
            break
            
    # block    = driver.find_elements(By.XPATH, "//tr[@class = 'gsc_a_tr']") # this contains all the other infos
    papers   = driver.find_elements(By.XPATH,"//a[@class='gsc_a_at']")
    years    = driver.find_elements(By.XPATH, "//span[@class='gsc_a_h gsc_a_hc gs_ibl']")
    subtitle = driver.find_elements(By.XPATH, "//div[@class='gs_gray']")
    
    n_papers = len(papers)    # Number of papers in the GS page
    
    titles   = []             # Where I'll save the right titles
    
    for i in range(n_papers):
        
        if years[i].text == "":
            pass
        
        elif subtitle[i].text == "":
            pass
            
        else:
            titles.append(f"#{i+1} - {papers[i].text}; Published in {years[i].text}.")

    papers_CCA[row[1][0]] = titles 

    
    
driver.quit() # chiudo tutto il browser 
