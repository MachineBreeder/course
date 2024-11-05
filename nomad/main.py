from playwright.sync_api import sync_playwright
import time
from bs4 import BeautifulSoup
import csv

p = sync_playwright().start()

browser = p.chromium.launch(headless=False)

page = browser.new_page()
# page.goto('https://www.wanted.co.kr/')

page.goto("https://www.wanted.co.kr/search?query=flutter&tab=position")

# page.screenshot(path = './screenshot.png')

# time.sleep(3)

# page.click("button.Aside_searchButton__rajGo")

# page.get_by_placeholder("검색어를 입력해 주세요.").fill("flutter")

# time.sleep(3)

# page.keyboard.down("Enter")

# time.sleep(3)

# page.click("a#search_tab_position")

# time.sleep(3)

for i in range(3):
    time.sleep(2)
    page.keyboard.down("End")

content = page.content()

p.stop()

soup = BeautifulSoup(content, "html.parser")

jobs_db = []

jobs = soup.find_all("div", class_="JobCard_container__REty8")

for job in jobs:
    link = f"https://www.wanted.co.kr{job.find('a')['href']}"
    title = job.find("strong", class_="JobCard_title__HBpZf").text
    company_name = job.find("span", class_="JobCard_companyName__N1YrF").text

    location = soup.find_all("button", class_="FilterButton_FilterButton__KYg_P")
    location = location[1].text

    # for l in location:
    #     location = l.text
    #     print(location)

    reward = job.find("span", class_="JobCard_reward__cNlG5").text

    job = {
        "title" : title,
        "company_name" : company_name,
        "location" : location,
        "reward" : reward,
        "link" : link
    }

    jobs_db.append(job)

print("포지션 개수 : ", len(jobs_db))

file = open("job.csv", "w", encoding="utf-8")
writer = csv.writer(file)

writer.writerow(job.keys())

for job in jobs_db:
    writer.writerow(job.values())

file.close()