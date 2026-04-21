import streamlit as st
from custom import top_menu, bottom_head, parse_time, hms, hm, ppk, speed_kmh, perc_rank 

import os
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

top_menu()

# colors

ATHLETE_PALETTE = ["#10b981", "#3b82f6", "#f97316", "#a855f7"]
DISCIPLINE_COLORS = {
    "Swim":  "#18A3DD",   # swim blue
    "T1":    "#a78bfa",   # violet
    "Bike":  "#05A435",   # bike green
    "T2":    "#fb923c",   # orange
    "Run":   "#E8E812",   # run yellow
}

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















st.header("Race Strategy Builder")
st.caption(
    "Set a target finish time and let the builder reverse-engineer "
    "optimal splits from real race data."
)
col_sb_l, col_sb_r = st.columns([1, 2])
with col_sb_l:
    st.markdown("#### Athlete Profile")
    sb_gender = st.selectbox("Gender", ["Male", "Female"], key="sb_gender")
    sb_ag_opts = sorted(
        df_all[df_all["Gender_clean"] == sb_gender]["AgeGroup"].dropna().unique().tolist()
    )
    sb_ag = st.selectbox("Age Group", sb_ag_opts if sb_ag_opts else ["PRO"], key="sb_ag")
    target_str = st.text_input("Target Finish Time (HH:MM:SS)", "10:00:00", key="sb_target")
    target_sec = parse_time(target_str)
    sb_weight = st.slider("Athlete weight (kg) – for power estimates", 50, 110, 75, key="sb_weight")
    st.markdown("---")
    st.markdown("#### Strategy Bias")
    swim_bias = st.slider("Swim effort vs. median (%)", -20, 20, 0, key="sb_swim_bias",
                          help="Negative = faster than median for this segment's proportion")
    bike_bias = st.slider("Bike effort vs. median (%)", -20, 20, 0, key="sb_bike_bias")
    run_bias  = st.slider("Run effort vs. median (%)",  -20, 20, 0, key="sb_run_bias")
