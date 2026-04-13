import streamlit as st
import pandas as pd
from custom import top_menu, bottom_head

top_menu()


text, map = st.columns([.35, .65])

with map:
    st.map()

with text:
    st.write("Qui ci vanno le parole")

bottom_head()