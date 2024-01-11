from pathlib import Path as pt

import pandas as pd
import streamlit as st

from src.output_transformer import make_data, make_graph
from src.preprocessor import preprocess
from src.style import css_code

st.set_page_config(
    page_title="Assignment 1",
    page_icon="🐯",
    layout="wide",
    initial_sidebar_state="expanded",
)


st.markdown(css_code, unsafe_allow_html=True)

st.markdown(
    "<h1 style='color:grey;' id='titleh1'>Sales Analytics Dashboard</h1>",
    unsafe_allow_html=True,
)

home_path = pt.cwd()
df = pd.read_csv(home_path / pt("data/Input_Sales_Data_v2.csv"), index_col="Id")
data = pd.DataFrame(preprocess(df))

data["Date"] = pd.to_datetime(data["Date"], format="%Y-%m-%d")

date_min = data["Date"].min().date()
date_max = data["Date"].max().date()

with st.sidebar:
    st.image("./assets/logo.png")
    st.markdown("---")
    st.markdown("<h3>Filters</h3>", unsafe_allow_html=True)

    col1, col2 = st.columns([0.40, 0.60])
    with col1:
        cate = st.selectbox("", options=list(data["Category"].unique()), placeholder="Choose a Category")

    with col2:
        selected_date = st.slider(
            "",
            min_value=date_min,
            max_value=date_max,
            value=(date_min, date_max),
        )
    st.markdown("---")
    with st.container():
        st.write(f"**Category :** {cate}")

        st.write(
            f"**Min Date :** {selected_date[0].strftime('%Y-%m-%d')}",
        )
        st.write(
            f"**Max Date :** {selected_date[1].strftime('%Y-%m-%d')}",
        )


selected_date = (pd.to_datetime(selected_date[0]), pd.to_datetime(selected_date[1]))

filtered_data = data[
    (data["Date"].dt.date >= selected_date[0].date())
    & (data["Date"].dt.date <= selected_date[1].date())
    & (data["Category"] == cate)
]
processed_data = make_data(filtered_data)
st.dataframe(
    processed_data.style.background_gradient(cmap="Blues", subset=["Market Share %"]),
    width=1200,
)


fig = make_graph(filtered_data, selected_date[0], selected_date[1])

# Display Plotly chart
st.plotly_chart(fig)
