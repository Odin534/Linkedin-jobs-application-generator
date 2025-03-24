from bs4 import BeautifulSoup
import requests
import random
import pandas as pd
from jobs_db_handler import JobsDBHandler
import time 

class WebScrapper:
    def __init__(self, job_title:str, location:str, page_limit:int):    
        self.job_title = job_title
        self.location = location
        self.page_limit = page_limit



    def create_job_search_url(self, job_title, location, page_num):
        keywords = job_title.strip()
        keywords = keywords.replace(" ","%2B")
        url = f"https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords={keywords}&location={location}&start={page_num}"
        # print(url)
        return url

    def create_job_description_url(self,job_id):
        desc_url = f"https://www.linkedin.com/jobs-guest/jobs/api/jobPosting/{job_id}"
        print(desc_url)
        return desc_url

    def get_job_decription(self,job_id):
        job_description_page = requests.get(self.create_job_description_url(job_id))
        if job_description_page.status_code == 200:
            job_dsec_soup = BeautifulSoup(job_description_page.text, "html.parser")   
            job_desc_text = job_dsec_soup.get_text("div", {"class":"show-more-less-html__markup show-more-less-html__markup--clamp-after-5relative overflow-hidden"})
            # print(job_desc_text)
            return job_desc_text
        else:
            return None

    def createDatabase(self,job_title, location, page_limit):
        page_num = 0
        db_handler = JobsDBHandler(job_title)
        processed_ids = set()  # Track already processed job IDs

        while page_num <= page_limit:
            print(f"Inside while loop for page number: {page_num}")
            job_search_url = self.create_job_search_url(job_title, location, page_num)
            print(job_search_url)
            jobs_list = requests.get(job_search_url)
            print(f"Before if condition, status code = {jobs_list.status_code}")
            if jobs_list is not None:
                print(f"Inside if condition, status code = job_list is not None")
                job_list_soup = BeautifulSoup(jobs_list.text, "html.parser")
                page_jobs = job_list_soup.find_all("li")

                # Handle page 0: Add all jobs
                if page_num == 0:
                    for job in page_jobs:
                        self.process_and_insert_job(job, db_handler, processed_ids)
                # Handle subsequent pages: Add only the last job
                else:
                    if page_jobs:
                        job = page_jobs[-1]  # Get the last job post
                        self.process_and_insert_job(job, db_handler, processed_ids)
            else:
                print(f"Reached end of available jobs at page {page_num}")
            
            page_num += 1

        db_handler.close_connection()


    def process_and_insert_job(self,job, db_handler, processed_ids):
        """Process a single job and insert it into the database if not already processed."""
        jobs = {}
        job_div = job.find("div", {"class": "base-card"})
        try:
            jobs["job_role"] = job_div.find("h3", {"class": "base-search-card__title"}).get_text().strip()
        except:
            jobs["job_role"] = None
        try:
            jobs["job_location"] = job_div.find("span", {"class": "job-search-card__location"}).get_text().strip()
        except:
            jobs["job_location"] = None
        try:
            jobs["company_name"] = job_div.find("a", {"class": "hidden-nested-link"}).get_text().strip()
        except:
            jobs["company_name"] = None
        try:
            jobs["date_posted_exact"] = job_div.find("time", {"class": "job-search-card__listdate"}).get("datetime").strip()
        except:
            jobs["date_posted_exact"] = None
        try:
            jobs["date_posted_relative"] = job_div.find("time", {"class": "job-search-card__listdate"}).get_text().strip()
        except:
            jobs["date_posted_relative"] = None
        try:
            jobs["id"] = job_div.get("data-entity-urn").split(":")[3]
        except:
            jobs["id"] = str(random.randint())
            print("ID not available")

        # Check if the job ID is already processed
        if jobs["id"] not in processed_ids:
            processed_ids.add(jobs["id"])  # Mark the job ID as processed
            if jobs["id"].isdigit():
                jobs["job_description"] = self.get_job_decription(int(jobs["id"]))
                time.sleep(1)
            try:
                db_handler.insert_row(jobs)
                print(f"Inserted job with ID {jobs['id']} into the database.")
            except Exception as e:
                print(f"Error inserting job: {e}")
        else:
            print(f"Job with ID {jobs['id']} already processed. Skipping.")


if __name__== '__main__':
    # input section
    job_title = input("Enter job title: ")
    location = input("Enter location: ")
    page_limit = int(input("Enter page limit: "))
    WebScrapper = WebScrapper(job_title, location, page_limit)
    WebScrapper.createDatabase(job_title, location, page_limit)