import os
import requests as rq
import pandas as pd
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time

# ---------- LTH University Data Scraping ----------
lth_data_raw = rq.get('https://www.student.lth.se/internationella-moejligheter/utbytesstudier/hit-kan-du-aaka/partneruniversitet-och-naetverk/')
lth_data_bs = bs(lth_data_raw.content, 'html.parser')

lists = lth_data_bs.find_all('div', {'class': 'lth-package-toggle accordion'})
eng = lists[2]
unis_lth = eng.find_all('a', {'class': 'external-link'})

# Extract text from each <a> tag and clean it
unis_lth_texts = [uni.get_text(strip=True) for uni in unis_lth]

# Save to DataFrame
df_LTH = pd.DataFrame({'University': unis_lth_texts})
df_LTH.to_csv("LTH_universities.csv", index=False)  # Save LTH universities

# ---------- THE Rankings Scraping (Only if CSV is Missing) ----------
csv_filename = "THE_rankings.csv"

if os.path.exists(csv_filename):
    print("Loading THE rankings from CSV...")
    df_THE = pd.read_csv(csv_filename)
else:
    print("Scraping THE rankings...")

    # Setup WebDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    # Load the website
    url = "https://www.timeshighereducation.com/world-university-rankings/latest/world-ranking#!/length/-1/sort_by/rank/sort_order/asc/cols/scores"
    driver.get(url)

    # Wait for JavaScript content to load
    time.sleep(5)  # Increase if needed

    # Extract university names
    unis = driver.find_elements(By.CLASS_NAME, "ranking-institution-title")
    uni_names = [uni.text for uni in unis]

    # Store data in Pandas DataFrame
    df_THE = pd.DataFrame({"University": uni_names})
    df_THE.to_csv(csv_filename, index=False)  # Save to CSV
    driver.quit()

# Setup WebDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    # Load the website
    url = "https://www.timeshighereducation.com/world-university-rankings/2025/subject-ranking/engineering#!/length/-1/sort_by/rank/sort_order/asc/cols/scores"
    driver.get(url)

    # Wait for JavaScript content to load
    time.sleep(5)  # Increase if needed

    # Extract university names
    unis = driver.find_elements(By.CLASS_NAME, "ranking-institution-title")
    uni_names = [uni.text for uni in unis]

    # Store data in Pandas DataFrame
    df_THE_ENG = pd.DataFrame({"University": uni_names})
    df_THE_ENG.to_csv('THE_ENG_rankings.csv', index=False)  # Save to CSV
    driver.quit()

