select a.CALENDAR_DATE as CALENDAR_DATE,a.SECURITY_CODE as SECURITY_CODE ,a.KANJI_NAME as KANJI_NAME,FLOOR(m.PRICE) as PRICE
from NPMDB_test.NQIUSER1.ATTRIBUTES A
left join NPMDB_test.NQIUSER1.MARKET M on 
 a.CALENDAR_DATE=m.CALENDAR_DATE and
 a.SECURITY_ID=m.SECURITY_ID
 where a.SECURITY_CODE= '+ kabu_OK_cd +'
  and m.APPRAISAL_ID=1
 and a.CALENDAR_DATE between 20220101 and 20221231  
 order by a.CALENDAR_DATE;
