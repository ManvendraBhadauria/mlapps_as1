import pandas as pd
import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode

from src.output_transformer import scenario_bar_chart
from src.scenarios_style import css

st.set_page_config(
    "Scenarios",
    page_icon="🎭",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.header("**Scenarios**")

st.markdown(css, unsafe_allow_html=True)


@st.cache_data
def load_data():
    selected_cols = ["Name", "Created Date", "Created by", "revenue", "cost", "profit", "prec_profit"]
    data = pd.read_excel("data/scenarios.xlsx", sheet_name=0)
    return data[selected_cols]


df = load_data()


builder = GridOptionsBuilder.from_dataframe(df)
builder.configure_selection(selection_mode="multiple", use_checkbox=True)
builder.configure_default_column(min_column_width=50)
go = builder.build()

grid_table = AgGrid(data=df, gridOptions=go, update_mode=GridUpdateMode.SELECTION_CHANGED, allow_unsafe_jscode=True)
selected_rows = grid_table["selected_rows"]

st.markdown("---")
if len(selected_rows) != 0:
    bar_Chart = scenario_bar_chart(selected_rows)
    st.plotly_chart(bar_Chart)
