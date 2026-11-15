 
import streamlit as st
import pandas as pd
import plotly.express as px

# PAGE CONFIGURATION
st.set_page_config(
    page_title="E-Commerce Analytics",
    page_icon="🛍️",
    layout="wide"
)

# MIDNIGHT LUXURY THEME
theme = {
    "background": "#080D1C",
    "sidebar": "#171333",
    "card": "#151D35",
    "primary": "#A78BFA",
    "secondary": "#22D3EE",
    "text": "#F1F5F9",
    "border": "#34345C",
    "charts": [
        "#A78BFA",
        "#22D3EE",
        "#F472B6",
        "#FBBF24",
        "#34D399",
        "#FB7185",
        "#818CF8"
    ]
}

chart_colors = theme["charts"]

# SIDEBAR
st.sidebar.title("✨ Dashboard Settings")
 

# CUSTOM CSS DESIGN
st.markdown(f"""
<style>

@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Poppins:wght@400;500;600;700&display=swap');

.stApp {{
    background: linear-gradient(
        135deg,
        #080D1C,
        #11152D,
        #19132F,
        #080D1C
    );
    font-family: 'Poppins', sans-serif;
}}

.block-container {{
    padding-top: 2rem;
    padding-bottom: 3rem;
}}

[data-testid="stHeader"] {{
    background: transparent;
}}

[data-testid="stSidebar"] {{
    background: linear-gradient(
        180deg,
        #171333,
        #30205A,
        #111C35
    );
    border-right: 1px solid #51417A;
}}

[data-testid="stSidebar"] * {{
    color: #FFFFFF !important;
}}

h1 {{
    font-family: 'Playfair Display', serif !important;
    color: #C4B5FD !important;
    font-size: 43px !important;
}}

h2, h3 {{
    color: #C4B5FD !important;
    font-weight: 700 !important;
}}

p, label, .stCaption {{
    color: #CBD5E1;
}}

[data-testid="stMetric"] {{
    background: linear-gradient(
        135deg,
        #202A48,
        #292044
    );
    padding: 22px;
    border-radius: 18px;
    border: 1px solid #62518F;
    box-shadow: 0 5px 20px rgba(0,0,0,0.30);
    transition: 0.3s ease;
}}

[data-testid="stMetric"]:hover {{
    transform: translateY(-5px);
    border-color: #A78BFA;
}}

[data-testid="stMetricLabel"] {{
    color: #CBD5E1 !important;
    font-weight: 600;
}}

[data-testid="stMetricValue"] {{
    color: #C4B5FD !important;
    font-weight: 700;
}}

[data-testid="stMetricDelta"] {{
    color: #34D399 !important;
}}

.stButton button,
.stDownloadButton button {{
    background: linear-gradient(
        90deg,
        #7C3AED,
        #DB2777
    );
    color: white !important;
    border: none;
    border-radius: 12px;
    font-weight: 600;
    padding: 10px 20px;
}}

.stButton button:hover,
.stDownloadButton button:hover {{
    background: linear-gradient(
        90deg,
        #0891B2,
        #7C3AED
    );
    color: white !important;
}}

[data-testid="stDataFrame"] {{
    border: 1px solid #51417A;
    border-radius: 12px;
}}

[data-testid="stSelectbox"] > div {{
    background-color: #202A48;
}}

[data-testid="stSlider"] {{
    padding-top: 10px;
}}

[data-testid="stSlider"] [role="slider"] {{
    background-color: #A78BFA !important;
    border-color: #A78BFA !important;
}}

[data-testid="stAlert"] {{
    border-radius: 12px;
}}

hr {{
    border-color: #34345C;
}}

</style>
""", unsafe_allow_html=True)


# CHART DESIGN FUNCTION
def style_chart(fig):
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#151D35",
        plot_bgcolor="#151D35",
        font=dict(
            family="Poppins",
            color="#E2E8F0"
        ),
        title_font=dict(
            family="Playfair Display",
            size=20,
            color="#C4B5FD"
        ),
        margin=dict(l=20, r=20, t=60, b=20),
        legend=dict(
            font=dict(color="#E2E8F0")
        )
    )

    fig.update_xaxes(
        gridcolor="#34345C",
        zerolinecolor="#34345C"
    )

    fig.update_yaxes(
        gridcolor="#34345C",
        zerolinecolor="#34345C"
    )

    return fig


