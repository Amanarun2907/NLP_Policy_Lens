"""
Visualizer - All Plotly charts for PolicyLens
"""
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd


THEME = dict(
    bg       = "#FFFFFF",
    paper    = "#F8F9FA",
    primary  = "#2471A3",
    positive = "#27AE60",
    negative = "#E74C3C",
    neutral  = "#F39C12",
    grid     = "#E5E7EB",
    text     = "#1B2631",
    palette  = px.colors.qualitative.Set2,
)


# ─────────────────────────────────────────────
# SECTOR ALLOCATION BAR CHART
# ─────────────────────────────────────────────

def sector_bar_chart(top_sectors: list[dict]) -> go.Figure:
    if not top_sectors:
        return _empty_fig("No sector allocation data found")
    df = pd.DataFrame(top_sectors).sort_values("total_crore", ascending=True)
    fig = px.bar(
        df, x="total_crore", y="sector", orientation="h",
        title="Sector-wise Budget Allocation (₹ Crore)",
        labels={"total_crore": "Amount (₹ Crore)", "sector": "Sector"},
        color="total_crore",
        color_continuous_scale="Blues",
        text="total_crore",
    )
    fig.update_traces(texttemplate="₹%{text:,.0f} Cr", textposition="outside")
    fig.update_layout(**_layout("Sector-wise Budget Allocation (₹ Crore)"))
    fig.update_layout(coloraxis_showscale=False, height=max(400, len(df) * 38))
    return fig


# ─────────────────────────────────────────────
# SECTOR TREEMAP
# ─────────────────────────────────────────────

def sector_treemap(top_sectors: list[dict]) -> go.Figure:
    if not top_sectors:
        return _empty_fig("No sector data")
    df = pd.DataFrame(top_sectors)
    df = df[df["total_crore"] > 0]
    fig = px.treemap(
        df, path=["sector"], values="total_crore",
        title="Budget Allocation Treemap",
        color="total_crore",
        color_continuous_scale="Blues",
        hover_data={"total_crore": ":,.0f"},
    )
    fig.update_traces(textinfo="label+value+percent root",
                      texttemplate="<b>%{label}</b><br>₹%{value:,.0f} Cr<br>%{percentRoot:.1%}")
    fig.update_layout(**_layout("Budget Allocation Treemap"))
    return fig


# ─────────────────────────────────────────────
# SECTOR PIE CHART
# ─────────────────────────────────────────────

def sector_pie_chart(top_sectors: list[dict], top_n: int = 10) -> go.Figure:
    if not top_sectors:
        return _empty_fig("No sector data")
    df = pd.DataFrame(top_sectors).head(top_n)
    fig = px.pie(
        df, names="sector", values="total_crore",
        title=f"Top {top_n} Sectors by Allocation",
        color_discrete_sequence=THEME["palette"],
        hole=0.35,
    )
    fig.update_traces(textposition="inside", textinfo="percent+label",
                      hovertemplate="<b>%{label}</b><br>₹%{value:,.0f} Cr<br>%{percent}")
    fig.update_layout(**_layout(f"Top {top_n} Sectors by Allocation"))
    return fig


# ─────────────────────────────────────────────
# FISCAL INDICATORS KPI CARDS (gauge)
# ─────────────────────────────────────────────

def fiscal_gauge(label: str, value: float, max_val: float = 10.0,
                 unit: str = "% of GDP") -> go.Figure:
    color = THEME["positive"] if value < 4 else THEME["neutral"] if value < 6 else THEME["negative"]
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=value,
        title={"text": f"<b>{label}</b><br><span style='font-size:0.8em'>{unit}</span>",
               "font": {"size": 16}},
        number={"suffix": f" {unit}", "font": {"size": 22}},
        gauge={
            "axis": {"range": [0, max_val], "tickwidth": 1},
            "bar":  {"color": color},
            "steps": [
                {"range": [0, max_val * 0.4], "color": "#D5F5E3"},
                {"range": [max_val * 0.4, max_val * 0.65], "color": "#FDEBD0"},
                {"range": [max_val * 0.65, max_val], "color": "#FADBD8"},
            ],
            "threshold": {"line": {"color": "red", "width": 3}, "value": max_val * 0.6},
        },
    ))
    fig.update_layout(height=260, margin=dict(t=60, b=20, l=30, r=30),
                      paper_bgcolor=THEME["paper"], plot_bgcolor=THEME["bg"])
    return fig


