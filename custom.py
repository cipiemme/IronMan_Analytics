import streamlit as st
import pandas as pd
import geopandas as gpd

def top_menu():
    st.set_page_config(
        page_title="IronMan Analytics",
        layout="wide",
        initial_sidebar_state="collapsed"
        )
    pages = {
        "Home": st.Page("main.py"),
        "Race compare": st.Page("pages/race_comp.py", icon="🏠"),
        "Athlete compare": st.Page("pages/athlete_comp.py", icon="🏋️"),
        "Strategy analyzer": st.Page("pages/strategy_analyzer.py", icon="🗺️"),
        "Strategy builder": st.Page("pages/strategy_builder.py", icon="🔮"),
        "Info": st.Page("pages/info.py", icon="ℹ️")
        }
    # Render top navigation using native columns
    with st.container(height="stretch", width="stretch", border=False):
        headerNavLinks = st.columns([.55, 1.3, 1.3, 1.3, .55])
        with headerNavLinks[0]: st.page_link(pages["Home"], label="IM Analytics", use_container_width=True)
        with headerNavLinks[1]: st.page_link(pages["Race compare"], label="Race compare", use_container_width=True)
        with headerNavLinks[2]: st.page_link(pages["Athlete compare"], label="Athletes", use_container_width=True)
        with headerNavLinks[3]: st.page_link(pages["Records"], label="Records", use_container_width=True)
        with headerNavLinks[4]: st.page_link(pages["Info"], label="Info", use_container_width=True)
