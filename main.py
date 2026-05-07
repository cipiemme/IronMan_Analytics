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

st.write("""
        <style>
        .button {
          height: 161px;
          position: relative;
          width: 716px;
          left: 25%;
        }

        .button .rectangle {
          background-color: #cc262d;
          border-radius: 20px;
          box-shadow: 0px 4px 4px #ff060680;
          height: 86.96%;
          left: 2.65%;
          position: absolute;
          top: 6.83%;
          width: 94.69%;
        }

        .button .text-wrapper {
          align-items: center;
          color: #ffffff;
          display: flex;
          font-family: Iceland-Regular, Helvetica;
          font-size: 50px;
          font-weight: 400;
          height: 100%;
          justify-content: center;
          left: 0;
          letter-spacing: 0;
          line-height: normal;
          position: absolute;
          text-align: center;
          top: 0;
          width: 100%;
        }
        </style>

        <html>
        <body>
        <div class="button" ><div class="rectangle" ></div>
        <div class="text-wrapper" >Start Your Analysis</div></div>
        </body>
        </html>

        """,
        unsafe_allow_html=True)


bottom_head()