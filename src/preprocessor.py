import pandas as pd
import numpy as np
import streamlit as st
import warnings

warnings.filterwarnings("ignore")


def preprocess(data):
    try:
        data = data.dropna(subset=["Price"])
        data["Date"] = pd.to_datetime(data["Date"])
        data["Date"] = data["Date"].dt.strftime("%Y-%m-%d")
        return data
    except Exception as e:
        print(f"Expected : {e}")
