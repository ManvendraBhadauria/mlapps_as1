import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px


@st.cache_data
def make_data(data):
    if data is None or data.empty:
        return pd.DataFrame()
    else:
        temp = data.groupby(["Manufacturer"])[["Volume", "Value"]].sum().reset_index()
        return pd.DataFrame(temp)


@st.cache_data
def make_graph(filtered_data, date_min, date_max):
    top_manufacturers = (
        filtered_data.groupby("Manufacturer")["Volume"].sum().nlargest(5).index
    )

    date_range = pd.date_range(start=date_min, end=date_max, freq="MS").strftime(
        "%Y-%m"
    )

    filtered_data_top5 = filtered_data[
        filtered_data["Manufacturer"].isin(top_manufacturers)
    ]

    filtered_data_top5 = (
        filtered_data_top5.groupby(["Manufacturer", pd.Grouper(key="Date", freq="MS")])
        .sum()
        .reset_index()
        .pivot(index="Date", columns="Manufacturer", values="Volume")
        .fillna(0)
        .reindex(date_range)
        .reset_index()
    )

    # Plotly chart creation with Month on the X-axis
    fig = px.line(
        filtered_data_top5,
        x="index",
        y=top_manufacturers,
        # title="Top 5 Manufacturers by Volume",
    )
    fig.update_layout(
        xaxis_title="Month",
        yaxis_title="Volume",
        xaxis={"type": "category"},
        width=1000,
    )

    return fig
