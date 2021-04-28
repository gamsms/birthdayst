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
from passlib.hash import pbkdf2_sha256 as pw

st.set_page_config(page_title='birthday', page_icon=':boom:', initial_sidebar_state='collapsed')

def text_colored(color,text):
    """
    @ color a string as html unsafe
    """
    my_text = "<font color='"+color+"'> "+text+" </font>"
    return my_text

def empty_line(n,add_line=False):
    if add_line:
      st.write("---")
    for i in range(1,n):
      st.write(" ")

def compute_birth(df):
    df = df.copy()
    today = date.today().strftime("%d/%m")
    today_date = datetime.strptime(today, '%d/%m')
    df["Compleanno"] = pd.to_datetime(df["Compleanno"],format="%d/%m") 
    df["diff"] = df["Compleanno"].transform(lambda x: (x-today_date).days if (x-today_date).days >= 0 else 365+(x-today_date).days) 
    df = df.sort_values(by="diff")
    next_day = df[df["diff"]!=0]["diff"].tolist()[0]
    today_list = []
    next_list = []
    for idx,diff in enumerate(df["diff"]):
        nome = df["Nome"].iloc[idx]
        if diff == 0 : today_list.append(nome)
        elif diff == next_day : next_list.append(nome)
    return today_list,next_list,next_day

myhash = '$pbkdf2-sha256$29000$/5.zFgKA0Nrbm5PyPqf0Pg$RcLiratElAGQ2SG.1SpBkwBgyuENNSFUeJf2rgdEg48'
def mysidebar(myhash):
    st.sidebar.header("Seleziona la modalita`")
    mode = st.sidebar.radio("",("User","Admin"))
    st.sidebar.write("""_In modalita\` **ADMIN** inserendo la password si ha la possibilita\` di inserire,modificare o eliminare un record._""")
    if mode == "Admin":
        pwd = st.sidebar.text_input("Inserisci Password",type="password")
        if pw.verify(pwd,myhash):
            admin_mode = True
            st.sidebar.success("Modalita` admin abilitata")
        elif pwd == "":
            admin_mode = False
        else:
            st.sidebar.error("Password errata!")
            admin_mode = False
    else:
        admin_mode = False
    return admin_mode

def insert_compl(data,nome,compl,myfile="list.csv"):
    if data["Nome"].tolist().count(nome)>0:
        st.error("Nome gia` esistente!")
    elif nome == "":
        st.error("Nome non valido!")
    else:
        new_row = pd.DataFrame({"Nome":[nome],"Compleanno": [compl]})
        data = data.append(new_row,ignore_index=True)
        data.to_csv(myfile,index=False)
    return data
    
def remove_compl(data,nome,myfile="list.csv"):
    data = data.set_index("Nome")
    data = data.drop(nome,axis=0).reset_index() 
    data.to_csv(myfile,index=False)
    return data
        
st.markdown(""" # """+ text_colored("CornflowerBlue", ":tada: Oggi festeggiamo ..."),unsafe_allow_html=True)
empty_line(1,True)

admin_mode = mysidebar(myhash)
data=pd.read_csv("list.csv",error_bad_lines=False)

if admin_mode:
    st.title("Modalita` admin")
    azione = st.radio("Cosa vuoi fare?",("Inserisci","Modifica","Elimina"))
    if azione == "Inserisci":
        st.header("Inserisci nuovo record")
        nome = st.text_input("Nome")
        compl = st.date_input("Compleanno").strftime("%d/%m")
        if st.button("Inserisci"):
            data = insert_compl(data,nome,compl,"list.csv")
    elif azione == "Modifica":
        st.header("Modifica record esistente")
        nome_old = st.selectbox("Record da modificare",data["Nome"].unique())
        data = data.set_index("Nome")
        compl_old = data["Compleanno"].loc[nome_old]
        data = data.reset_index()
        modif = st.radio("Seleziona il campo da modificare",("Nome","Compleanno"))
        if modif == "Nome":
            nome = st.text_input("Inserisci nuovo nome")
            compl = compl_old
        else:
            compl = st.date_input("Inserisci nuovo compleanno").strftime("%d/%m")
            nome = nome_old
        if st.button("Modifica"):
            data = remove_compl(data,nome_old,"list.csv")
            data = insert_compl(data,nome,compl,"list.csv")
    elif azione == "Elimina":
        st.header("Elimina record esistente")
        nome = st.selectbox("Record da eliminare",data["Nome"].unique())
        if st.button("Elimina"):
            data = remove_compl(data,nome,"list.csv")
    else:
        st.warning("Seleziona un'azione valida")
    st.header("Compleanni")
    st.write(data)
    st.title("Modalita` Utente")
    empty_line(3,True)
    
today_list,next_list,next_day = compute_birth(data)
if len(today_list) == 0:
    st.info("Nessun compleanno oggi!")
else:
    for nome in today_list:
        st.balloons()
        st.markdown(""" # """ + text_colored("red","Auguri "+nome+"!"),unsafe_allow_html=True)
empty_line(4,True)
for nome in next_list:
    st.write(""" *Il prossimo da festeggiare tra """+str(next_day)+""" giorni è """+nome+"""*""")
