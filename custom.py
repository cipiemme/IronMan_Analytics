import streamlit as st

def top_menu():
    st.set_page_config(
        page_title="IRONMAN view",
#    page_icon="Logo",
        layout="wide",
        initial_sidebar_state="collapsed"
        )

# define colors and dimensions of top line
    st.markdown("""
        <style>
        /* Hide the default Streamlit sidebar and header */
        [data-testid="collapsedControl"] { display: none; }
        section[data-testid="stSidebar"] { display: none; }
        header {visibility: hidden;}
        
        /* Reduce top/bottom padding of main content */
        .block-container {
            padding-top: 2rem !important;
            padding-bottom: 5rem !important;
        }
        
        /* Color accent bar at the top of the page */
        .disk-bar {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 10px;
            background: linear-gradient(
                90deg,
                #343434 0%,
                #343434 15%,
                #1976d2 15%,
                #1976d2 35%,
                #d32f2f 40%,
                #d32f2f 57.5%,
                #d4af37 62.5%,
                #d4af37 80%,
                #e0e0e0 85%,
                #e0e0e0 100%
            );
        }
                
        /* Mobile Responsiveness Overrides */
        @media (max-width: 640px) {
            .hero-title {
                font-size: 4rem !important;
                line-height: 1.2 !important;
                width: 100% !important;
            }
            .block-container {
                padding-left: 0.5rem !important;
                padding-right: 0.5rem !important;
                max-width: 100% !important;
            }
        }

        /* --- Header Nav Link Colors --- */
        div[data-testid="stColumn"] a[data-testid="stPageLink-NavLink"] {
            display: flex !important;
            justify-content: center !important;
            align-items: center !important;
        }

        </style>
        
        <div class="disk-bar"></div>

    """,
    unsafe_allow_html=True,
    )

    pages = {
        "Home": st.Page("streamlit_app.py"),
        "Race compare": st.Page("pages/race_comp.py", icon="🏠"),
        "Athlete compare": st.Page("pages/athlete_comp.py", icon="🏋️"),
        "Records": st.Page("pages/records.py", icon="🏆"),
        "Info": st.Page("pages/info.py", icon="ℹ️")
        }
    # Render top navigation using native columns
    with st.container():
        headerNavLinks = st.columns([.55, 1.3, 1.3, 1.3, .55])
        with headerNavLinks[0]: st.page_link(pages["Home"], label="IM view", use_container_width=True)
        with headerNavLinks[1]: st.page_link(pages["Race compare"], label="Race compare", use_container_width=True)
        with headerNavLinks[2]: st.page_link(pages["Athlete compare"], label="Athletes", use_container_width=True)
        with headerNavLinks[3]: st.page_link(pages["Records"], label="Records", use_container_width=True)
        with headerNavLinks[4]: st.page_link(pages["Info"], label="Info", use_container_width=True)
    
    st.markdown("---")







def bottom_head():
    st.markdown("---")
    st.header("✉️ Get in Touch")
    st.write("Want to rate your experience on this site? Found a bug? Have a feature request?")

    c0, c1, c2 = st.columns(3)

    with c0:
        st.page_link(st.Page("pages/rate_page.py"), label="Rate us!")

    with c1:
        st.markdown(" 📧 Email")
        st.code("placeholder.one@example.com")

    with c2:
        st.markdown(" 📧 Email")
        st.code("placeholder.two@example.com")




