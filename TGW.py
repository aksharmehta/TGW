from concurrent.futures import process
from flask import Flask, redirect, render_template, url_for, request,send_file, Response,flash, session           # import flask
import streamlit as st
import pandas as pd
from st_aggrid import AgGrid
from st_aggrid.grid_options_builder import GridOptionsBuilder
from st_aggrid.shared import GridUpdateMode
from st_aggrid.shared import JsCode
import pandas as pd
import numpy as np
from io import BytesIO
import sys
import time
import xlsxwriter
import plotly
import plotly.graph_objects as go
import gspread as gs

from oauth2client.service_account import ServiceAccountCredentials
from google.oauth2 import service_account
from gsheetsdb import connect


app = Flask(__name__)             # create an app instance
app.config.from_object(__name__)
app.secret_key = b'kc1230'
gc = gs.service_account(filename='thisgoeswith.json')
sheet_url = 'https://docs.google.com/spreadsheets/d/1ES2yN1BPFWeVAlDLmJWvf5hXExci55eooWjDgtCYqJo/edit?usp=sharing'


sh = gc.open_by_url(sheet_url)
ws = sh.worksheet('Sheet1')
df = pd.DataFrame(ws.get_all_records())

df = df.applymap(lambda s: s.upper() if type(s) == str else s)


st.set_page_config(page_icon="✂️", page_title="THIS GOES WITH")

# st.image("https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/240/apple/285/balloon_1f388.png", width=100)
st.image(
    "https://www.thisgoeswith.com/uploads/1/4/2/1/142114579/whatsapp-image-2022-09-15-at-1-32-20-pm_orig.jpeg",
    width=100,
)

st.title("THIS GOES WITH")
c29, c30, c31 = st.columns([1, 6, 1])
with c30:
    with st.form('Form1'):
        numbers = st.text_area("Please enter stock numbers:")
        submitted = st.form_submit_button('Submit')
        

   
    numbers = numbers.upper()
    listStock = numbers.split()

    df1 = df.query("StockNum in @listStock")
    df2 = df1.query("Status == 'SOLD'")
    if not df2.empty:
        st.write("This item has been sold")
        st.dataframe(df2)
    
    with st.form('Form2'):
        st.dataframe(df1)
        st.write("Total is " + df1.Price.sum().astype(str))
        df.loc[df['StockNum'].isin(df1['StockNum']), 'Status'] = 'SOLD'
        orderVal = df1.Price.sum().astype(str)      
        client = st.text_input("Customer Name:")
        phone = st.text_input("Phone Number:")
        pay = st.text_input("Payment Method:")
        orderNum = st.text_input("Order Number:")
        totalPaid = st.text_input("Total Paid:")
        okButton = st.form_submit_button('Submit')

    import gspread_dataframe as gd
    
    if okButton:   
        df.loc[df['StockNum'].isin(df1['StockNum']), 'Status'] = 'SOLD'
        df.loc[df['StockNum'].isin(df1['StockNum']), 'OrderValue'] = orderVal
        df.loc[df['StockNum'].isin(df1['StockNum']), 'OrderNum'] = orderNum
        df.loc[df['StockNum'].isin(df1['StockNum']), 'Customer'] = client
        df.loc[df['StockNum'].isin(df1['StockNum']), 'Phone'] = phone
        df.loc[df['StockNum'].isin(df1['StockNum']), 'ModeOfPayment'] = pay
        df.loc[df['StockNum'].isin(df1['StockNum']), 'TotalPaid'] = totalPaid
        gd.set_with_dataframe(ws, df)
        st.write("Data has been sent to Google Sheets")
        st.balloons()

    #change values in df based on df1
        




