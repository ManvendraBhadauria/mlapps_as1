from pathlib import Path as pt

import pandas as pd
import streamlit as st

from src.deepdive_plotter import (
    create_bar_chart,
    create_line_chart,
    create_line_chart_bottom,
    create_pie_chart,
    create_trend_line_value,
    create_trend_line_vol,
)
from src.delta_calculator import delta_cal
from src.pages_style import css_pages
from src.preprocessor import preprocess

st.set_page_config(
    "Deep Dive",
    page_icon="🥽",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(css_pages, unsafe_allow_html=True)

home_path = pt.cwd()
df = pd.read_csv(home_path / pt("data/Input_Sales_Data_v2.csv"), index_col="Id")
data = pd.DataFrame(preprocess(df))

with st.container():
    st.markdown(
        "<h1 style='color: grey; text-align: center;' id='titleh1'>Deep Dive</h1>",
        unsafe_allow_html=True,
    )

with st.container():
    cat_col, manu_col, brand_col = st.columns(3, gap="large")
    selected_cate = cat_col.selectbox("", options=data["Category"].unique())
    data_cate = data[(data["Category"] == selected_cate)]
    selected_manu = manu_col.selectbox("", options=data_cate["Manufacturer"].unique())
    data_manu = data_cate[data_cate["Manufacturer"] == selected_manu]
    selected_brand = brand_col.selectbox("", options=data_manu["Brand"].unique())
    filtered_data = data_manu[data_manu["Brand"] == selected_brand]

total_sales = data["Value"].sum()


ytd_vol_sales_delta, ytd_val_sales_delta = delta_cal(filtered_data)
st.markdown("---")
with st.container():
    vol_sales_col, val_sales_col, mark_share_col, num_sku_col = st.columns(4)
    ytd_vol_sales = vol_sales_col.metric(
        "**YTD Volume Sales**",
        value=filtered_data["Volume"].sum(),
        delta=ytd_vol_sales_delta,
    )
    ytd_val_sales = val_sales_col.metric(
        "**YTD $ Sales**",
        value=filtered_data["Value"].sum(),
        delta=ytd_val_sales_delta,
    )
    ytd_market_share = mark_share_col.metric(
        "**YTD Market Share**",
        value=(filtered_data["Value"].sum() / total_sales) * 100,
    )

    num_sku = num_sku_col.metric(
        "**# SKUs**",
        value=(filtered_data["SKU Name"].nunique()),
    )

st.markdown("---")
with st.container():
    line_chart = create_line_chart(filtered_data)
    pie_chart = create_pie_chart(filtered_data)
    line_chart_col, pie_chart_col = st.columns(2, gap="large")
    line_chart_col.plotly_chart(line_chart)
    pie_chart_col.plotly_chart(pie_chart)

# st.markdown("---")
with st.container():
    trend_line_vol_col, trend_line_val_col = st.columns(2, gap="large")
    trend_line_vol = create_trend_line_vol(filtered_data)
    tend_line_value = create_trend_line_value(filtered_data)
    trend_line_vol_col.plotly_chart(trend_line_vol)
    trend_line_val_col.plotly_chart(tend_line_value)

with st.container():
    selection = st.multiselect("", options=filtered_data["SKU Name"].unique())

filtered_data_final = filtered_data[filtered_data["SKU Name"].isin(selection)]
with st.container():
    bot_col_1, bot_col_2 = st.columns(2, gap="large")
    line_chart_bot = create_line_chart_bottom(filtered_data_final)
    bar_chart = create_bar_chart(filtered_data_final)
    bot_col_1.plotly_chart(line_chart_bot)
    bot_col_2.plotly_chart(bar_chart)
