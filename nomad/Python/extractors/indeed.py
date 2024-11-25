from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
browser = webdriver.Chrome(options=options)

def get_page_count(keyword):
    base_url = "https://kr.indeed.com/jobs"
    
    browser.get(f"{base_url}?q={keyword}")

    print(f"{base_url}?q={keyword}")

    soup = BeautifulSoup(browser.page_source, "html.parser")
    # role="navigation"
    pagination = soup.find("nav", class_="css-98e656 eu4oa1w0")
    pages = pagination.find_all("div", recursive=False)
    count = len(pages)
    
    if count == 0:
        return 1
    else:
        return - 1
    
def extract_indeed_jobs(keyword):

    base_url = "https://kr.indeed.com/jobs"
    pages = get_page_count(keyword)
    results = []

    for page in range(pages):
        final_url = f"{base_url}?q={keyword}&start={page * 10}"
        
        browser.get(final_url)
        
        soup = BeautifulSoup(browser.page_source, "html.parser")
        
        job_list = soup.find("ul", class_="css-1faftfv")
        
        jobs = job_list.find_all("li", recursive=False)
        
        for job in jobs:
            zone = job.find("div", class_="mosaic")

            if zone is None:
                anchor = job.select_one("h2 a")
                title = anchor["aria-label"]
                
                if title in "�":
                    title = anchor["aria-label"].replace("�","")
                
                link = anchor["href"]
                company = job.find("span", class_="css-1h7lukg eu4oa1w0")
                location = job.find("div", class_="css-1restlb eu4oa1w0")

                job_data = {
                    "link": f"https://kr.indeed.com/{link}",
                    "company": company.string,
                    "location": location.string,
                    "title": title
                }
                results.append(job_data)
                
    return results