# LOAD DATASET
df = pd.read_csv("ecommerce_customers.csv")


# HEADER
st.title("🌙 E-Commerce Customer Analytics")
st.caption(
    "✨ Customer Behavior | Spending Patterns | Business Intelligence"
)

st.divider()


# SIDEBAR FILTERS
st.sidebar.subheader("🎯 Customer Filters")

min_membership, max_membership = st.sidebar.slider(
    "Membership Duration",
    float(df["Length of Membership"].min()),
    float(df["Length of Membership"].max()),
    (
        float(df["Length of Membership"].min()),
        float(df["Length of Membership"].max())
    )
)

min_app, max_app = st.sidebar.slider(
    "Time on App",
    float(df["Time on App"].min()),
    float(df["Time on App"].max()),
    (
        float(df["Time on App"].min()),
        float(df["Time on App"].max())
    )
)

min_website, max_website = st.sidebar.slider(
    "Time on Website",
    float(df["Time on Website"].min()),
    float(df["Time on Website"].max()),
    (
        float(df["Time on Website"].min()),
        float(df["Time on Website"].max())
    )
)

min_spending, max_spending = st.sidebar.slider(
    "Yearly Amount Spent",
    float(df["Yearly Amount Spent"].min()),
    float(df["Yearly Amount Spent"].max()),
    (
        float(df["Yearly Amount Spent"].min()),
        float(df["Yearly Amount Spent"].max())
    )
)


# APPLY FILTERS
filtered_df = df[
    (df["Length of Membership"].between(min_membership, max_membership)) &
    (df["Time on App"].between(min_app, max_app)) &
    (df["Time on Website"].between(min_website, max_website)) &
    (df["Yearly Amount Spent"].between(min_spending, max_spending))
].copy()


# CUSTOMER OVERVIEW
st.subheader("💎 Customer Overview")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "👥 Total Customers",
    len(filtered_df)
)

col2.metric(
    "💰 Average Spending",
    round(filtered_df["Yearly Amount Spent"].mean(), 2)
    if not filtered_df.empty else "N/A"
)

col3.metric(
    "⭐ Average Membership",
    round(filtered_df["Length of Membership"].mean(), 2)
    if not filtered_df.empty else "N/A"
)

col4.metric(
    "📱 Average App Time",
    round(filtered_df["Time on App"].mean(), 2)
    if not filtered_df.empty else "N/A"
)

st.divider()


if filtered_df.empty:

    st.warning("No customers found. Please adjust your filters.")

