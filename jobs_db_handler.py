from sqlalchemy import create_engine
import pandas as pd
import json


def load_config(path='config.json'):
    with open(path, "r") as f:
        config = json.load(f)
    return config

def get_engine():
    db = load_config()
    return create_engine(
        f"postgresql://{db['user']}:{db['password']}@{db['host']}:{db['port']}/{db['name']}")

def normalise_job_title(job_title: str)->str:
    return "job" + job_title.strip().lowe().replace(" ", "_")

def create_job_table_if_not_exists(engine, job_title:str):
    table_name = normalise_job_title(job_title)
    create_table_query = f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
        id SERIAL PRIMARY KEY,
        job_role TEXT,
        job_location TEXT,
        company_name TEXT,
        date_posted_exact TEXT,
        date_posted_relative TEXT,
        job_description TEXT
    );
    """
    with engine.connect() as conn:
        conn.execute(text(create_table_query))
        print(f"Ensured table '{table_name}' exists.")

# Direct approach
def insert_row(engine, job_title:str, job_data: dict):
    create_job_table_if_not_exists(engine, job_title)
    table_name = normalise_job_title(job_title)

    keys = ", ".join(job_data.keys())
    values = ", ".join([f":{k} for k in job_data.keys()"])
    insert_querry = f"INSERT INTO {table_name} ({keys}) VALUES ({values})"

    with engine.connect() as conn:
        conn.execute(text(insert_querry), job_data)



# # Dataframe approach
# def save_jobs_to_db(jobs_df: pd.DataFrame):
#     create_table_if_not_exists()  # Ensure table is there before insert
#     try:
#         jobs_df.to_sql(table_name, engine, if_exists='append', index=False)
#         print(f"Saved {len(jobs_df)} jobs to database.")
#     except Exception as e:
#         print(f"Error saving to DB: {e}")