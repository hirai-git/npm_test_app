import streamlit 
import pandas
import requests
import snowflake.connector
import os
from dotenv import load_dotenv
# .envファイルの内容を読み込見込む
load_dotenv()

from urllib.error import URLError
#import snowflake.connector
streamlit.header("NPMdata")

def get_connection():
    con = snowflake.connector.connect(
        user = os.environ['SNOWFLAKE_USER'],
        password = os.environ['SNOWFLAKE_PASSWORD'],
        account = os.environ['SNOWFLAKE_ACCOUNT'],
        warehouse = os.environ['SNOWFLAKE_WAREHOUSE'],
        database = os.environ['SNOWFLAKE_DATABASE'],
        role = os.environ['SNOWFLAKE_ROLE'],
        schema = os.environ['SNOWFLAKE_SCHEMA']
    )
    #data=pd.read_sql("select * from nqiuser1.db_master ",con )
    #print(data)
    return con

def get_query(query_file_path):
    with open(query_file_path, 'r', encoding='utf-8') as f:
        query = f.read()
    return query

if __name__ == "__main__":
    #my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    con= get_connection()
    query_file_path = 'npmdbtest.sql'
    query = get_query(query_file_path)
    #my_data_rows=run_query(query_file_path)
    my_data_rows2 = pandas.read_sql(query,con)


my_data_rows2.loc[:,'PRICE']=my_data_rows2.loc[:,'PRICE'].astype('int')
streamlit.dataframe(my_data_rows2)


#streamlit.dataframe(my_data_rows2)
con.close()

    #https://www.freecodecamp.org/japanese/news/connect-python-with-sql/
    #https://linus-mk.hatenablog.com/entry/pandas_convert_float_to_int
        
