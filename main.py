import streamlit as st
import pandas as pd
from custom import top_menu, bottom_head

top_menu()

text, map = st.columns([.4, .6])

with text:
    st.write("Qui ci vanno le parole")

with map:
    st.image("Images/world_map_colored_150.png", caption="Participants world heat map, for more info visit the [Demographics](demographics) page")

bottom_head()