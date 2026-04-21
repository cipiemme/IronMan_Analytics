import streamlit as st
from custom import top_menu, bottom_head, parse_time, hms, hm, speed_kmh, DISCIPLINE_COLORS, ATHLETE_PALETTE

import os
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go


top_menu()


# Folder that contains the CSV files. Change if needed.
DATA_DIR = "Data/WorldChamp/M"

YEARS = list(range(2003, 2026))          # 2003 – 2025

##############
    #FUNCTIONS

# ─── Data Loading ─────────────────────────────────────────────────────────────

@st.cache_data(show_spinner="Loading race data …")
def load_data() -> pd.DataFrame:
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


df_all = load_data()

##########

# ─── Sidebar – Global Filters ─────────────────────────────────────────────────

with st.sidebar:
    st.markdown("## ⚙️ Global Filters")
    sel_years = st.multiselect(
        "Year(s)",
        options=YEARS,
        default=YEARS,
    )
    sel_gender = st.selectbox(
        "Gender",
        ["All", "Male", "Female"],
        index=0,
    )
    all_ag = sorted(df_all["AgeGroup"].dropna().unique().tolist())
    sel_ag = st.multiselect(
        "Age Group(s)",
        options=all_ag,
        default=[],
        placeholder="All age groups",
    )
    st.markdown("---")
    st.caption("Ironman World Championship • 2003 – 2025")

# Apply global filters
def apply_filters(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    if sel_years:
        out = out[out["Year"].isin(sel_years)]
    if sel_gender != "All":
        out = out[out["Gender_clean"] == sel_gender]
    if sel_ag:
        out = out[out["AgeGroup"].isin(sel_ag)]
    return out

df = apply_filters(df_all)



##########


st.header("Pacing Strategy Analyzer")
st.caption(
    "Visualise bike-vs-run pacing trade-offs. "
    "Overbiker: fast bike → slow run. Underrunner: fast run relative to bike."
    )

pa_df = df.dropna(subset=["Bike_sec", "Run_sec"]).copy()
if pa_df.empty:
    st.warning("No valid Bike/Run data for current filters.")
else:
    col_pa_l, col_pa_r = st.columns([1, 3])
    with col_pa_l:
        st.markdown("#### Filters")
        ag_options = ["All"] + sorted(pa_df["AgeGroup"].dropna().unique().tolist())
        pa_ag = st.selectbox("Age Group", ag_options, key="pa_ag")
        pa_year = st.selectbox(
            "Year",
            ["All"] + [str(y) for y in sorted(pa_df["Year"].unique())],
            key="pa_year",
        )
        sample_n = st.slider("Max points plotted", 200, 2000, 800, 100, key="pa_n")
        if pa_ag != "All":
            pa_df = pa_df[pa_df["AgeGroup"] == pa_ag]
        if pa_year != "All":
            pa_df = pa_df[pa_df["Year"] == int(pa_year)]
        bike_med = pa_df["Bike_sec"].median()
        run_med  = pa_df["Run_sec"].median()
        def pacing_label(row):
            b_fast = row["Bike_sec"] < bike_med
            r_fast = row["Run_sec"]  < run_med
            if b_fast and r_fast:
                return "Elite"
            if b_fast and not r_fast:
                return "Overbiker"
            if not b_fast and r_fast:
                return "Strong Runner"
            return "Conservative"
        pa_df["PacingType"] = pa_df.apply(pacing_label, axis=1)
        label_counts = pa_df["PacingType"].value_counts()
        st.markdown("#### Pacing Breakdown")
        pacing_colors = {
            "Elite":         "#fbbf24",
            "Overbiker":     "#ef4444",
            "Strong Runner": "#10b981",
            "Conservative":  "#6b7280",
        }
        for label, cnt in label_counts.items():
            pct = cnt / len(pa_df) * 100
            color = pacing_colors.get(label, "#9ca3af")
            st.markdown(
                f"<div style='display:flex;justify-content:space-between;"
                f"border-left:3px solid {color};padding-left:8px;margin-bottom:6px'>"
                f"<span style='color:{color}'>{label}</span>"
                f"<span style='color:#9ca3af'>{pct:.0f}%</span></div>",
                unsafe_allow_html=True,
            )
    with col_pa_r:
        sample = pa_df.sample(min(sample_n, len(pa_df)), random_state=42)
        fig_sc = go.Figure()
        for label, grp in sample.groupby("PacingType"):
            fig_sc.add_trace(go.Scatter(
                x=grp["Bike_sec"] / 3600,
                y=grp["Run_sec"]  / 3600,
                mode="markers",
                name=label,
                marker=dict(
                    color=pacing_colors.get(label, "#9ca3af"),
                    size=6,
                    opacity=0.7,
                ),
                hovertemplate=(
                    "<b>%{text}</b><br>"
                    "Bike: %{customdata[0]}<br>"
                    "Run: %{customdata[1]}<extra></extra>"
                ),
                text=grp["Name"].fillna("Unknown"),
                customdata=list(zip(
                    [hm(v) for v in grp["Bike_sec"]],
                    [hm(v) for v in grp["Run_sec"]],
                )),
            ))
        # Quadrant lines
        fig_sc.add_vline(x=bike_med / 3600, line_dash="dash", line_color="#4b5563",
                         annotation_text="Bike Median", annotation_font_color="#6b7280")
        fig_sc.add_hline(y=run_med / 3600, line_dash="dash", line_color="#4b5563",
                         annotation_text="Run Median", annotation_font_color="#6b7280")
        fig_sc.update_layout(
            title="Bike vs Run Scatter – Pacing Quadrants",
            xaxis_title="Bike Time (hours)",
            yaxis_title="Run Time (hours)",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(17,24,39,0.6)",
            font_color="#9ca3af",
            xaxis=dict(gridcolor="#374151"),
            yaxis=dict(gridcolor="#374151"),
            legend=dict(orientation="h", y=1.08),
            height=500,
        )
        st.plotly_chart(fig_sc, width="stretch")
    # ── Swim-to-Bike-to-Run pacing funnel ─────────────────────────────
    st.subheader("Leg-Time Correlation: Does a fast swim lead to a faster finish?")
    corr_seg = st.selectbox(
        "Select discipline to correlate with finish time",
        ["Swim_sec", "Bike_sec", "Run_sec"],
        format_func=lambda x: x.replace("_sec", ""),
        key="corr_seg",
    )
    corr_df = pa_df.dropna(subset=[corr_seg, "Overall_sec"])
    corr_df = corr_df.sample(min(1000, len(corr_df)), random_state=1)
    fig_corr = px.scatter(
        corr_df,
        x=corr_df[corr_seg] / 3600,
        y=corr_df["Overall_sec"] / 3600,
        color="AgeGroup",
        hover_name="Name",
        trendline="ols",
        labels={
            "x": f"{corr_seg.replace('_sec','')} Time (hrs)",
            "y": "Finish Time (hrs)",
        },
        color_discrete_sequence=px.colors.qualitative.Set2,
    )
    fig_corr.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(17,24,39,0.6)",
        font_color="#9ca3af",
        height=380,
        xaxis=dict(gridcolor="#374151"),
        yaxis=dict(gridcolor="#374151"),
    )
    st.plotly_chart(fig_corr, width="stretch")




bottom_head()