# ─────────────────────────────────────────────
# FISCAL INDICATORS BAR
# ─────────────────────────────────────────────

def fiscal_indicators_bar(fiscal_data: list[dict]) -> go.Figure:
    rows = [f for f in fiscal_data if f.get("percent")]
    if not rows:
        return _empty_fig("No fiscal indicator data with percentages")
    df = pd.DataFrame([{"Indicator": r["indicator"], "Value (%)": float(r["percent"])} for r in rows])
    df = df.drop_duplicates("Indicator")
    colors = [THEME["negative"] if v > 5 else THEME["neutral"] if v > 3 else THEME["positive"]
              for v in df["Value (%)"]]
    fig = go.Figure(go.Bar(
        x=df["Indicator"], y=df["Value (%)"],
        marker_color=colors,
        text=df["Value (%)"].apply(lambda x: f"{x}%"),
        textposition="outside",
    ))
    fig.update_layout(**_layout("Fiscal Indicators (% of GDP)"))
    fig.update_layout(xaxis_tickangle=-30, yaxis_title="% of GDP")
    return fig


# ─────────────────────────────────────────────
# TAX CHANGES TABLE
# ─────────────────────────────────────────────

def tax_changes_table(tax_changes: list[dict]) -> go.Figure:
    if not tax_changes:
        return _empty_fig("No tax change data")
    rows = tax_changes[:20]
    colors = []
    for r in rows:
        ct = r.get("change_type", "")
        if "Reduced" in ct or "Exempted" in ct:
            colors.append("#D5F5E3")
        elif "Increased" in ct or "Introduced" in ct:
            colors.append("#FADBD8")
        else:
            colors.append("#F4F6F7")

    fig = go.Figure(go.Table(
        header=dict(
            values=["<b>Category</b>", "<b>Change Type</b>", "<b>Amount / Rate</b>", "<b>Key Detail</b>"],
            fill_color=THEME["primary"], font=dict(color="white", size=13),
            align="left", height=36,
        ),
        cells=dict(
            values=[
                [r["category"]    for r in rows],
                [r.get("change_type", "-") for r in rows],
                [r.get("amount") or (r.get("percent", "") + "%") if r.get("percent") else "-" for r in rows],
                [r["sentence"][:80] + "..." for r in rows],
            ],
            fill_color=[colors] * 4,
            align="left", font=dict(size=12), height=30,
        ),
    ))
    fig.update_layout(**_layout("Tax Changes Summary"))
    fig.update_layout(height=max(300, len(rows) * 35 + 80))
    return fig


# ─────────────────────────────────────────────
# POLICY SCHEMES BY CATEGORY
# ─────────────────────────────────────────────

def policy_category_bar(by_category: dict) -> go.Figure:
    if not by_category:
        return _empty_fig("No policy data")
    df = pd.DataFrame([
        {"Category": k, "Count": len(v)} for k, v in by_category.items()
    ]).sort_values("Count", ascending=False)
    fig = px.bar(
        df, x="Category", y="Count",
        title="Policy Announcements by Category",
        color="Count", color_continuous_scale="Greens",
        text="Count",
    )
    fig.update_traces(textposition="outside")
    fig.update_layout(**_layout("Policy Announcements by Category"))
    fig.update_layout(coloraxis_showscale=False, xaxis_tickangle=-30)
    return fig


# ─────────────────────────────────────────────
# SENTIMENT DONUT
# ─────────────────────────────────────────────

