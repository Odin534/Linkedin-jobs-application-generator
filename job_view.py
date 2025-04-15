import tkinter as tk
from tkinter import ttk, messagebox
from jobs_db_handler import JobsDBHandler
import webscrapper

# class jobViewPage:
#     def __init__(self, root, job_title):
#             self.root = root
#             self.root.title("Job Viewer")
#             self.db = JobsDBHandler(job_title)
            
#             # Scrollable canvas setup
#             canvas = tk.Canvas(root)
#             scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
#             self.frame = tk.Frame(canvas)

#             self.frame.bind(
#                 "<Configure>",
#                 lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
#             )

#             canvas.create_window((0, 0), window=self.frame, anchor="nw")
#             canvas.configure(yscrollcommand=scrollbar.set)

#             canvas.pack(side="left", fill="both", expand=True)
#             scrollbar.pack(side="right", fill="y")

#             self.load_jobs()

#     def load_jobs(self):
#         rows, columns = self.db.fetch_all_jobs()
#         self.columns = columns

#         # Headers
#         for col_idx, col in enumerate(columns):
#             tk.Label(self.frame, text=col, borderwidth=1, relief="solid", width=20).grid(row=0, column=col_idx)
#         tk.Label(self.frame, text="Action", borderwidth=1, relief="solid", width=15).grid(row=0, column=len(columns))

#         # Data rows
#         for row_idx, row in enumerate(rows, start=1):
#             for col_idx, value in enumerate(row):
#                 tk.Label(self.frame, text=value, borderwidth=1, relief="solid", width=20, anchor="w", justify="left", wraplength=200).grid(row=row_idx, column=col_idx)
            
#             job_data = dict(zip(self.columns, row))
#             btn = tk.Button(self.frame, text="Modify CV", command=lambda jd=job_data: self.modify_documents(jd))
#             btn.grid(row=row_idx, column=len(self.columns), padx=5)

#     def modify_documents(self):
#         pass
class JobViewerApp:
    def __init__(self, root, job_title):
        self.db = JobsDBHandler(job_title)
        self.root = root
        self.root.title("Job Viewer")

        self.tree = ttk.Treeview(root)
        self.tree.pack(fill="both", expand=True)

        self.select_button = ttk.Button(root, text="Show details", command=self.modify_documents)
        self.select_button.pack(pady=10)

        self.load_jobs()

    def load_jobs(self):
        rows, columns = self.db.fetch_all_jobs()
        self.tree["columns"] = columns
        self.tree["show"] = "headings"
        self.columns = columns

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)

        for row in rows:
            self.tree.insert("", "end", values=row)

    def show_details(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a job row.")
            return
        
        values = self.tree.item(selected[0])["values"]
        job_data = dict(zip(self.columns, values))

        # 👇 Placeholder for LLM integration
        job_description = job_data.get("job_description", "")
        print(f"Sending to LLM: {job_description[:100]}...")  # Truncate for preview

        messagebox.showinfo("LLM Call", "This would now call the LLM to modify the CV & cover letter.")
