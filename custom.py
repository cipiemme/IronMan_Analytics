import streamlit as st
import pandas as pd
import geopandas as gpd
import numpy as np
import os

# colors

site_red = "#CC262D"

ATHLETE_PALETTE = ["#10b981", "#3b82f6", "#f97316", "#a855f7"]

DISCIPLINE_COLORS = {
    "Swim":  "#18A3DD",   # swim blue
    "T1":    "#a78bfa",   # violet
    "Bike":  "#05A435",   # bike green
    "T2":    "#fb923c",   # orange
    "Run":   "#E8E812",   # run yellow
}

gr_gridcol = "#374151"
gr_axcol = "#374151"
gr_fontcol = "#9ca3af"

## interface functions

def top_menu():

    st.sidebar.title("ironMan Analytics")

    # define colors and dimensions of background
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

        /* Color accent background */
        .sfondo {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 10px;
            background: linear-gradient(
                90deg,
                #0F0000 0%,
                #0F0000 100%
            );
        }
        </style>
        <div class="sfondo"></div>
    """,
    unsafe_allow_html=True,
    )

    st.set_page_config(
        page_title="IronMan Analytics",
        layout="wide",
        initial_sidebar_state="collapsed"
        )

    pages = {
        "Home": st.Page("main.py"),
        "Race compare": st.Page("pages/race_comp.py", icon="🏠"),
        "Athlete compare": st.Page("pages/athlete_comp.py", icon="🏋️"),
        "Predictive model": st.Page("pages/strategy_analyzer.py", icon="🗺️"),
        "Strategy builder": st.Page("pages/strategy_builder.py", icon="🔮"),
        "Info": st.Page("pages/info.py", icon="ℹ️")
        }

    # Render top navigation using native columns
    with st.container(height="stretch", width="stretch", border=False):
        headerNavLinks = st.columns([ 1, 1, 1, 1, .5])
        with headerNavLinks[0]: st.page_link(pages["Race compare"], label="Race Intelligence Dashboard", use_container_width=True)
        with headerNavLinks[1]: st.page_link(pages["Athlete compare"], label="Athlete Comparator", use_container_width=True)
        with headerNavLinks[2]: st.page_link(pages["Predictive model"], label="Predictive Time Model", use_container_width=True)
        with headerNavLinks[3]: st.page_link(pages["Strategy builder"], label="Race Strategy Builder", use_container_width=True)
        with headerNavLinks[4]: st.page_link(pages["Info"], label="Info", use_container_width=True)


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


## working functions

# load functions
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

def load_data(DATA_DIR, YEARS) -> pd.DataFrame:
    frames = []
    for year in YEARS:
        for code in ("M", "F"):
            path = os.path.join(DATA_DIR, f"IM{year}_{code}.csv")
            if not os.path.exists(path):
                continue
            try:
                df = pd.read_csv(path, low_memory=False)
                df["Year"] = year
                df["FileGender"] = code
                frames.append(df)
            except Exception as e:
                st.warning(f"Could not read {path}: {e}")

    if not frames:
        st.error(
            "No CSV files found. Place IM2003_F.csv … IM2026_M.csv "
            f"in: {DATA_DIR}"
        )
        st.stop()

    raw = pd.concat(frames, ignore_index=True)

    # ── Parse times to seconds ──────────────────────────────────────────────
    time_map = {
        "Overall Time":       "Overall_sec",
        "Swim Time":          "Swim_sec",
        "Bike Time":          "Bike_sec",
        "Run Time":           "Run_sec",
        "Transition 1 Time":  "T1_sec",
        "Transition 2 Time":  "T2_sec",
    }
    for col, sec_col in time_map.items():
        if col in raw.columns:
            raw[sec_col] = raw[col].apply(parse_time)

    # ── Keep finishers with valid overall time ───────────────────────────────
    raw = raw[raw["Finish"] == "FIN"].copy()
    raw = raw[raw["Overall_sec"].notna() & (raw["Overall_sec"] > 0)].copy()

    # ── Derive gender from Division prefix (more reliable than Gender col) ───
    def div_gender(div):
        d = str(div).upper()
        if d.startswith("F"):
            return "Female"
        if d.startswith("M"):
            return "Male"
        return "Unknown"

    raw["Gender_clean"] = raw["Division"].apply(div_gender)

    # ── Normalise age-group labels  ──────────────────────────────────────────
    def clean_div(div):
        d = str(div).strip()
        if d in ("MPRO", "FPRO"):
            return "PRO"
        return d.replace("M", "").replace("F", "").strip() if d not in ("Male", "Female") else d

    raw["AgeGroup"] = raw["Division"].apply(clean_div)

    # ── Derived numeric columns ──────────────────────────────────────────────
    raw["Total_min"] = raw["Overall_sec"] / 60
    raw["Total_hr"]  = raw["Overall_sec"] / 3600

    # ── Percentile within year × gender × age-group ─────────────────────────
    # (computed lazily per query to avoid huge upfront cost)

    raw.reset_index(drop=True, inplace=True)
    return raw

# gender select load filter
def gen_sel() -> str:
    sel_gender = st.radio( "Select gender", ["Male", "Female"])
    # Directory for the CSV files
    if sel_gender == "Male":
        return "Data/WorldChamp/M"
    else:
        return "Data/WorldChamp/F"


# time parsers
def parse_time(t) -> float:
    """HH:MM:SS → seconds. Returns NaN for zeros / invalid / DNF."""
    s = str(t).strip() if not pd.isna(t) else ""
    if s in ("", "00:0:0", "0:0:0", "nan"):
        return np.nan
    try:
        parts = s.split(":")
        if len(parts) == 3:
            total = int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])
        elif len(parts) == 2:
            total = int(parts[0]) * 60 + int(parts[1])
        else:
            return np.nan
        return float(total) if total > 0 else np.nan
    except Exception:
        return np.nan

def hms(seconds) -> str:
    """seconds → H:MM:SS"""
    if pd.isna(seconds):
        return "N/A"
    seconds = int(round(seconds))
    h = seconds // 3600
    m = (seconds % 3600) // 60
    s = seconds % 60
    return f"{h}:{m:02d}:{s:02d}"

def hm(seconds) -> str:
    """seconds → H:MM"""
    if pd.isna(seconds):
        return "N/A"
    seconds = int(round(seconds))
    h = seconds // 3600
    m = (seconds % 3600) // 60
    return f"{h}:{m:02d}"


# pace per km
def ppk(seconds, km) -> str:
    """seconds for a leg → MM:SS/km pace string"""
    if pd.isna(seconds) or km == 0:
        return "N/A"
    pace = seconds / km
    m = int(pace // 60)
    s = int(round(pace % 60))
    return f"{m}:{s:02d}/km"


# speed function
def speed_kmh(seconds, km) -> str:
    if pd.isna(seconds) or seconds == 0:
        return "N/A"
    return f"{(km / seconds * 3600):.1f} km/h"


# percentile rank
def perc_rank(value, series) -> float:
    """Percentile of 'value' within 'series' (lower time → higher percentile)."""
    valid = series.dropna()
    if len(valid) == 0:
        return 50.0
    return round(float((valid > value).sum() / len(valid) * 100), 1)




