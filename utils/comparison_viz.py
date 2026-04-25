"""
Comparison Visualizations - Year-on-Year charts
"""
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd

THEME = dict(
    y1_color  = "#1F6FEB",
    y2_color  = "#238636",
    inc_color = "#238636",
    dec_color = "#DA3633",
    neu_color = "#9E6A03",
    paper     = "#161B22",
    bg        = "#0D1117",
    text      = "#E6EDF3",
    subtext   = "#8B949E",
    grid      = "#21262D",
    border    = "#30363D",
)


def sector_comparison_chart(sector_data: list[dict], year1: str, year2: str) -> go.Figure:
    if not sector_data:
        return _empty("No sector comparison data")
    df = pd.DataFrame(sector_data)
    df = df[(df[f"{year1}_crore"] > 0) | (df[f"{year2}_crore"] > 0)]
    df = df.sort_values(f"{year2}_crore", ascending=True).tail(15)

    fig = go.Figure()
    fig.add_trace(go.Bar(
        name=year1, y=df["sector"], x=df[f"{year1}_crore"],
        orientation="h", marker_color=THEME["y1_color"],
        text=df[f"{year1}_crore"].apply(lambda x: f"₹{x:,.0f}Cr"),
        textposition="outside",
    ))
    fig.add_trace(go.Bar(
        name=year2, y=df["sector"], x=df[f"{year2}_crore"],
        orientation="h", marker_color=THEME["y2_color"],
        text=df[f"{year2}_crore"].apply(lambda x: f"₹{x:,.0f}Cr"),
        textposition="outside",
    ))
    fig.update_layout(
        **_layout(f"Sector Allocation: {year1} vs {year2}"),
        barmode="group",
        height=max(450, len(df) * 55),
        xaxis_title="Amount (₹ Crore)",
    )
    return fig


def sector_change_waterfall(sector_data: list[dict], year1: str, year2: str) -> go.Figure:
    if not sector_data:
        return _empty("No data")
    df = pd.DataFrame(sector_data)
    df = df[df["change_crore"] != 0].sort_values("change_crore", ascending=False).head(15)
    colors = [THEME["inc_color"] if c > 0 else THEME["dec_color"] for c in df["change_crore"]]
    fig = go.Figure(go.Bar(
        x=df["sector"], y=df["change_crore"],
        marker_color=colors,
        text=df["change_crore"].apply(lambda x: f"{'+'if x>0 else ''}₹{x:,.0f}Cr"),
        textposition="outside",
    ))
    fig.add_hline(y=0, line_dash="dash", line_color="#888")
    fig.update_layout(
        **_layout(f"Sector Allocation Change ({year1} → {year2})"),
        xaxis_tickangle=-35,
        yaxis_title="Change (₹ Crore)",
    )
    return fig


def sector_change_pct_chart(sector_data: list[dict], year1: str, year2: str) -> go.Figure:
    if not sector_data:
        return _empty("No data")
    df = pd.DataFrame(sector_data)
    df = df[df["change_pct"] != 0].sort_values("change_pct", ascending=True).head(15)
    colors = [THEME["inc_color"] if c > 0 else THEME["dec_color"] for c in df["change_pct"]]
    fig = go.Figure(go.Bar(
        x=df["change_pct"], y=df["sector"],
        orientation="h", marker_color=colors,
        text=df["change_pct"].apply(lambda x: f"{'+'if x>0 else ''}{x:.1f}%"),
        textposition="outside",
    ))
    fig.add_vline(x=0, line_dash="dash", line_color="#888")
    fig.update_layout(
        **_layout(f"% Change in Sector Allocation ({year1} → {year2})"),
        xaxis_title="% Change",
        height=max(400, len(df) * 40),
    )
    return fig


def fiscal_comparison_chart(fiscal_data: list[dict], year1: str, year2: str) -> go.Figure:
    rows = [f for f in fiscal_data if f.get(f"{year1}_%") and f.get(f"{year2}_%")]
    if not rows:
        return _empty("No fiscal comparison data with values for both years")
    df = pd.DataFrame(rows)
    fig = go.Figure()
    fig.add_trace(go.Bar(
        name=year1, x=df["indicator"], y=df[f"{year1}_%"],
        marker_color=THEME["y1_color"],
        text=df[f"{year1}_%"].apply(lambda x: f"{x}%"),
        textposition="outside",
    ))
    fig.add_trace(go.Bar(
        name=year2, x=df["indicator"], y=df[f"{year2}_%"],
        marker_color=THEME["y2_color"],
        text=df[f"{year2}_%"].apply(lambda x: f"{x}%"),
        textposition="outside",
    ))
    fig.update_layout(
        **_layout(f"Fiscal Indicators: {year1} vs {year2}"),
        barmode="group",
        xaxis_tickangle=-30,
        yaxis_title="% of GDP",
    )
    return fig


def keyword_shift_chart(kw_data: dict, year1: str, year2: str) -> go.Figure:
    comp = kw_data.get("comparison", [])
    if not comp:
        return _empty("No keyword comparison data")
    df = pd.DataFrame(comp[:20])
    fig = go.Figure()
    fig.add_trace(go.Bar(
        name=year1, x=df["keyword"], y=df[f"{year1}_freq"],
        marker_color=THEME["y1_color"],
    ))
    fig.add_trace(go.Bar(
        name=year2, x=df["keyword"], y=df[f"{year2}_freq"],
        marker_color=THEME["y2_color"],
    ))
    fig.update_layout(
        **_layout(f"Keyword Frequency Shift: {year1} vs {year2}"),
        barmode="group",
        xaxis_tickangle=-35,
        yaxis_title="Frequency",
    )
    return fig


