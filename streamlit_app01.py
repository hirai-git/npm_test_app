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

def get_share_data():
   con_npm = get_connection()
   querylist = """SELECT distinct SECURITY_CODE,KANJI_NAME
                FROM NPMDB_test.NQIUSER1.ATTRIBUTES
                WHERE CALENDAR_DATE = '20230123' 
                order by SECURITY_CODE desc"""
   querycd = pd.read_sql(querylist,con_npm)
   querycd = querycd.set_index('SECURITY_CODE')

   return querycd


# Using "with" notation
kabulist =get_share_data()

selector = st.sidebar.selectbox( "銘柄CD選択:",list(kabulist.index))

st.header("NPMdata")
meigara_to_show = kabulist.loc[selector]
st.write(meigara_to_show)


def get_query( kabuid:str, filename:str):
    with open(filename, 'r', encoding='utf-8') as f:
        query = f.read().format(kabuid=kabuid)
    return query

if __name__ == "__main__":
    #my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    con= get_connection()
    query_file_path = 'npmdbtest.sql'
    query = get_query(kabuid=selector,filename=query_file_path)
    #my_data_rows=run_query(query_file_path)
    my_data = pd.read_sql(query,con)


st.subheader('株価')

my_data.loc[:,'PRICE']=my_data.loc[:,'PRICE'].astype('int')
my_chart= my_data.set_index("CALENDAR_DATE")["PRICE"]
st.line_chart(my_chart)
st.dataframe(my_data)
