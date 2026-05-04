import streamlit as st
from custom import top_menu, bottom_head, site_red

top_menu()

col_jan, col_ryf, col_blu = st.columns([1, 1, 1])

with col_jan:
    st.markdown("<h2 style='text-align: center;'>Jan Frodeno</h2>", unsafe_allow_html=True)
    st.write("<h5 style='text-align: center;'>Total control over every single variable.</h5>", unsafe_allow_html=True)

with col_ryf:
    st.markdown("<h2 style='text-align: center;'>Daniela Ryf</h2>", unsafe_allow_html=True)
    st.write("<h5 style='text-align: center;'>Surgical pacing and mathematicsl precision.</h5>", unsafe_allow_html=True)

with col_blu:
    st.markdown("<h2 style='text-align: center;'>Kristian Blummenfelt</h2>", unsafe_allow_html=True)
    st.write("<h5 style='text-align: center;'>Data and biometrics to push the boundaries of human performance.<h5>", unsafe_allow_html=True)


# Start analysis button

emp_col, an_container, emp_col = st.columns([1, 1, 1])

with emp_col:
    st.write("")

with an_container:
    css = """.st-key-an_container {background-color: rgba(204, 38, 45, .95);}"""
    st.html(f"<style>{css}</style>")

    an_page = st.Page("pages/strategy_analyzer.py")
    an_butt = st.container(height="stretch", width="stretch", border=True, key="an_container")
    an_butt.page_link(an_page, use_container_width=False, label="")
    an_butt.write("<h3 style='text-align: center; color: white'> Start Your Analysis<h3>", unsafe_allow_html=True)

bottom_head()