def sentiment_donut(sentiment_result: dict, title: str = "Document Sentiment") -> go.Figure:
    pos = sentiment_result.get("positive", 0)
    neg = sentiment_result.get("negative", 0)
    neu = sentiment_result.get("neutral", 0)
    total = pos + neg + neu or 1
    fig = go.Figure(go.Pie(
        labels=["Positive", "Negative", "Neutral"],
        values=[pos, neg, neu],
        hole=0.55,
        marker_colors=[THEME["positive"], THEME["negative"], THEME["neutral"]],
        textinfo="percent+label",
        hovertemplate="<b>%{label}</b><br>%{value} sentences (%{percent})<extra></extra>",
    ))
    score = sentiment_result.get("score", 0)
    label = sentiment_result.get("label", "Neutral")
    fig.add_annotation(
        text=f"<b>{label}</b><br>{score:+.2f}",
        x=0.5, y=0.5, showarrow=False,
        font=dict(size=16, color=THEME["text"]),
    )
    fig.update_layout(**_layout(title))
    fig.update_layout(height=320, showlegend=True)
    return fig


# ─────────────────────────────────────────────
# WORD CLOUD (as scatter)
# ─────────────────────────────────────────────

def word_cloud_chart(keywords: list[dict], title: str = "Top Keywords") -> go.Figure:
    if not keywords:
        return _empty_fig("No keyword data")
    import random, math
    random.seed(42)
    n = len(keywords)
    max_freq = max(k["frequency"] for k in keywords) or 1
    fig = go.Figure()
    for i, kw in enumerate(keywords[:40]):
        angle = (i / n) * 2 * math.pi
        r     = 0.3 + 0.6 * (1 - kw["frequency"] / max_freq)
        x     = r * math.cos(angle) + random.uniform(-0.1, 0.1)
        y     = r * math.sin(angle) + random.uniform(-0.1, 0.1)
        size  = 12 + int(28 * kw["frequency"] / max_freq)
        fig.add_trace(go.Scatter(
            x=[x], y=[y], mode="text",
            text=[kw["keyword"]],
            textfont=dict(size=size, color=random.choice(THEME["palette"])),
            hovertemplate=f"<b>{kw['keyword']}</b><br>Frequency: {kw['frequency']}<extra></extra>",
            showlegend=False,
        ))
    fig.update_layout(**_layout(title))
    fig.update_xaxes(showgrid=False, zeroline=False, showticklabels=False)
    fig.update_yaxes(showgrid=False, zeroline=False, showticklabels=False)
    fig.update_layout(height=420)
    return fig


# ─────────────────────────────────────────────
# KEYWORD FREQUENCY BAR
# ─────────────────────────────────────────────

def keyword_freq_bar(keywords: list[dict], top_n: int = 20,
                     title: str = "Top Keywords by Frequency") -> go.Figure:
    if not keywords:
        return _empty_fig("No keyword data")
    df = pd.DataFrame(keywords[:top_n]).sort_values("frequency", ascending=True)
    fig = px.bar(
        df, x="frequency", y="keyword", orientation="h",
        title=title, color="frequency",
        color_continuous_scale="Teal", text="frequency",
    )
    fig.update_traces(textposition="outside")
    fig.update_layout(**_layout(title))
    fig.update_layout(coloraxis_showscale=False, height=max(350, top_n * 28))
    return fig


# ─────────────────────────────────────────────
# NEWS CATEGORY DISTRIBUTION
# ─────────────────────────────────────────────

def news_category_chart(category_tags: dict) -> go.Figure:
    if not category_tags:
        return _empty_fig("No category data")
    df = pd.DataFrame([
        {"Category": k, "Articles": len(v)}
        for k, v in category_tags.items() if v
    ]).sort_values("Articles", ascending=False)
    fig = px.bar(
        df, x="Articles", y="Category", orientation="h",
        title="News Category Distribution",
        color="Articles", color_continuous_scale="Purples", text="Articles",
    )
    fig.update_traces(textposition="outside")
    fig.update_layout(**_layout("News Category Distribution"))
    fig.update_layout(coloraxis_showscale=False, height=max(350, len(df) * 36))
    return fig


