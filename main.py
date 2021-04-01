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
st.write ("---")
st.write (" ")
st.write (" ")

data=pd.read_csv("list.csv",error_bad_lines=False)
today = date.today().strftime("%d") + "/" + date.today().strftime("%m")
today_date = datetime.strptime(today, '%d/%m')

df = data[["Nome","Compleanno"]]
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
next_compl = (df_ordered["diff"]>0) 
next_days = df_ordered[next_compl]["diff"].tolist()[0]

st.write (" ")
st.write (" ")
st.write ("---")
st.write (" ")
st.write (" ")

for idx,diff in enumerate(df_ordered["diff"]):
    if diff == next_days:
        next_names = df_ordered["Nome"].tolist()[idx]
        st.write(""" *Il prossimo da festeggiare tra """+str(next_days)+""" giorni è """+next_names+"""*""")

if st.checkbox("ADMIN"):
    st.header("Admin Section")
    pwd = st.text_input("Inserisci Password",type="password")
    if pwd == "gnappy":
        st.write("### Inserisci nuovo compleanno")
        i1,i2 = st.beta_columns((1,1))
        nome = i1.text_input("Nome")
        compl = i2.date_input("Compleanno")
        new_compl = compl.strftime("%d") + "/" + compl.strftime("%m")
        if st.button("Inserisci"):
            if data["Nome"].tolist().count(nome)>0:
                st.error("Nome già esistente")
            else:
                with open("list.csv","a") as f:
                    f.write(nome+","+new_compl+"\n")
        st.write("### Elimina compleanno")
        e1,e2 = st.beta_columns((1,1))
        nome = e1.selectbox("Seleziona record da eliminare",data["Nome"].unique())
        if st.button("Elimina"):
            data = data.set_index("Nome")
            data = data.drop(nome,axis=0).reset_index() 
            data.to_csv("list.csv",index=False)
        st.write("### Modifica compleanno")
        m1,m2 = st.beta_columns((1,1))
        nome = m1.selectbox("Seleziona record da modificare",data["Nome"].unique())
        data = data.set_index("Nome")
        compl = data["Compleanno"].loc[nome]
        data = data.reset_index()
        modif = m1.radio("Seleziona il campo da modificare",("Nome","Compleanno"))
        if modif == "Nome":
            new_nome = m1.text_input("Inserisci nuovo nome")
            if data["Nome"].tolist().count(new_nome)>0:
                st.error("Nome già esistente!")
        else:
            new_nome = nome
            new_compl = m1.date_input("Inserisci nuovo compleanno")
            compl = new_compl.strftime("%d") + "/" + new_compl.strftime("%m")
        if st.button("Modifica"):
            if data["Nome"].tolist().count(new_nome)>0:
                st.error("Nome già esistente!")
            else:
                data = data.set_index("Nome")
                data = data.drop(nome,axis=0).reset_index()
                new_row = pd.DataFrame({"Nome":[new_nome],"Compleanno": [compl]})
                data.append(new_row,ignore_index=True).to_csv("list.csv",index=False)
