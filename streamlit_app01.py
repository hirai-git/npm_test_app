import streamlit as st
import pandas as pd
import requests
import snowflake.connector
import datetime as dt
import jpbizday


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

def get_share_data(kabulist_date:str):
   con_npm = get_connection()
   querylist = f"""select distinct SECURITY_CODE, KANJI_NAME
                    from NPMDB_test.NQIUSER1.ATTRIBUTES 
                    WHERE CALENDAR_DATE = {kabulist_date}
                    and  SECURITY_CODE not like '%0000%'
                    order by SECURITY_CODE;
                """
   querycd = pd.read_sql(querylist,con_npm)
   querycd = querycd.set_index('SECURITY_CODE')
   con_npm.close()
   return querycd


# 第一営業日取得
kabulist_date = format(jpbizday.first_bizday(dt.datetime.today()), '%Y%m%d')
kabulist =get_share_data(kabulist_date)

selector = st.sidebar.selectbox( "銘柄CD選択:",list(kabulist.index))
selector2 = selector[0:4] 
date1 = st.sidebar.date_input("from-date",
                              value=dt.date(2020, 1, 1),
                              min_value=dt.date(1992,1,1),
                              max_value=dt.date.today())
date1 = format(date1, '%Y%m%d')
date2 = st.sidebar.date_input("to-date",
                              value=dt.date.today(),
                              min_value=dt.date(1992,1,1),
                              max_value=dt.date.today())
date2 = format(date2, '%Y%m%d')

st.header("NPMdata")
meigara_to_show = kabulist.loc[selector]
st.dataframe(meigara_to_show)


def get_query( kabuid:str, date_from:str, date_to:str, filename:str):
    with open(filename, 'r', encoding='utf-8') as f:
        query = f.read().format(kabuid=kabuid,date_from=date_from,date_to=date_to)
    return query

st.subheader('株価グラフ表示')
#if __name__ == "__main__":
if st.button('push display'):   
    #my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    con= get_connection()
    query_file_path = 'npmdbtest.sql'
    query = get_query(kabuid=selector2,date_from=date1,date_to=date2,filename=query_file_path)
    #my_data_rows=run_query(query_file_path)
    my_data = pd.read_sql(query,con)
    con.close()
    
    my_data.loc[:,'PRICE']=my_data.loc[:,'PRICE'].astype('int')
    my_chart= my_data.set_index("CALENDAR_DATE")["PRICE"]
    st.line_chart(my_chart)
    st.dataframe(my_data)

    st.subheader('20日移動平均株価')
    my_data2=my_chart
    my_data2=my_data2.rolling(20).apply(lambda x: x.mean())
    st.line_chart(my_data2)
    st.dataframe(my_data2)




    #https://www.freecodecamp.org/japanese/news/connect-python-with-sql/
    #https://linus-mk.hatenablog.com/entry/pandas_convert_float_to_int
        