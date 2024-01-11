import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go


def create_line_chart(data):
    filtered_data = data.copy(deep=True)
    filtered_data["Date"] = pd.to_datetime(filtered_data["Date"])
    filtered_data.set_index("Date", inplace=True)
    weekly_data = filtered_data.resample("W").sum()
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=weekly_data.index,
            y=weekly_data["Volume"],
            name="Weekly Volume Sales",
            yaxis="y",
        )
    )

    fig.add_trace(
        go.Scatter(
            x=weekly_data.index,
            y=weekly_data["Value"],
            name="Weekly Value Sales",
            yaxis="y2",
        )
    )

    fig.update_layout(
        yaxis=dict(title="Volume Sales", side="left", showgrid=False),
        yaxis2=dict(title="Value Sales", overlaying="y", side="right", showgrid=False),
        xaxis=dict(title="Date (Weekly)"),
    )

    return fig


def create_pie_chart(filtered_data):
    sku_value = filtered_data.groupby("SKU Name")["Value"].sum()
    top_10_skus = sku_value.nlargest(10)
    total_top_10_value = top_10_skus.sum()
    percentage_values = (top_10_skus / total_top_10_value) * 100
    fig = go.Figure(data=[go.Pie(labels=top_10_skus.index, values=percentage_values)])
    fig.update_layout(title="Percentage of Value for Top 10 SKUs within the Brand")
    return fig


def create_trend_line_vol(filtered_data):
    # Fit a linear regression model
    coefficients = np.polyfit(filtered_data["Volume"], filtered_data["Price"], 1)
    line = np.poly1d(coefficients)
    trendline = line(filtered_data["Volume"])

    # Create scatter plot
    fig = go.Figure()

    # Add scatter plot
    fig.add_trace(
        go.Scatter(
            x=filtered_data["Volume"],
            y=filtered_data["Price"],
            mode="markers",
            name="Price vs Volume Sales",
        )
    )

    # Add trendline
    fig.add_trace(go.Scatter(x=filtered_data["Volume"], y=trendline, mode="lines", name="Trendline"))

    # Update layout for axis titles and labels
    fig.update_layout(xaxis=dict(title="Volume Sales"), yaxis=dict(title="Price"))

    return fig


def create_trend_line_value(filtered_data):
    # Fit a linear regression model
    coefficients = np.polyfit(filtered_data["Value"], filtered_data["Price"], 1)
    line = np.poly1d(coefficients)
    trendline = line(filtered_data["Value"])

    # Create scatter plot
    fig = go.Figure()

    # Add scatter plot
    fig.add_trace(
        go.Scatter(
            x=filtered_data["Value"],
            y=filtered_data["Price"],
            mode="markers",
            name="Price vs Value Sales",
        )
    )

    # Add trendline
    fig.add_trace(go.Scatter(x=filtered_data["Value"], y=trendline, mode="lines", name="Trendline"))

    # Update layout for axis titles and labels
    fig.update_layout(xaxis=dict(title="Value Sales"), yaxis=dict(title="Price"))

    return fig


def create_line_chart_bottom(data):
    filtered_data = data.copy(deep=True)
    filtered_data["Date"] = pd.to_datetime(filtered_data["Date"])
    filtered_data.set_index("Date", inplace=True)
    weekly_data = filtered_data.resample("W").sum()
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=weekly_data.index,
            y=weekly_data["Volume"],
            name="Weekly Volume Sales",
            yaxis="y",
        )
    )

    fig.add_trace(
        go.Scatter(
            x=weekly_data.index,
            y=weekly_data["Value"],
            name="Weekly Value Sales",
            yaxis="y2",
        )
    )

    fig.update_layout(
        yaxis=dict(title="Volume Sales", side="left", showgrid=False),
        yaxis2=dict(title="Value Sales", overlaying="y", side="right", showgrid=False),
        xaxis=dict(title="Date (Weekly)"),
    )

    return fig


def create_bar_chart(filtered_data):
    filtered_data["Month"] = pd.to_datetime(filtered_data["Date"]).dt.to_period("M").astype(str)
    average_sales_per_month_sku = filtered_data.groupby(["Month", "SKU Name"])["Value"].mean().reset_index()
    fig = px.bar(
        average_sales_per_month_sku,
        x="Month",
        y="Value",
        color="SKU Name",
        title="Average Sales per Month for Selected SKUs",
        labels={"Month": "Date", "Value": "Average Sales"},
    )
    return fig
