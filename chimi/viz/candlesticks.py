import pandas as pd
from plotly import graph_objects as go
from plotly.subplots import make_subplots


def get_candlestick_chart(inst_data: pd.DataFrame, name: str, periods_back=365):
    layout = go.Layout(
        xaxis={"title": "Date"},
        yaxis={"title": "Price"},
        height=2**10,
    )

    fig = make_subplots(
        rows=2, cols=1, row_heights=[0.8, 0.2], shared_xaxes=True, vertical_spacing=0.05
    )

    fig.add_trace(
        go.Candlestick(
            # x=inst_data.index.to_pydatetime(),
            open=inst_data["o"],
            high=inst_data["h"],
            low=inst_data["l"],
            close=inst_data["c"],
            increasing_line_color="#26a69a",
            decreasing_line_color="#ef5350",
            increasing=dict(fillcolor="#26a69a"),
            decreasing=dict(fillcolor="#ef5350"),
            name=name,
        ),
        row=1,
        col=1,
    )

    fig.add_trace(
        go.Bar(
            # x=inst_data.index.to_pydatetime(),
            y=inst_data.volume,
            marker_color="#00337C",
            name="VO",
            hovertemplate=[],
        ),
        row=2,
        col=1,
    )

    fig.update_layout(
        {
            "plot_bgcolor": "#FFFFFF",
            "paper_bgcolor": "#FFFFFF",
            "legend_orientation": "h",
        },
        legend=dict(y=1, x=0),
        font=dict(color="#dedddc"),
        dragmode="pan",
        hovermode="x unified",
        margin=dict(b=20, t=0, l=0, r=40),
        height=2**10,
    )
    fig.update_xaxes(
        showgrid=True,
        zeroline=True,
        rangeslider_visible=False,
        showspikes=True,
        spikemode="across",
        spikesnap="hovered data",
        showline=True,
        spikedash="solid",
        spikethickness=0.25,
    )

    fig.update_yaxes(
        showspikes=True, spikedash="solid", spikemode="across", spikethickness=0.25
    )

    # Set the X-axis range from periods_back to to latest value + 10 periods
    x_buffer = 20
    local_xmin = len(inst_data) - periods_back
    x_range = [local_xmin, len(inst_data) + x_buffer]

    # Set the Y-axis range from the local min to local max plus a buffer
    local_min = inst_data.l.iloc[local_xmin : len(inst_data)].min()
    local_max = inst_data.h.iloc[local_xmin : len(inst_data)].max()
    y_buffer = inst_data.c.iloc[local_xmin : len(inst_data)].mean() * 0.005
    y_range = [local_min - y_buffer, local_max + y_buffer]

    fig.update_layout(
        xaxis=dict(range=x_range, autorange=False),
        yaxis=dict(range=y_range, autorange=False),
    )

    return fig
