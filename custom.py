import streamlit as st
import pandas as pd

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
        "Home": st.Page("main.py"),
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

def load_merge():
    # load all files
    F03 = pd.read_csv("/Data/WorldChamp/F/IM2003_F.csv")
    M03 = pd.read_csv("/Data/WorldChamp/M/IM2003_M.csv")
    F04 = pd.read_csv("/Data/WorldChamp/F/IM2004_F.csv")
    M04 = pd.read_csv("/Data/WorldChamp/M/IM2004_M.csv")
    F05 = pd.read_csv("/Data/WorldChamp/F/IM2005_F.csv")
    M05 = pd.read_csv("/Data/WorldChamp/M/IM2005_M.csv")
    F06 = pd.read_csv("/Data/WorldChamp/F/IM2006_F.csv")
    M06 = pd.read_csv("/Data/WorldChamp/M/IM2006_M.csv")
    F07 = pd.read_csv("/Data/WorldChamp/F/IM2007_F.csv")
    M07 = pd.read_csv("/Data/WorldChamp/M/IM2007_M.csv")
    F08 = pd.read_csv("/Data/WorldChamp/F/IM2008_F.csv")
    M08 = pd.read_csv("/Data/WorldChamp/M/IM2008_M.csv")
    F09 = pd.read_csv("/Data/WorldChamp/F/IM2009_F.csv")
    M09 = pd.read_csv("/Data/WorldChamp/M/IM2009_M.csv")
    F10 = pd.read_csv("/Data/WorldChamp/F/IM2010_F.csv")
    M10 = pd.read_csv("/Data/WorldChamp/M/IM2010_M.csv")
    F11 = pd.read_csv("/Data/WorldChamp/F/IM2011_F.csv")
    M11 = pd.read_csv("/Data/WorldChamp/M/IM2011_M.csv")
    F12 = pd.read_csv("/Data/WorldChamp/F/IM2012_F.csv")
    M12 = pd.read_csv("/Data/WorldChamp/M/IM2012_M.csv")
    F13 = pd.read_csv("/Data/WorldChamp/F/IM2013_F.csv")
    M13 = pd.read_csv("/Data/WorldChamp/M/IM2013_M.csv")
    F14 = pd.read_csv("/Data/WorldChamp/F/IM2014_F.csv")
    M14 = pd.read_csv("/Data/WorldChamp/M/IM2014_M.csv")
    F15 = pd.read_csv("/Data/WorldChamp/F/IM2015_F.csv")
    M15 = pd.read_csv("/Data/WorldChamp/M/IM2015_M.csv")
    F16 = pd.read_csv("/Data/WorldChamp/F/IM2016_F.csv")
    M16 = pd.read_csv("/Data/WorldChamp/M/IM2016_M.csv")
    F17 = pd.read_csv("/Data/WorldChamp/F/IM2017_F.csv")
    M17 = pd.read_csv("/Data/WorldChamp/M/IM2017_M.csv")
    F18 = pd.read_csv("/Data/WorldChamp/F/IM2018_F.csv")
    M18 = pd.read_csv("/Data/WorldChamp/M/IM2018_M.csv")
    F19 = pd.read_csv("/Data/WorldChamp/F/IM2019_F.csv")
    M19 = pd.read_csv("/Data/WorldChamp/M/IM2019_M.csv")
    F22 = pd.read_csv("/Data/WorldChamp/F/IM2022_F.csv")
    M22 = pd.read_csv("/Data/WorldChamp/M/IM2022_M.csv")
    F23 = pd.read_csv("/Data/WorldChamp/F/IM2023_F.csv")
    M23 = pd.read_csv("/Data/WorldChamp/M/IM2023_M.csv")
    F24 = pd.read_csv("/Data/WorldChamp/F/IM2024_F.csv")
    M24 = pd.read_csv("/Data/WorldChamp/M/IM2024_M.csv")
    F25 = pd.read_csv("/Data/WorldChamp/F/IM2025_F.csv")
    M25 = pd.read_csv("/Data/WorldChamp/M/IM2025_M.csv")

    # Dynamically collect all Fxx and Mxx dataframes
    all_dataframes_to_combine = []

    # Get all variables in the global scope
    current_globals = globals()
    for name in list(current_globals.keys()): # Iterate over a copy of keys
        # Check if the variable name matches the pattern Fxx or Mxx and is a DataFrame
        if (name.startswith('F') or name.startswith('M')) and len(name) == 3 and name[1:].isdigit():
            df = current_globals[name]
            if isinstance(df, pd.DataFrame):
                all_dataframes_to_combine.append(df)

    # Concatenate all collected dataframes into one
    combined_df = pd.concat(all_dataframes_to_combine, ignore_index=True)

    # Replace important names to be consistent with Geopandas database
    combined_df['Country'] = combined_df['Country'].replace('United States', 'United States of America')
    combined_df['Country'] = combined_df['Country'].replace('Bosnia and Herzegovina', 'Bosnia and Herz.')
    combined_df['Country'] = combined_df['Country'].replace('Argentinia', 'Argentina')
    combined_df['Country'] = combined_df['Country'].replace('SOUTH KOREA', 'South Korea')
    combined_df['Country'] = combined_df['Country'].replace('DEUTSHLAND', 'Germany')
    combined_df['Country'] = combined_df['Country'].replace('Russian Federation', 'Russia')
    combined_df['Country'] = combined_df['Country'].replace('Czech Republic', 'Czechia')

    return combined_df



