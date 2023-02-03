import streamlit as st
import pandas as pd
import requests
import snowflake.connector

import os
from dotenv import load_dotenv
# .envファイルの内容を読み込見込む
load_dotenv()

from urllib.error import URLError

#import snowflake.connector
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



def get_share_data(this_kabu_cd):
   con_npm = get_connection()
   querylist = """SELECT distinct(SECURITY_CODE)
                FROM ATTRIBUTES A 
                WHERE A.CALENDAR_DATE = '20230201' """
   
   querycd = pd.read_sql(querylist,con_npm)

   if kabu_cd in querycd:
      this_kabu_cd = kabu_cd
   else: st.error("Please select a share_cd to get information.") 

   return this_kabu_cd

# Using "with" notation

st.header("Fruityvice Fruit Advice!")
try:
    kabu_cd = st.text_input('証券CDをいれてね','1301')
    if not kabu_cd:
       st.error("Please select a share_cd to get information.") 
    else:
       kabu_OK_cd =get_share_data(kabu_cd)
except URLError as e:
    st.error() 




st.header("NPMdata")

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
    my_data = pd.read_sql(query,con)




st.subheader('株価')

my_data.loc[:,'PRICE']=my_data.loc[:,'PRICE'].astype('int')
my_chart= my_data.set_index("CALENDAR_DATE")["PRICE"]
st.line_chart(my_chart)
st.dataframe(my_data)


#streamlit.dataframe(my_data_rows2)
con.close()

    #https://www.freecodecamp.org/japanese/news/connect-python-with-sql/
    #https://linus-mk.hatenablog.com/entry/pandas_convert_float_to_int
        

