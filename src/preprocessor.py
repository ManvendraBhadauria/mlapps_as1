import warnings

import numpy as np
import pandas as pd
import streamlit as st

warnings.filterwarnings("ignore")


def preprocess(data):
    try:
        data = data.dropna(subset=["Price"])
        data["Date"] = pd.to_datetime(data["Date"])
        data["Date"] = data["Date"].dt.strftime("%Y-%m-%d")
        return data
    except Exception as e:
        print(f"Expected : {e}")