with col_sb_r:
    if pd.isna(target_sec) or target_sec <= 0:
        st.warning("Enter a valid target time (HH:MM:SS) on the left.")
    else:
        ref_sb = df_all[
            (df_all["Gender_clean"] == sb_gender) &
            (df_all["AgeGroup"] == sb_ag)
        ].dropna(subset=["Overall_sec", "Swim_sec", "Bike_sec", "Run_sec"])
        # ── Calculate split targets ───────────────────────────────
        # Use median proportions from reference group, then scale to target
        if ref_sb.empty:
            st.warning("No reference data for this gender/age group combination.")
        else:
            # Median segment proportions (excluding transitions in proportion calc)
            med_swim = ref_sb["Swim_sec"].median()
            med_bike = ref_sb["Bike_sec"].median()
            med_run  = ref_sb["Run_sec"].median()
            med_t1   = ref_sb["T1_sec"].dropna().median()
            med_t2   = ref_sb["T2_sec"].dropna().median()
            # Fix transitions (not scaled with speed)
            t1_target = med_t1 if not np.isnan(med_t1) else 210
            t2_target = med_t2 if not np.isnan(med_t2) else 150
            # Remaining time for SBR after transitions
            sbr_target = target_sec - t1_target - t2_target
            # Proportions with bias
            denom = med_swim + med_bike + med_run
            p_swim = (med_swim / denom) * (1 + swim_bias / 100)
            p_bike = (med_bike / denom) * (1 + bike_bias / 100)
            p_run  = (med_run  / denom) * (1 + run_bias  / 100)
            total_p = p_swim + p_bike + p_run
            swim_target = sbr_target * (p_swim / total_p)
            bike_target = sbr_target * (p_bike / total_p)
            run_target  = sbr_target * (p_run  / total_p)
            calc_total = swim_target + t1_target + bike_target + t2_target + run_target
            # ── Feasibility vs. reference group ──────────────────────
            pct_vs_ag = perc_rank(target_sec, ref_sb["Overall_sec"])
            achievers = (ref_sb["Overall_sec"] <= target_sec).sum()
            pct_achievers = achievers / len(ref_sb) * 100
            st.markdown("#### Projected Split Plan")
            st.markdown(
                f"<div style='font-size:2.5rem;font-weight:700;color:#10b981;text-align:center'>"
                f"{hms(calc_total)}</div>"
                f"<div style='text-align:center;color:#6b7280;font-size:0.85em'>"
                f"Projected finish · Target was {hms(target_sec)}</div>",
                unsafe_allow_html=True,
            )
            st.markdown("")
            # ── Strategy table ────────────────────────────────────────
            swim_speed_mh = (3.8 / swim_target * 3600) * 1000  # m/h
            bike_speed    = 180 / bike_target * 3600
            run_pace_km   = run_target / 42.195
            # Rough power estimate
            v_ms = bike_speed / 3.6
            power_w = int(0.3 * v_ms ** 3 + 35 + (sb_weight - 70) * 0.5)
            strategy_df = pd.DataFrame([
                {
                    "Segment":      "🏊 Swim",
                    "Target Time":  hms(swim_target),
                    "Metric":       f"{ppk(swim_target, 3.8)}",
                    "vs. Median":   f"{((swim_target - med_swim) / med_swim * 100):+.1f}%",
                    "Percentile":   f"Top {100 - perc_rank(swim_target, ref_sb['Swim_sec']):.0f}%",
                },
                {
                    "Segment":      "⚡ T1",
                    "Target Time":  hms(t1_target),
                    "Metric":       "—",
                    "vs. Median":   f"{((t1_target - med_t1) / med_t1 * 100 if not np.isnan(med_t1) else 0):+.1f}%",
                    "Percentile":   "—",
                },
                {
                    "Segment":      "🚴 Bike",
                    "Target Time":  hms(bike_target),
                    "Metric":       f"{speed_kmh(bike_target, 180)} · ~{power_w}W",
                    "vs. Median":   f"{((bike_target - med_bike) / med_bike * 100):+.1f}%",
                    "Percentile":   f"Top {100 - perc_rank(bike_target, ref_sb['Bike_sec']):.0f}%",
                },
                {
                    "Segment":      "⚡ T2",
                    "Target Time":  hms(t2_target),
                    "Metric":       "—",
                    "vs. Median":   f"{((t2_target - med_t2) / med_t2 * 100 if not np.isnan(med_t2) else 0):+.1f}%",
                    "Percentile":   "—",
                },
                {
                    "Segment":      "🏃 Run",
                    "Target Time":  hms(run_target),
                    "Metric":       f"{ppk(run_target, 42.195)}",
                    "vs. Median":   f"{((run_target - med_run) / med_run * 100):+.1f}%",
                    "Percentile":   f"Top {100 - perc_rank(run_target, ref_sb['Run_sec']):.0f}%",
                },
            ])
            st.dataframe(strategy_df, width="stretch", hide_index=True)
            # ── Feasibility ───────────────────────────────────────────
            st.markdown("#### Feasibility Analysis")
            fa1, fa2, fa3 = st.columns(3)
            fa1.metric(
                "Athletes who hit this target",
                f"{achievers:,} / {len(ref_sb):,}",
                delta=f"{pct_achievers:.1f}% of {sb_ag}",
            )
            fa2.metric("Field Percentile", f"Top {100 - pct_vs_ag:.0f}%")
            fa3.metric("Reference Field", f"{len(ref_sb):,} athletes")
            # ── Visual split bar ──────────────────────────────────────
            fig_plan = go.Figure()
            plan_segs = [
                ("Swim", swim_target, "#38bdf8"),
                ("T1",   t1_target,   "#a78bfa"),
                ("Bike", bike_target, "#34d399"),
                ("T2",   t2_target,   "#fb923c"),
                ("Run",  run_target,  "#f87171"),
            ]
            plan_med = [
                ("Swim", med_swim, "#38bdf8"),
                ("T1",   med_t1 if not np.isnan(med_t1) else 0, "#a78bfa"),
                ("Bike", med_bike, "#34d399"),
                ("T2",   med_t2 if not np.isnan(med_t2) else 0, "#fb923c"),
                ("Run",  med_run,  "#f87171"),
            ]
            for (seg, val, col) in plan_segs:
                fig_plan.add_trace(go.Bar(
                    name=seg,
                    x=["Your Plan"],
                    y=[val / 60],
                    marker_color=col,
                    text=hm(val),
                    textposition="inside",
                    hovertemplate=f"<b>{seg}</b>: {hm(val)}<extra></extra>",
                ))
            for (seg, val, col) in plan_med:
                fig_plan.add_trace(go.Bar(
                    name=f"{seg} (Median)",
                    x=["Age Group Median"],
                    y=[val / 60 if not pd.isna(val) else 0],
                    marker_color=col,
                    marker_pattern_shape="/",
                    text=hm(val),
                    textposition="inside",
                    hovertemplate=f"<b>{seg} median</b>: {hm(val)}<extra></extra>",
                    showlegend=False,
                ))
            fig_plan.update_layout(
                barmode="stack",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(17,24,39,0.6)",
                font_color="#9ca3af",
                height=320,
                xaxis=dict(gridcolor="#374151"),
                yaxis=dict(title="Minutes", gridcolor="#374151"),
                legend=dict(orientation="h", y=1.08),
                margin=dict(l=10, r=10, t=10, b=10),
            )
            st.plotly_chart(fig_plan, width="stretch")
            # ── Coaching insights ──────────────────────────────────────
            st.markdown("#### Coaching Insights")
            insights = []
            if swim_target < med_swim:
                insights.append(("✅", "Swim", "You're targeting a swim faster than your age group median. Conserve energy for the bike and run."))
            else:
                insights.append(("⚠️", "Swim", "Your swim target is slower than the median. A faster swim could improve your position early in the race."))
            if bike_target < med_bike * 0.95:
                insights.append(("⚠️", "Bike", "You're targeting a significantly faster bike than median. Be cautious of overbiker syndrome – a hard bike often leads to a slow run."))
            elif bike_target < med_bike:
                insights.append(("✅", "Bike", "Bike target is slightly faster than median – a solid position to hold."))
            else:
                insights.append(("ℹ️", "Bike", "Conservative bike target leaves energy for a strong run."))
            if run_target < med_run:
                insights.append(("✅", "Run", "Strong run target – if your legs are fresh off the bike, this is achievable."))
            else:
                insights.append(("ℹ️", "Run", "Run target is at or above median. Focus on nutrition and pacing on the bike to maximise run potential."))
            for emoji, seg, text in insights:
                st.markdown(
                    f"<div style='border-left:3px solid #374151;padding:8px 12px;"
                    f"margin-bottom:8px;color:#d1d5db'>"
                    f"<b>{emoji} {seg}:</b> {text}</div>",
                    unsafe_allow_html=True,
                )











bottom_head()