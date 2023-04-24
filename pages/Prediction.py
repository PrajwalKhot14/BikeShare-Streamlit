import datetime
import streamlit as st

d = st.date_input("Enter date", datetime.date(2019, 7, 6))
st.write(d)