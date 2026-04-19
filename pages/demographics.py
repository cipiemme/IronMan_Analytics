import streamlit as st
from custom import top_menu, bottom_head, load_merge

import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt

top_menu()

dem = load_merge()

# how many from each category are present in dataset
divisions = dem['Division'].unique()
cat_counts = dem['Division'].value_counts().sort_index()
cat_counts_df = pd.DataFrame([divisions, cat_counts])
cat_counts_df = cat_counts_df.transpose()

#create histogram plot
dem_cat_hist_fig = px.histogram(cat_counts_df, x=0, y=1,
                                labels={
                                    "0": "Divisions",
                                    "1": "# of participants"}
                                    )

st.plotly_chart(dem_cat_hist_fig)

st.write(cat_counts_df)


bottom_head()

