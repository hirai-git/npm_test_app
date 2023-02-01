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

def run_query(query_file_path):
   with my_cnx.cursor() as cur:
            query = get_query(query_file_path)
            cur.execute(query)
            return cur.fetchall()
            
if __name__ == "__main__":
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    query_file_path = 'npmdbtest.sql'
    my_data_rows=run_query(query_file_path)
    
    from_db = []
    for result in my_data_rows:
        result = list(result)
        from_db.append(result)
    feature = ["height","weight","blood type","age"]
    my_data_rows2=pandas.DataFrame(from_db,columns=feature)
    streamlit.dataframe(my_data_rows2)
    
    
    #streamlit.dataframe(my_data_rows2)
    my_cnx.close()
