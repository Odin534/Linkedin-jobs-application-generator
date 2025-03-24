from bs4 import BeautifulSoup
import requests
import random
import pandas as pd


def create_job_search_url(job_title, location, page_num):
    keywords = job_title.strip()
    keywords = keywords.replace(" ","%2B")
    url = f"https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords={keywords}&location={location}&start={page_num}"
    # print(url)
    return url

def create_job_description_url(job_id):
    desc_url = f"https://www.linkedin.com/jobs-guest/jobs/api/jobPosting/{job_id}"
    return desc_url

def get_job_decription(job_id):
    job_description_page = requests.get(create_job_description_url(job_id))
    if job_description_page.status_code == 200:
        job_dsec_soup = BeautifulSoup(job_description_page.text, "html.parser")   
        job_desc_text = job_dsec_soup.get_text("div", {"class":"show-more-less-html__markup show-more-less-html__markup--clamp-after-5relative overflow-hidden"})
        print(job_desc_text)
        return job_desc_text
    else:
        return None

def createDatabase(job_title, location, page_limit):
    try:
        engine = get_engine("db_user_johnsmith") 
    page_num = 0
    jobs_post_list = []
    while page_num <= page_limit:
        print(page_num)
        job_search_url = create_job_search_url(job_title, location, page_num)
        print(job_search_url)
        jobs_list = requests.get(job_search_url)
        print(jobs_list.status_code)
        if jobs_list.status_code == 200:
            job_list_soup = BeautifulSoup(jobs_list.text, "html.parser")
            page_jobs = job_list_soup.find_all("li")
            for job in page_jobs:
                jobs = {}
                job_div = job.find("div", {"class":"base-card"})
                try:
                    jobs["job_role"] = job_div.find("h3", {"class":"base-search-card__title"}).get_text().strip()
                except:
                    jobs["job_role"] = None
                try:
                    jobs["job_location"] = job_div.find("span", {"class":"job-search-card__location"}).get_text().strip()
                except:
                    jobs["job_location"] = None
                try:
                    jobs["company_name"] = job_div.find("a", {"class":"hidden-nested-link"}).get_text().strip()
                except:
                    jobs["company_name"] = None
                try:
                    jobs["date_posted_exact"] = job_div.find("time", {"class":"job-search-card__listdate"}).get("datetime").strip()
                except:
                    jobs["date_posted_exact"] = None
                try:
                    jobs["date_posted_relative"] = job_div.find("time", {"class":"job-search-card__listdate"}).get_text().strip()
                except:
                    jobs["date_posted_relative"] = None
                try:
                    job_id = job_div.get("data-entity-urn").split(":")[3]
                except:
                    print("ID not available")
                if(job_id):
                    jobs["description"] = get_job_decription(job_id)
                
                # Populate list
                jobs_post_list.append(jobs)
                # End for loop
                break
            page_num = page_num + 1
        else:
            print(f"Reached end of avilabe jobs at page {page_num}")
            break
    # print(jobs_post_list)
    jobs_df = pd.DataFrame(jobs_post_list)
    print(jobs_df.head)

if __name__== '__main__':
    # input section
    # job_title = input("Enter job title: ")
    # location = input("Enter location: ")
    # page_limit = int(input("Enter page limit: "))
    
    # #web scraping section
    # createDatabase(job_title, location, page_limit)
    get_job_decription(4174817695)