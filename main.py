import streamlit as st
import custom as c

c.top_menu()

text, map = st.columns([.4, .6])

with text:
    st.write("Qui ci vanno le parole")
    st.write("Prova")
    st.write("Prova2")

with map:
    st.image("Images/world_map_colored_150.png", caption="Participants world heat map, for more info visit the [Demographics](demographics) page")

c.bottom_head()