# define colors and dimensions of top line
    st.markdown("""
        <style>
        /* Hide the default Streamlit sidebar and header */
        [data-testid="collapsedControl"] { display: none; }
        section[data-testid="stSidebar"] { display: none; }
        header {visibility: hidden;}
        
        /* Reduce top/bottom padding of main content */
        .block-container {
            padding-top: 1rem !important;
            padding-bottom: 0rem !important;
        }

        /* Color accent bar at the top of the page */
        .color-bar {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 8px;
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

        /* --- Header Nav Link Colors --- */
        div[data-testid="stColumn"] a[data-testid="stPageLink-NavLink"] {
            display: flex !important;
            justify-content: center !important;
            align-items: center !important;
        }

        </style>
        <div class="color-bar"></div>
    """,
    unsafe_allow_html=True,
    )

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

    url = "https://naciscdn.org/naturalearth/110m/cultural/ne_110m_admin_0_countries.zip"
    world = gpd.read_file(url)
    world = world[["NAME", "geometry"]]
    
    # remove antartica
    world = world[world["NAME"] != "Antarctica"]
    
    # load all files
    F03 = pd.read_csv("Data/WorldChamp/F/IM2003_F.csv")
    M03 = pd.read_csv("Data/WorldChamp/M/IM2003_M.csv")
    F04 = pd.read_csv("Data/WorldChamp/F/IM2004_F.csv")
    M04 = pd.read_csv("Data/WorldChamp/M/IM2004_M.csv")
    F05 = pd.read_csv("Data/WorldChamp/F/IM2005_F.csv")
    M05 = pd.read_csv("Data/WorldChamp/M/IM2005_M.csv")
    F06 = pd.read_csv("Data/WorldChamp/F/IM2006_F.csv")
    M06 = pd.read_csv("Data/WorldChamp/M/IM2006_M.csv")
    F07 = pd.read_csv("Data/WorldChamp/F/IM2007_F.csv")
    M07 = pd.read_csv("Data/WorldChamp/M/IM2007_M.csv")
    F08 = pd.read_csv("Data/WorldChamp/F/IM2008_F.csv")
    M08 = pd.read_csv("Data/WorldChamp/M/IM2008_M.csv")
    F09 = pd.read_csv("Data/WorldChamp/F/IM2009_F.csv")
    M09 = pd.read_csv("Data/WorldChamp/M/IM2009_M.csv")
    F10 = pd.read_csv("Data/WorldChamp/F/IM2010_F.csv")
    M10 = pd.read_csv("Data/WorldChamp/M/IM2010_M.csv")
    F11 = pd.read_csv("Data/WorldChamp/F/IM2011_F.csv")
    M11 = pd.read_csv("Data/WorldChamp/M/IM2011_M.csv")
    F12 = pd.read_csv("Data/WorldChamp/F/IM2012_F.csv")
    M12 = pd.read_csv("Data/WorldChamp/M/IM2012_M.csv")
    F13 = pd.read_csv("Data/WorldChamp/F/IM2013_F.csv")
    M13 = pd.read_csv("Data/WorldChamp/M/IM2013_M.csv")
    F14 = pd.read_csv("Data/WorldChamp/F/IM2014_F.csv")
    M14 = pd.read_csv("Data/WorldChamp/M/IM2014_M.csv")
    F15 = pd.read_csv("Data/WorldChamp/F/IM2015_F.csv")
    M15 = pd.read_csv("Data/WorldChamp/M/IM2015_M.csv")
    F16 = pd.read_csv("Data/WorldChamp/F/IM2016_F.csv")
    M16 = pd.read_csv("Data/WorldChamp/M/IM2016_M.csv")
    F17 = pd.read_csv("Data/WorldChamp/F/IM2017_F.csv")
    M17 = pd.read_csv("Data/WorldChamp/M/IM2017_M.csv")
    F18 = pd.read_csv("Data/WorldChamp/F/IM2018_F.csv")
    M18 = pd.read_csv("Data/WorldChamp/M/IM2018_M.csv")
    F19 = pd.read_csv("Data/WorldChamp/F/IM2019_F.csv")
    M19 = pd.read_csv("Data/WorldChamp/M/IM2019_M.csv")
    F22 = pd.read_csv("Data/WorldChamp/F/IM2022_F.csv")
    M22 = pd.read_csv("Data/WorldChamp/M/IM2022_M.csv")
    F23 = pd.read_csv("Data/WorldChamp/F/IM2023_F.csv")
    M23 = pd.read_csv("Data/WorldChamp/M/IM2023_M.csv")
    F24 = pd.read_csv("Data/WorldChamp/F/IM2024_F.csv")
    M24 = pd.read_csv("Data/WorldChamp/M/IM2024_M.csv")
    F25 = pd.read_csv("Data/WorldChamp/F/IM2025_F.csv")
    M25 = pd.read_csv("Data/WorldChamp/M/IM2025_M.csv")

    # Concatenate all collected dataframes into one
    combined_df = pd.concat([F03,M03,F04,M04,F05,M05,F06,M06,F07,M07,F08,M08,F09,M09,
                            F10,M10,F11,M11,F12,M12,F13,M13,F14,M14,F15,M15,F16,M16,
                            F17,M17,F18,M18,F19,M19,F22,M22,F23,M23,F24,M24,F25,M25])

    # Replace important names to be consistent with Geopandas database
    combined_df['Country'] = combined_df['Country'].replace('United States', 'United States of America')
    combined_df['Country'] = combined_df['Country'].replace('Bosnia and Herzegovina', 'Bosnia and Herz.')
    combined_df['Country'] = combined_df['Country'].replace('Argentinia', 'Argentina')
    combined_df['Country'] = combined_df['Country'].replace('SOUTH KOREA', 'South Korea')
    combined_df['Country'] = combined_df['Country'].replace('DEUTSHLAND', 'Germany')
    combined_df['Country'] = combined_df['Country'].replace('Russian Federation', 'Russia')
    combined_df['Country'] = combined_df['Country'].replace('Czech Republic', 'Czechia')

    #replace non matching with unknown
    countries_in_combined = combined_df['Country'].unique()
    countries_in_world = world['NAME'].unique()
    missing_countries = [country for country in countries_in_combined if country not in countries_in_world]
    combined_df['Country'] = combined_df['Country'].replace(missing_countries, 'Unknown')

    return combined_df
