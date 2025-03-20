from bs4 import BeautifulSoup
import requests
import random
import pandas as pd
import io


def create_job_search_url(job_title, location, page_num):
    keywords = job_title.strip()
    keywords = keywords.replace(" ","%2B")
    url = f"https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords={keywords}&location={location}&start={page_num}"
    # print(url)
    return url

def create_job_description_url(job_id):
    desc_url = f"https://www.linkedin.com/jobs-guest/jobs/api/jobPosting/{job_id}"
    return desc_url


if __name__== '__main__':

    # input section
    job_title = input("Enter job title: ")
    location = input("Enter location: ")
    page_limit = int(input("Enter page limit: "))

    #web scraping section
    page_num = 0
    jobs_post_list = []
    while page_num <= page_limit:
        print(page_num)
        job_search_url = create_job_search_url(job_title, location, page_num)
        print(job_search_url)
        jobs_list = requests.get(job_search_url)
        if jobs_list is not None:
            
            job_list_soup = BeautifulSoup(jobs_list.text, "html.parser")
            page_jobs = job_list_soup.find_all("li")
            for job in page_jobs:
                jobs = {}
                job_div = job.find("div", {"class":"base-card"})
                jobs["job_role"] = job_div.find("h3", {"class":"base-search-card__title"}).get_text().strip()
                jobs["job_location"] = job_div.find("span", {"class":"job-search-card__location"}).get_text().strip()
                jobs["company_name"] = job_div.find("a", {"class":"hidden-nested-link"}).get_text().strip()
                try:
                    jobs["date_posted_exact"] = job_div.find("time", {"class":"job-search-card__listdate"}).get("datetime").strip()
                except:
                    jobs["date_posted_exact"] = None
                try:
                    jobs["date_posted_relative"] = job_div.find("time", {"class":"job-search-card__listdate"}).get_text().strip()
                except:
                    jobs["date_posted_relative"] = None    
                # job_id = job_div.get("data-entity-urn").split(":")[3]
                # job_description_page = requests.get(create_job_description_url(job_id))
                # job_dsec_soup = BeautifulSoup(job_description_page.text, "html.parser")
                jobs_post_list.append(jobs)
            page_num = page_num + 1
    print(jobs_post_list)
    jobs_df = pd.DataFrame(jobs_post_list)
    print(jobs_df.head)