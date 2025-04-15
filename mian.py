from webscrapper import WebScrapper
import tkinter as tk
from job_view import JobViewerApp

if __name__== '__main__':
    # input section
    job_title = input("Enter job title: ")
    location = input("Enter location: ")
    page_limit = int(input("Enter page limit: "))
    WebScrapper = WebScrapper(job_title, location, page_limit)
    WebScrapper.createDatabase(job_title, location, page_limit)
    root = tk.Tk()
    app = JobViewerApp(root, job_title)
    root.mainloop()