def sentiment_comparison_chart(sent_data: dict, year1: str, year2: str) -> go.Figure:
    s1 = sent_data.get(year1, {})
    s2 = sent_data.get(year2, {})
    categories = ["Positive", "Negative", "Neutral"]
    v1 = [s1.get("positive",0), s1.get("negative",0), s1.get("neutral",0)]
    v2 = [s2.get("positive",0), s2.get("negative",0), s2.get("neutral",0)]
    fig = go.Figure()
    fig.add_trace(go.Bar(name=year1, x=categories, y=v1,
                         marker_color=THEME["y1_color"], text=v1, textposition="outside"))
    fig.add_trace(go.Bar(name=year2, x=categories, y=v2,
                         marker_color=THEME["y2_color"], text=v2, textposition="outside"))
    fig.update_layout(
        **_layout(f"Sentiment Comparison: {year1} vs {year2}"),
        barmode="group", yaxis_title="Sentence Count",
    )
    return fig


def summary_kpi_chart(summary: dict, year1: str, year2: str) -> go.Figure:
    alloc = summary.get("total_allocation", {})
    schemes = summary.get("scheme_count", {})
    taxes   = summary.get("tax_changes", {})

    metrics = ["Total Allocation (₹Cr)", "Policy Schemes", "Tax Changes"]
    v1 = [alloc.get(year1,0), schemes.get(year1,0), taxes.get(year1,0)]
    v2 = [alloc.get(year2,0), schemes.get(year2,0), taxes.get(year2,0)]

    fig = make_subplots(rows=1, cols=3,
                        subplot_titles=metrics)
    for i, (m, a, b) in enumerate(zip(metrics, v1, v2), 1):
        fig.add_trace(go.Bar(name=year1, x=[year1], y=[a],
                             marker_color=THEME["y1_color"],
                             text=[f"{a:,.0f}"], textposition="outside",
                             showlegend=(i==1)), row=1, col=i)
        fig.add_trace(go.Bar(name=year2, x=[year2], y=[b],
                             marker_color=THEME["y2_color"],
                             text=[f"{b:,.0f}"], textposition="outside",
                             showlegend=(i==1)), row=1, col=i)
    fig.update_layout(
        **_layout(f"Key Metrics: {year1} vs {year2}"),
        barmode="group", height=380,
    )
    return fig


def policy_category_comparison(pol_data: dict, year1: str, year2: str) -> go.Figure:
    cat_comp = pol_data.get("category_comparison", [])
    if not cat_comp:
        return _empty("No policy category data")
    df = pd.DataFrame(cat_comp)
    fig = go.Figure()
    fig.add_trace(go.Bar(
        name=year1, x=df["category"], y=df[f"{year1}_count"],
        marker_color=THEME["y1_color"],
        text=df[f"{year1}_count"], textposition="outside",
    ))
    fig.add_trace(go.Bar(
        name=year2, x=df["category"], y=df[f"{year2}_count"],
        marker_color=THEME["y2_color"],
        text=df[f"{year2}_count"], textposition="outside",
    ))
    fig.update_layout(
        **_layout(f"Policy Schemes by Category: {year1} vs {year2}"),
        barmode="group", xaxis_tickangle=-30,
    )
    return fig


def tax_category_comparison(tax_data: dict, year1: str, year2: str) -> go.Figure:
    delta = tax_data.get("category_delta", [])
    if not delta:
        return _empty("No tax comparison data")
    df = pd.DataFrame(delta)
    fig = go.Figure()
    fig.add_trace(go.Bar(
        name=year1, x=df["category"], y=df[f"{year1}_count"],
        marker_color=THEME["y1_color"],
        text=df[f"{year1}_count"], textposition="outside",
    ))
    fig.add_trace(go.Bar(
        name=year2, x=df["category"], y=df[f"{year2}_count"],
        marker_color=THEME["y2_color"],
        text=df[f"{year2}_count"], textposition="outside",
    ))
    fig.update_layout(
        **_layout(f"Tax Changes by Category: {year1} vs {year2}"),
        barmode="group", xaxis_tickangle=-30,
    )
    return fig


def _layout(title: str) -> dict:
    return dict(
        title=dict(text=f"<b>{title}</b>", font=dict(size=16, color=THEME["text"]), x=0.02),
        paper_bgcolor=THEME["paper"], plot_bgcolor=THEME["bg"],
        font=dict(family="'Inter', Arial, sans-serif", size=13, color=THEME["text"]),
        margin=dict(t=60, b=50, l=50, r=40),
        hoverlabel=dict(bgcolor=THEME["paper"], font_size=13, bordercolor=THEME["border"]),
        xaxis=dict(gridcolor=THEME["grid"], zerolinecolor=THEME["grid"], color=THEME["subtext"]),
        yaxis=dict(gridcolor=THEME["grid"], zerolinecolor=THEME["grid"], color=THEME["subtext"]),
        legend=dict(bgcolor=THEME["paper"], bordercolor=THEME["border"], borderwidth=1,
                    font=dict(color=THEME["text"])),
    )


def _empty(msg: str) -> go.Figure:
    fig = go.Figure()
    fig.add_annotation(text=msg, x=0.5, y=0.5, showarrow=False,
                       font=dict(size=14, color="#888"))
    fig.update_layout(
        paper_bgcolor=THEME["paper"], plot_bgcolor=THEME["bg"],
        xaxis=dict(visible=False), yaxis=dict(visible=False), height=300,
    )
    return fig
