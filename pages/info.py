import streamlit as st
from custom import top_menu, bottom_head

top_menu()

# ── Header Section ───────────────────────────────────────────────────

# ── Sources ────────────────────────────────────────
st.header("🗄️ The Data Engine")
st.write("In this page there will be info about the project")
col1, col2 = st.columns([1, 2])

with col1:
    st.image("https://gitlab.com/uploads/-/system/project/avatar/6722790/favicon.png", width=200)

with col2:
    st.subheader("Data Source: ")
    st.write("""
        At the heart of  
    """)

st.markdown("---")

# ── Reading the Charts ───────────────────────────────────────────────
st.header("📊 Chart Reading 101")
st.write("If the colors and lines look confusing, here’s a quick field guide to the analytics:")

with st.expander("🛡️ Radar Charts: The Strength Geometry"):
    st.write("""
        - **Outer Points**: Represent the absolute maximums or best coefficients. 
        - **Area**: The bigger the shape, the more "balanced" the athlete. 
        - **Z-Ordering**: In our 1v1 tool, we always put the smaller shape on top 
          so you can see how much further you need to grow to engulf your competition!
    """)

with st.expander("🗺️ Heatmaps: Searching the Ocean"):
    st.write("""
        - **Brightness (Yellow/Green)**: Areas of high population density. Most people live here.
        - **Darkness (Purple)**: The "Quiet Zones." If you see a star marker here at a high Total, 
          you're looking at a world-class outlier (a 'Freak' in our Sandbox terms).
    """)

with st.expander("📈 Trend Path: The Road to White Lights"):
    st.write("""
        - **The Staircase**: Shows your recommended attempt progression.
        - **The Shaded Aura**: This is the 'Safe Zone'—representing **±1 Standard Deviation** 
          of thousands of successful lifters in your weight class. Straying too far outside 
          it might mean your opener is too heavy or your 2nd is too conservative.
    """)

bottom_head()