# ─────────────────────────────────────────────
# FINANCIAL METRICS TABLE
# ─────────────────────────────────────────────

def financial_metrics_table(metrics: list[dict]) -> go.Figure:
    if not metrics:
        return _empty_fig("No financial metrics")
    rows = metrics[:20]
    fig = go.Figure(go.Table(
        header=dict(
            values=["<b>Metric</b>", "<b>Value</b>", "<b>Period</b>", "<b>Context</b>"],
            fill_color=THEME["primary"], font=dict(color="white", size=13),
            align="left", height=36,
        ),
        cells=dict(
            values=[
                [r["metric"] for r in rows],
                [r.get("amount") or (str(r.get("percent", "")) + "%") for r in rows],
                [r.get("year") or "-" for r in rows],
                [r["sentence"][:80] + "..." for r in rows],
            ],
            fill_color=["#F4F6F7", "#FFFFFF"] * (len(rows) // 2 + 1),
            align="left", font=dict(size=12), height=30,
        ),
    ))
    fig.update_layout(**_layout("Financial Metrics"))
    fig.update_layout(height=max(300, len(rows) * 35 + 80))
    return fig


# ─────────────────────────────────────────────
# RISK SEVERITY CHART
# ─────────────────────────────────────────────

def risk_severity_chart(risk_factors: list[dict]) -> go.Figure:
    if not risk_factors:
        return _empty_fig("No risk data")
    from collections import Counter
    sev_count = Counter(r["severity"] for r in risk_factors)
    typ_count = Counter(r["risk_type"] for r in risk_factors)

    fig = make_subplots(
        rows=1, cols=2,
        specs=[[{"type": "pie"}, {"type": "bar"}]],
        subplot_titles=["Risk by Severity", "Risk by Type"],
    )
    sev_colors = {"High": THEME["negative"], "Medium": THEME["neutral"], "Low": THEME["positive"]}
    fig.add_trace(go.Pie(
        labels=list(sev_count.keys()),
        values=list(sev_count.values()),
        marker_colors=[sev_colors.get(k, "#AAB7B8") for k in sev_count],
        hole=0.4, textinfo="percent+label",
    ), row=1, col=1)
    fig.add_trace(go.Bar(
        x=list(typ_count.values()),
        y=list(typ_count.keys()),
        orientation="h",
        marker_color=THEME["primary"],
        text=list(typ_count.values()),
        textposition="outside",
    ), row=1, col=2)
    fig.update_layout(**_layout("Risk Analysis"))
    fig.update_layout(height=380, showlegend=False)
    return fig


# ─────────────────────────────────────────────
# YEAR-ON-YEAR COMPARISON BAR
# ─────────────────────────────────────────────

def yoy_comparison_chart(data: list[dict], year1: str, year2: str) -> go.Figure:
    if not data:
        return _empty_fig("No comparison data")
    df = pd.DataFrame(data)
    fig = go.Figure()
    if year1 in df.columns:
        fig.add_trace(go.Bar(name=year1, x=df["metric"], y=df[year1],
                             marker_color=THEME["primary"], text=df[year1],
                             textposition="outside"))
    if year2 in df.columns:
        fig.add_trace(go.Bar(name=year2, x=df["metric"], y=df[year2],
                             marker_color=THEME["positive"], text=df[year2],
                             textposition="outside"))
    fig.update_layout(**_layout(f"Year-on-Year Comparison: {year1} vs {year2}"))
    fig.update_layout(barmode="group", xaxis_tickangle=-30)
    return fig


# ─────────────────────────────────────────────
# MACRO INDICATORS RADAR
# ─────────────────────────────────────────────

def macro_radar_chart(macro_indicators: list[dict]) -> go.Figure:
    rows = [m for m in macro_indicators if m.get("percent")]
    if len(rows) < 3:
        return _empty_fig("Not enough macro indicator data for radar chart")
    labels = [r["indicator"] for r in rows[:8]]
    values = [float(r["percent"]) for r in rows[:8]]
    values_closed = values + [values[0]]
    labels_closed = labels + [labels[0]]
    fig = go.Figure(go.Scatterpolar(
        r=values_closed, theta=labels_closed,
        fill="toself", fillcolor="rgba(36,113,163,0.2)",
        line=dict(color=THEME["primary"], width=2),
        marker=dict(size=6, color=THEME["primary"]),
    ))
    fig.update_layout(**_layout("Macro Economic Indicators Radar"))
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, gridcolor=THEME["grid"])),
        height=420,
    )
    return fig


