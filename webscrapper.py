from bs4 import BeautifulSoup
import requests
import random
import pandas
import io


def create_job_search_url(job_title, location, page_num):
    keywords = job_title.strip()
    keywords = keywords.replace(" ","%2B")
    url = f"https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords={keywords}&location={location}&start={page_num}"
    print(url)
    return url

def create_job_description_url(job_id):
    desc_url = f"https://www.linkedin.com/jobs-guest/jobs/api/jobPosting/{job_id}"
    return desc_url


if __name__== '__main__':
    job_title = input("Enter job title: ")
    location = input("Enter location: ")
    page_num = int(input("Enter page number: "))
    job_search_url = create_job_search_url(job_title, location, page_num)
    jobs_list = requests.get(job_search_url)
    job_list_soup = BeautifulSoup(jobs_list.text, "html.parser")
    page_jobs = job_list_soup.find_all("li")
    for job in page_jobs:
        job_div = job.find("div", {"class":"base-card"})
        job_title = job_div.find("h3", {"class":"base-search-card__title"}).get_text()
        job_location = job_div.find("span", {"class":"job-search-card__location"}).get_text()
        company_name = job_div.find("a", {"class":"hidden-nested-link"}).get_text()
        try:
            date_posted_exact = job_div.find("time", {"class":"job-search-card__listdate"}).get("datetime")
        except:
            date_posted_exact = None
        try:
            date_posted_relative = job_div.find("time", {"class":"job-search-card__listdate"}).get_text().strip()
        except:
            date_posted_relative = None    
        job_id = job_div.get("data-entity-urn").split(":")[3]
        job_description_page = requests.get(create_job_description_url(job_id))
        job_dsec_soup = BeautifulSoup(job_description_page.text, "html.parser")

    print(date_posted_exact)
    print(date_posted_relative)