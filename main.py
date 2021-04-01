#**********************************************
# author: mika.spagnolo@gmail.com
# rev 1.0
# birthday app running on streamlit
#**********************************************

import streamlit as st
import numpy as np
import pandas as pd
import time
from datetime import date 
from datetime import datetime 

st.set_page_config(page_title='birthday', page_icon=':boom:', layout='centered')

def text_colored(color,text):
    my_text = "<font color='"+color+"'> "+text+" </font>"
    return my_text

st.markdown(""" # """+ text_colored("CornflowerBlue", ":tada: Oggi festeggiamo ..."),unsafe_allow_html=True)
st.write (" ")
st.write (" ")
st.write (" ")

data=pd.read_csv("list.csv",error_bad_lines=False)
today = date.today().strftime("%d") + "/" + date.today().strftime("%m")
today_date = datetime.strptime(today, '%d/%m')

df = data[["Nome","Compleanno"]]
#df["Nome"] = df["Nome"] + " " + data["Cognome"].str[0] + "."
df["diff"] = 0

count = 0
for idx,val in enumerate(df["Compleanno"]):
    df["diff"].iloc[idx] = (datetime.strptime(df["Compleanno"].iloc[idx],'%d/%m') - today_date).days
    if df["diff"].iloc[idx] < 0:
        df["diff"].iloc[idx] = 365 + df["diff"].iloc[idx]   
    if val == today:
        st.balloons()
        count = count +1
        nome = df["Nome"].iloc[idx]
        st.markdown(""" # """ + text_colored("red","Auguri "+nome+"!"),unsafe_allow_html=True)

if count == 0:
    st.info("Nessun compleanno oggi!")

df_ordered = df.sort_values(by="diff")
next_names = df_ordered[df_ordered["diff"]>0]["Nome"].tolist()[0]
next_days = df_ordered[df_ordered["diff"]>0]["diff"].tolist()[0]

st.write (" ")
st.write (" ")
st.write (" ")
st.write(""" *Il prossimo da festeggiare tra """+str(next_days)+""" giorni è """+next_names+"""*""")