# ─────────────────────────────────────────────
# BIAS ANALYSIS CHART
# ─────────────────────────────────────────────

def bias_chart(bias_data: dict) -> go.Figure:
    pos = bias_data.get("positive_signals", 0)
    neg = bias_data.get("negative_signals", 0)
    neu = bias_data.get("neutral_signals", 0)
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=["Positive Signals", "Negative Signals", "Neutral Signals"],
        y=[pos, neg, neu],
        marker_color=[THEME["positive"], THEME["negative"], THEME["neutral"]],
        text=[pos, neg, neu], textposition="outside",
    ))
    fig.update_layout(**_layout("Newspaper Tone & Bias Analysis"))
    fig.update_layout(yaxis_title="Signal Count", showlegend=False)
    return fig


# ─────────────────────────────────────────────
# ENTITY FREQUENCY CHART
# ─────────────────────────────────────────────

def entity_freq_chart(most_mentioned: list[dict]) -> go.Figure:
    if not most_mentioned:
        return _empty_fig("No entity data")
    df = pd.DataFrame(most_mentioned[:15]).sort_values("count", ascending=True)
    color_map = {"Person": THEME["primary"], "Organization": THEME["positive"],
                 "Location": THEME["neutral"]}
    colors = [color_map.get(t, "#AAB7B8") for t in df["type"]]
    fig = go.Figure(go.Bar(
        x=df["count"], y=df["entity"], orientation="h",
        marker_color=colors, text=df["count"], textposition="outside",
    ))
    fig.update_layout(**_layout("Most Mentioned Entities"))
    fig.update_layout(height=max(350, len(df) * 32))
    return fig


# ─────────────────────────────────────────────
# PERFORMANCE TREND LINE
# ─────────────────────────────────────────────

def performance_trend(trend_data: list[dict], metric: str = "Value") -> go.Figure:
    rows = [t for t in trend_data if t.get("year") and (t.get("percent") or t.get("amount"))]
    if not rows:
        return _empty_fig("No trend data available")
    df = pd.DataFrame([{
        "Year":  r["year"],
        "Value": float(r["percent"]) if r.get("percent") else 0,
    } for r in rows]).sort_values("Year")
    fig = px.line(
        df, x="Year", y="Value", markers=True,
        title=f"{metric} Trend Over Time",
        labels={"Value": metric},
        color_discrete_sequence=[THEME["primary"]],
    )
    fig.update_traces(line_width=2.5, marker_size=8)
    fig.update_layout(**_layout(f"{metric} Trend Over Time"))
    return fig


# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────

def _layout(title: str) -> dict:
    return dict(
        title=dict(text=f"<b>{title}</b>", font=dict(size=17, color=THEME["text"]), x=0.02),
        paper_bgcolor=THEME["paper"],
        plot_bgcolor=THEME["bg"],
        font=dict(family="Arial, sans-serif", size=13, color=THEME["text"]),
        margin=dict(t=60, b=40, l=40, r=40),
        hoverlabel=dict(bgcolor="white", font_size=13),
        xaxis=dict(gridcolor=THEME["grid"]),
        yaxis=dict(gridcolor=THEME["grid"]),
    )


def _empty_fig(msg: str) -> go.Figure:
    fig = go.Figure()
    fig.add_annotation(text=msg, x=0.5, y=0.5, showarrow=False,
                       font=dict(size=15, color="#888"))
    fig.update_layout(
        paper_bgcolor=THEME["paper"], plot_bgcolor=THEME["bg"],
        xaxis=dict(visible=False), yaxis=dict(visible=False),
        height=300,
    )
    return fig
