import streamlit 
import pandas
import requests
import snowflake.connector

from urllib.error import URLError
#import snowflake.connector
streamlit.header("NPMdata")

def get_query(query_file_path):
    with open(query_file_path, 'r', encoding='utf-8') as f:
        query = f.read()
    return query

def run_query():
   with my_cnx.cursor() as cur:
            query = get_query(query_file_path)
            cur.execute("select CALENDAR_DATE,SECURITY_CODE,KANJI_NAME from NPMDB_test.NQIUSER1.ATTRIBUTES where SECURITY_CODE='1301' and CALENDAR_DATE between 20220101 and 20221231 order by CALENDAR_DATE")
            return cur.fetchall()
            
if __name__ == "__main__":
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    query_file_path = 'npmdbtest.sql'
    my_data_rows=run_query()
    streamlit.dataframe(my_data_rows)
    my_cnx.close()
