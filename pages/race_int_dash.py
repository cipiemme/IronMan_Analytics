import streamlit as st
from custom import top_menu, bottom_head, hms, hm, load_data, DISCIPLINE_COLORS, ATHLETE_PALETTE, gr_gridcol, gr_fontcol

import numpy as np
import plotly.express as px
import plotly.graph_objects as go


top_menu()

# Folder that contains the CSV files. Change if needed.
DATA_DIR = {"Data/WorldChamp/M", "Data/WorldChamp/F"}

YEARS = list(range(2003, 2026))          # 2003 – 2025

# ─── Data Loading ─────────────────────────────────────────────────────────────

df = load_data(DATA_DIR, YEARS)

##########

st.header("Race Intelligence Dashboard")

if df.empty:
    st.warning("No data matches the current filters.")
else:
    # ── KPI Cards ────────────────────────────────────────────────────────
    n_fin     = len(df)
    avg_total = df["Overall_sec"].mean()
    best_time = df["Overall_sec"].min()
    worst_time= df["Overall_sec"].max()
    avg_swim  = df["Swim_sec"].dropna().mean()
    avg_bike  = df["Bike_sec"].dropna().mean()
    avg_run   = df["Run_sec"].dropna().mean()
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Finishers",  f"{n_fin:,}")
    c2.metric("Average Finish",   hms(avg_total))
    c3.metric("Course Record",    hms(best_time))
    c4.metric("Slowest Finisher", hms(worst_time))
    st.markdown("---")
    # ── Average split composition ─────────────────────────────────────
    st.subheader("Average Split Composition")
    splits = {
        "Swim": avg_swim,
        "T1":   df["T1_sec"].dropna().mean(),
        "Bike": avg_bike,
        "T2":   df["T2_sec"].dropna().mean(),
        "Run":  avg_run,
    }
    total_split = sum(v for v in splits.values() if not np.isnan(v))
    split_pct = {k: (v / total_split * 100 if not np.isnan(v) else 0) for k, v in splits.items()}
    fig_split = go.Figure()
    x_pos = 0
    for seg, pct in split_pct.items():
        fig_split.add_trace(go.Bar(
            name=seg,
            x=[pct],
            y=["Avg Finisher"],
            orientation="h",
            marker_color=DISCIPLINE_COLORS[seg],
            text=f"{seg}<br>{hms(splits[seg])}<br>({pct:.1f}%)",
            textposition="inside",
            insidetextanchor="middle",
            hovertemplate=f"<b>{seg}</b><br>Avg: {hms(splits[seg])}<br>{pct:.1f}% of race<extra></extra>",
        ))

    fig_split.update_layout(
        barmode="stack",
        height=100,
        margin=dict(l=0, r=0, t=0, b=0),
        showlegend=False,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(showticklabels=False, showgrid=False, zeroline=False),
        yaxis=dict(showticklabels=False, showgrid=False),
    )

    st.plotly_chart(fig_split, width="stretch")

    st.markdown("---")
    col_hist, col_bench = st.columns([1.5, 1])

    # ── Finish-Time Histogram ────────────────────────────────────────────
    with col_hist:
        st.subheader("Finish Time Distribution")
        bins = st.slider("Histogram bins", 20, 80, 40, key="hist_bins")
        fig_hist = px.histogram(
            df,
            x="Total_hr",
            nbins=bins,
            labels={"Total_hr": "Finish Time (hours)"},
            color_discrete_sequence=["#10b981"],
        )
        fig_hist.update_traces(
            hovertemplate="Time: %{x:.2f} hrs<br>Count: %{y}<extra></extra>"
        )
        fig_hist.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(17,24,39,0.6)",
            font_color = gr_fontcol,
            margin=dict(l=10, r=10, t=10, b=10),
            xaxis=dict(gridcolor = gr_gridcol),
            yaxis=dict(title="Athletes", gridcolor = gr_gridcol)
        )
        st.plotly_chart(fig_hist, width="stretch")
    # ── Age Group Benchmarks ─────────────────────────────────────────────
    with col_bench:
        st.subheader("Age Group Benchmarks")
        ag_stats = (
            df.groupby("AgeGroup")["Overall_sec"]
            .agg(["mean", "median", "min", "count"])
            .reset_index()
            .rename(columns={"mean": "Avg", "median": "Median",
                              "min": "Best", "count": "N"})
            .sort_values("Avg")
        )
        ag_stats = ag_stats[ag_stats["N"] >= 5]  # At least 5 finishers
        fig_ag = go.Figure()
        fig_ag.add_trace(go.Bar(
            y=ag_stats["AgeGroup"],
            x=ag_stats["Avg"] / 3600,
            orientation="h",
            name="Average",
            marker_color="#10b981",
            text=[hm(v) for v in ag_stats["Avg"]],
            textposition="outside",
            hovertemplate="<b>%{y}</b><br>Avg: %{text}<br>N=%{customdata}<extra></extra>",
            customdata=ag_stats["N"],
        ))
        fig_ag.add_trace(go.Scatter(
            y=ag_stats["AgeGroup"],
            x=ag_stats["Best"] / 3600,
            mode="markers",
            name="Best",
            marker=dict(color="#fbbf24", size=8, symbol="diamond"),
            hovertemplate="<b>%{y}</b> Best: %{text}<extra></extra>",
            text=[hm(v) for v in ag_stats["Best"]],
        ))
        fig_ag.update_layout(
            height=400,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(17,24,39,0.6)",
            font_color = gr_fontcol,
            margin=dict(l=10, r=10, t=10, b=10),
            xaxis=dict(title="Hours", gridcolor = gr_gridcol),
            yaxis=dict(gridcolor = gr_gridcol),
            legend=dict(orientation="h", y=1.05),
        )
        st.plotly_chart(fig_ag, width="stretch")

    st.markdown("---")

    # ── Year-over-Year Trends ────────────────────────────────────────────

    st.subheader("Year-over-Year Performance Trends")
    yearly = (
        df.groupby("Year")
        .agg(
            Avg_Total=("Overall_sec", "mean"),
            Avg_Swim=("Swim_sec", "mean"),
            Avg_Bike=("Bike_sec", "mean"),
            Avg_Run=("Run_sec", "mean"),
            Finishers=("Overall_sec", "count"),
        )
        .reset_index()
    )
    col_trend_l, col_trend_r = st.columns([3, 1])
    with col_trend_l:
        fig_trend = go.Figure()
        for seg, col_key in [("Swim", "Avg_Swim"), ("Bike", "Avg_Bike"), ("Run", "Avg_Run")]:
            fig_trend.add_trace(go.Scatter(
                x=yearly["Year"],
                y=yearly[col_key] / 3600,
                mode="lines+markers",
                name=seg,
                line=dict(color=DISCIPLINE_COLORS[seg], width=2),
                hovertemplate=f"<b>{seg}</b> %{{x}}: %{{text}}<extra></extra>",
                text=[hm(v) for v in yearly[col_key]],
            ))
        fig_trend.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(17,24,39,0.6)",
            font_color = gr_fontcol,
            margin=dict(l=10, r=10, t=10, b=10),
            xaxis=dict(title="Year", dtick=1, gridcolor = gr_gridcol),
            yaxis=dict(title="Hours (avg)", gridcolor = gr_gridcol),
            legend=dict(orientation="h", y=1.05),
        )
        st.plotly_chart(fig_trend, width="stretch")
    with col_trend_r:
        st.markdown("#### Field Size")
        for _, row in yearly.iterrows():
            st.metric(str(int(row["Year"])), f"{int(row['Finishers']):,} finishers")



bottom_head()