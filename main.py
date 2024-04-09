import requests

api = "8218f62e9e79da400690bee6b0dd983cafbba098"
url = f"https://endpoint.apivoid.com/urlrep/v1/pay-as-you-go/?key={api}&url={url1}"

url1 = "https://www.tribuneindia.com"

js = requests.get(url).json()
print(js)
print(js["data"]["report"]["domain_blacklist"]["detections"])
print(js["data"]["report"]["risk_score"]["result"])

need_to_be_true = [
    "is_url_accessible",
    "is_domain_ipv4_assigned",
    "is_domain_ipv4_valid",
]
unknown = []

checks = js["data"]["report"]["security_checks"]

for i in list(checks)[:31]:
    if checks[i] and checks[i] not in need_to_be_true:
        unknown.append(i)
for i in need_to_be_true:
    if not checks[i]:
        unknown.append(i)

print(checks["is_domain_very_recent"])
print(checks["is_domain_recent"])

print(js["data"]["report"]["server_details"]["ip"])

from GoogleNews import GoogleNews

import datetime

import pandas as pd

gn = GoogleNews(lang="en", country="IN")

df = gn.top_news()
# print(df['entries'][0])
# for i in df['entries'][0]:
#     print(i)
print(df["entries"][0]["title_detail"])
print(df["entries"][0]["summary"])


input_query = """
i have two sentences
sentence1 = "modi is visiting drdo"
sentence2 = "modi is visiting brdo"
based on the contextual similarity, is the first statement true based on second statement?, just say yes or no"""

# AIzaSyBG09n_KK433hGBSSZIdEOO2fGqebwBSRo

bard = Bard(token=token)

print(bard.get_answer(input_text=input_query)["content"])
from bs4 import BeautifulSoup

headline = "massive floods in delhi"
url = f"https://www.google.com/search?q={headline}"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.content, "html.parser")
print(soup.prettify())
