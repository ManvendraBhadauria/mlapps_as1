import pandas as pd
import numpy as np


def delta_cal(filtered_data):
    filtered_data["Date"] = pd.to_datetime(filtered_data["Date"])
    date_max = filtered_data["Date"].max()
    date_min = filtered_data["Date"].min()

    ytd_vol_sales_delta = (filtered_data["Volume"].sum()) - (
        filtered_data[filtered_data["Date"] == date_min]["Volume"].sum()
    )

    ytd_val_sales_delta = (filtered_data["Value"].sum()) - (
        filtered_data[filtered_data["Date"] == date_min]["Value"].sum()
    )

    return ytd_vol_sales_delta, ytd_val_sales_delta
