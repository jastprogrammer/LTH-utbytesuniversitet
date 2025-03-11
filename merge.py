import os
import requests as rq
import pandas as pd
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time

# Load the saved CSV files
df_LTH = pd.read_csv("LTH_universities.csv")
df_THE = pd.read_csv("THE_rankings.csv")
names=[]
order =[]
for uni in df_LTH['University']:
    index = df_THE.loc[df_THE["University"] == uni].index
    if not index.empty:
        names.append(uni)
        order.append(int(index[0]))
    else:
        pass

Merge = pd.DataFrame({'University':names, 'Rank': order})
Merge_sorted = Merge.sort_values(by="Rank", ascending=True)
Merge_sorted = Merge_sorted.set_index('Rank')
Merge_sorted.to_csv('merge.sorted.csv', index=False)

print(Merge_sorted.head(25))