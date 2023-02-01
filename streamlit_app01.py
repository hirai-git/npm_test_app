import streamlit 
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

#import snowflake.connector
streamlit.header("NPM個別銘柄情報")

def get_query(query_file_path):
    with open(query_file_path, 'r', encoding='utf-8') as f:
        query = f.read()
    return query

def run_query(query_file_path):
   with my_cnx.cursor() as cur:
            query = get_query(query_file_path)
            cur.execute(query)
            rows = cur.fetchall()
            streamlit.dataframe(rows)
      

if __name__ == "__main__":
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    query_file_path = 'npmdbtest.sql'
    run_query(query_file_path)
    my_cnx.close()
      