else:

    # SPENDING ANALYSIS
    st.subheader("💰 Customer Spending Analysis")

    col1, col2 = st.columns(2)

    with col1:

        fig1 = px.histogram(
            filtered_df,
            x="Yearly Amount Spent",
            nbins=25,
            title="Yearly Spending Distribution",
            color_discrete_sequence=[chart_colors[0]]
        )

        st.plotly_chart(
            style_chart(fig1),
            use_container_width=True
        )

    with col2:

        fig2 = px.scatter(
            filtered_df,
            x="Length of Membership",
            y="Yearly Amount Spent",
            title="Membership vs Yearly Spending",
            color_discrete_sequence=[chart_colors[1]]
        )

        st.plotly_chart(
            style_chart(fig2),
            use_container_width=True
        )


    # CUSTOMER ACTIVITY
    st.subheader("📊 Customer Activity Analysis")

    col3, col4 = st.columns(2)

    with col3:

        fig3 = px.scatter(
            filtered_df,
            x="Time on App",
            y="Yearly Amount Spent",
            title="App Time vs Yearly Spending",
            color_discrete_sequence=[chart_colors[2]]
        )

        st.plotly_chart(
            style_chart(fig3),
            use_container_width=True
        )

    with col4:

        fig4 = px.scatter(
            filtered_df,
            x="Time on Website",
            y="Yearly Amount Spent",
            title="Website Time vs Yearly Spending",
            color_discrete_sequence=[chart_colors[3]]
        )

        st.plotly_chart(
            style_chart(fig4),
            use_container_width=True
        )


    # CUSTOMER SEGMENTATION
    st.divider()
    st.subheader("🎯 Customer Segmentation")

    if len(filtered_df) >= 3:

        filtered_df["Customer Segment"] = pd.qcut(
            filtered_df["Yearly Amount Spent"].rank(method="first"),
            q=3,
            labels=[
                "Low Spending",
                "Medium Spending",
                "High Spending"
            ]
        )

        segment_counts = (
            filtered_df["Customer Segment"]
            .value_counts()
            .reindex([
                "Low Spending",
                "Medium Spending",
                "High Spending"
            ])
            .reset_index()
        )

        segment_counts.columns = [
            "Customer Segment",
            "Customers"
        ]

        fig6 = px.pie(
            segment_counts,
            names="Customer Segment",
            values="Customers",
            title="Customers by Spending Segment",
            color_discrete_sequence=chart_colors,
            hole=0.4
        )

        st.plotly_chart(
            style_chart(fig6),
            use_container_width=True
        )

    else:
        st.info("At least 3 customers are needed for segmentation.")


    # TOP CUSTOMERS
    st.subheader("🏆 Top 10 Customers")

    top_customers = filtered_df.nlargest(
        10,
        "Yearly Amount Spent"
    )[[
        "Email",
        "Length of Membership",
        "Yearly Amount Spent"
    ]]

    st.dataframe(
        top_customers,
        use_container_width=True,
        hide_index=True
    )


    # MEMBERSHIP GROUPS
    st.subheader("🌟 Average Spending by Membership Group")

    membership_df = filtered_df.copy()

    membership_df["Membership Group"] = pd.cut(
        membership_df["Length of Membership"],
        bins=3,
        labels=["Short", "Medium", "Long"],
        duplicates="drop"
    )

    membership_average = (
        membership_df.groupby(
            "Membership Group",
            observed=False
        )["Yearly Amount Spent"]
        .mean()
        .reset_index()
    )

    fig7 = px.bar(
        membership_average,
        x="Membership Group",
        y="Yearly Amount Spent",
        title="Average Spending by Membership Duration",
        color="Membership Group",
        color_discrete_sequence=chart_colors
    )

    st.plotly_chart(
        style_chart(fig7),
        use_container_width=True
    )


    # CORRELATION HEATMAP
    st.subheader("🔥 Correlation Analysis")

    corr = filtered_df.select_dtypes(
        include="number"
    ).corr()

    fig5 = px.imshow(
        corr,
        text_auto=".2f",
        color_continuous_scale=[
            "#312E81",
            "#7C3AED",
            "#EC4899",
            "#F9A8D4",
            "#FDE68A"
        ],
        title="Customer Data Correlation Heatmap",
        aspect="auto"
    )

    st.plotly_chart(
        style_chart(fig5),
        use_container_width=True
    )


    # BUSINESS INSIGHTS
    st.divider()
    st.subheader("💡 Business Insights")

    average_spending = filtered_df[
        "Yearly Amount Spent"
    ].mean()

    average_membership = filtered_df[
        "Length of Membership"
    ].mean()

    app_corr = filtered_df["Time on App"].corr(
        filtered_df["Yearly Amount Spent"]
    )

    membership_corr = filtered_df[
        "Length of Membership"
    ].corr(
        filtered_df["Yearly Amount Spent"]
    )

    st.info(
        f"💰 Average customer spending is {average_spending:.2f}."
    )

    st.info(
        f"⭐ Average membership duration is {average_membership:.2f} years."
    )

    if pd.notna(membership_corr):

        st.info(
            f"📈 Membership and yearly spending correlation: "
            f"{membership_corr:.2f}."
        )

    if pd.notna(app_corr):

        st.info(
            f"📱 App time and yearly spending correlation: "
            f"{app_corr:.2f}."
        )


    # DOWNLOAD REPORT
    st.divider()
    st.subheader("📥 Download Customer Report")

    csv_data = filtered_df.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        label="⬇️ Download Filtered Data as CSV",
        data=csv_data,
        file_name="ecommerce_customer_report.csv",
        mime="text/csv"
    )


    # CUSTOMER DETAILS
    st.subheader("📋 Customer Details")

    st.dataframe(
        filtered_df,
        use_container_width=True,
        hide_index=True
    )


# FOOTER
st.divider()

st.caption(
    "🌙 E-Commerce Customer Analytics Dashboard | "
    "Python • Pandas • Plotly • Streamlit"
)
