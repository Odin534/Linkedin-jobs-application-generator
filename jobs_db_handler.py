from sqlalchemy import create_engine, text
import pandas as pd
import json
import psycopg2
from psycopg2 import sql

class JobsDBHandler:
    def __init__(self, job_title:str):
        self.job_title = job_title
        self.table_name = self.normalise_job_title(job_title)
        self.conn = self.connect_to_db()
        self.cur = self.conn.cursor()
        self.create_job_table_if_not_exists()


    def load_config(self,path='config.json'):
        with open(path, "r") as f:
            config = json.load(f)
        return config

    def connect_to_db(self):
        config = self.load_config()
        db = config["database"]
        conn = psycopg2.connect(
            host=db["host"],
            dbname=db["name"],
            user=db["user"],
            password=db["password"],
            port=db["port"]
        )
        return conn

    def normalise_job_title(self, job_title: str)->str:
        return "job" + "_" + job_title.strip().lower().replace(" ", "_")

    def create_job_table_if_not_exists(self):
        table_name = self.table_name
        create_table_query = f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            job_role TEXT,
            job_location TEXT,
            company_name TEXT,
            date_posted_exact TEXT,
            date_posted_relative TEXT,
            id BIGINT PRIMARY KEY,
            job_description TEXT
            
        );
        """
        self.cur.execute(create_table_query)
        self.conn.commit()

    def check_of_id_exists(self, job_id: int):
        table_name = self.table_name
        check_query = f"""
        SELECT EXISTS(SELECT 1 FROM {table_name} WHERE id = {job_id});
        """
        self.cur.execute(check_query)
        return self.cur.fetchone()[0]
    
    # Direct approach
    def insert_row(self, job_data: dict):
        id_exists = self.check_of_id_exists(job_data["id"])
        if not id_exists:
            table_name = self.table_name
            keys = job_data.keys()
            values = job_data.values()
            # print(keys)
            # print(values)
            insert_query = sql.SQL("""
            INSERT INTO {table} ({fields}) VALUES ({placeholders})
        """).format(
            table=sql.Identifier(table_name),
            fields=sql.SQL(', ').join(map(sql.Identifier, keys)),
            placeholders=sql.SQL(', ').join(sql.Placeholder() * len(keys))
        )
            
            self.cur.execute(insert_query, tuple(values))
            self.conn.commit()
        else:
            print(f"Job with ID {job_data['id']} already exists in the database.")


    def close_connection(self):
        self.cur.close()
        self.conn.close()   



    # # Dataframe approach
    # def save_jobs_to_db(jobs_df: pd.DataFrame):
    #     create_table_if_not_exists()  # Ensure table is there before insert
    #     try:
    #         jobs_df.to_sql(table_name, engine, if_exists='append', index=False)
    #         print(f"Saved {len(jobs_df)} jobs to database.")
    #     except Exception as e:
    #         print(f"Error saving to DB: {e}")