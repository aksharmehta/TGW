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
import plotly.express as px 
from oauth2client.service_account import ServiceAccountCredentials
from google.oauth2 import service_account
from gsheetsdb import connect
from datetime import datetime


app = Flask(__name__)             # create an app instance
app.config.from_object(__name__)
app.secret_key = b'kc1230'
gc = gs.service_account(filename='thisgoeswith.json')
sheet_url = 'https://docs.google.com/spreadsheets/d/1HPyY-IfmrYmFVTvqc26Eejl1X_ZAwACW573lS94MD2U/edit?usp=sharing'


sh = gc.open_by_url(sheet_url)
ws = sh.worksheet('Sales')
df = pd.DataFrame(ws.get_all_records())

df = df.applymap(lambda s: s.upper() if type(s) == str else s)
df["Hour"]=pd.to_datetime(df["Time Stamp"],format="%d/%m/%Y %H:%M").dt.hour
print(df)

st.set_page_config(page_icon="✂️", page_title="THIS GOES WITH")

# st.image("https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/240/apple/285/balloon_1f388.png", width=100)
st.image(
    "https://www.thisgoeswith.com/uploads/1/4/2/1/142114579/whatsapp-image-2022-09-15-at-1-32-20-pm_orig.jpeg",
    width=100,
)

st.title("THIS GOES WITH")

st.title(":bar_chart: Sales Dashboard")
st.markdown("##")



# TOP KPI's
total_sales= int(df["Total Amount"].sum())
average_sale_by_transaction=round(df["Total Amount"].mean(),2)


# KPI's COLUMNS
left_column,middle_column,right_column=st.columns(3)


with left_column:
  st.subheader("Total Sales:")
  st.subheader(f"Rs {total_sales:,}")

with right_column:
  st.subheader("Average Sales Per Transaction:")
  st.subheader(f"Rs {average_sale_by_transaction}")

st.markdown("---")



sales_by_product_line=(
  df.groupby(by=["Brand"]).sum()[["Total Amount"]].sort_values(by="Total Amount")
)

fig_product_sales = px.bar(
    sales_by_product_line,
    x="Total Amount",
    y=sales_by_product_line.index,
    orientation="h",
    title="<b>Sales by Brand</b>",
    text = "Total Amount",
    color_discrete_sequence=["#205295"] * len(sales_by_product_line),
    template="plotly_white"
)

fig_product_sales.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False)),
    yaxis=(dict(showgrid=False))
)

fig_product_sales.update_xaxes(showgrid=False)
fig_product_sales.update_yaxes(showgrid=False)



sales_by_hour=df.groupby(by=["Hour"]).sum()[["Total Amount"]]

fig_hourly_sales=px.bar(
    sales_by_hour,
    x=sales_by_hour.index,
    y="Total Amount",
    text = "Total Amount",
    title="<b>Sales by Hour</b>",
    color_discrete_sequence=["#205295"] * len(sales_by_hour),
    template="plotly_white",
)

fig_hourly_sales.update_layout(
    xaxis=dict(tickmode="linear"),
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis=(dict(showgrid=False)),
)



sales_by_customer=(
  df.groupby(by=["Client Name"]).sum()[["Total Amount"]].sort_values(by="Total Amount")
)

fig_customer = px.bar(
    sales_by_customer,
    x="Total Amount",
    y=sales_by_customer.index,
    orientation="h",
    title="<b>Sales by Customer</b>",
    text = "Total Amount",
    color_discrete_sequence=["#205295"] * len(sales_by_customer),
    template="plotly_white"
)

fig_customer.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False)),
    yaxis=(dict(showgrid=False))
)

fig_customer.update_xaxes(showgrid=False)
fig_customer.update_yaxes(showgrid=False)





sales_by_mode=(
  df.groupby(by=["Mode of Payment"]).sum()[["Total Amount"]].sort_values(by="Total Amount")
)

fig_mode = px.bar(
    sales_by_mode,
    x="Total Amount",
    y=sales_by_mode.index,
    orientation="h",
    title="<b>Sales by Mode</b>",
    text = "Total Amount",
    color_discrete_sequence=["#205295"] * len(sales_by_mode),
    template="plotly_white"
)

fig_mode.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False)),
    yaxis=(dict(showgrid=False))
)

fig_mode.update_xaxes(showgrid=False)
fig_mode.update_yaxes(showgrid=False)



sales_by_order=(
  df.groupby(by=["Custom"]).sum()[["Total Amount"]].sort_values(by="Total Amount")
)

fig_custom = px.bar(
    sales_by_order,
    x="Total Amount",
    y=sales_by_order.index,
    orientation="h",
    title="<b>Order / Ready</b>",
    text = "Total Amount",
    color_discrete_sequence=["#205295"] * len(sales_by_order),
    template="plotly_white"
)

fig_custom.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False)),
    yaxis=(dict(showgrid=False))
)

fig_custom.update_xaxes(showgrid=False)
fig_custom.update_yaxes(showgrid=False)




# Displaying charts

st.plotly_chart(fig_product_sales,theme="streamlit",use_container_width=True)
st.plotly_chart(fig_hourly_sales,use_container_width=True,theme="streamlit")


st.plotly_chart(fig_customer,use_container_width=True,theme="streamlit")
st.plotly_chart(fig_mode,use_container_width=True,theme="streamlit")

#left_column,right_column=st.columns(2)
st.plotly_chart(fig_custom,use_container_width=True,theme="streamlit")
#st.plotly_chart(fig_custom, theme="streamlit", use_container_width=True)

#right_column.plotly_chart(fig_mode,use_container_width=True)


# HIDE STREAMLIT STYLE
hide_st_style="""
            <style>
            #MainMenu {visibility:hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """

st.markdown(hide_st_style, unsafe_allow_html=True)

