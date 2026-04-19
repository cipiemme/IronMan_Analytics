import streamlit as st
import custom as c

c.top_menu()

# ── Header Section ───────────────────────────────────────────────────

# ── Sources ────────────────────────────────────────
st.header("🗄️ The Database")
col1, col2 = st.columns([1, 2])

with col1:
    st.image("https://gitlab.com/uploads/-/system/project/avatar/6722790/favicon.png", width=200)

with col2:
    st.subheader("Data Source: ")
    st.write("All of the data analyzed in this site was taken from publicly available sources")

st.markdown("---")

# ── Reading the Charts ───────────────────────────────────────────────
st.header("📊 Chart Reading 101")
st.write("If the colors and lines look confusing, here’s a quick field guide to the analytics:")

with st.expander("Color guide"):
        st.write("""
                - **:color[Red]{foreground="#CE0B2D"}**, main color of the website, taken from IronMan branding,
                - **:color[Blue]{foreground="#18A3DD"}**, used to represent the data regarding the swimming sections,
                - **:color[Green]{foreground="#05A435"}**, used to visualize the data of the cycling segment,
                - **:color[Yellow]{foreground="#E8E812"}**, used to present the data concerning the running segment.
    """, unsafe_allow_html=True)

c.bottom_head()