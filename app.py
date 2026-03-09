import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# --- Page Configuration ---
st.set_page_config(
    page_title="Student Performance Dashboard",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom Styling ---
st.markdown("""
<style>
    /* Black Background Base */
    .stApp {
        background-color: #000000;
    }
    /* Yellow and White Text */
    h1, h2, h3, h4, h5, h6, .stMarkdown p {
        color: #ffffff !important; 
    }
    h1, h2 {
        color: #fbbf24 !important; /* Amber/Yellow for main headers */
    }
    /* Metric Cards: Dark grey background, yellow values */
    .stMetric, [data-testid="stMetricValue"], [data-testid="stMetricLabel"] {
        background-color: #1a1a1a;
    }
    [data-testid="stMetricValue"] {
        color: #fcd34d !important; /* Bright Yellow */
        font-weight: 900;
        font-size: 2.2rem;
    }
    [data-testid="stMetricLabel"] {
        color: #e5e7eb !important; /* Off-white for labels */
        font-size: 1.1rem;
        font-weight: 600;
    }
    /* Dark Sidebar with Yellow Accent */
    [data-testid="stSidebar"] {
        background-color: #111111;
        border-right: 2px solid #fbbf24;
    }
    [data-testid="stSidebar"] p, [data-testid="stSidebar"] span {
        color: #f3f4f6 !important;
    }
</style>
""", unsafe_allow_html=True)

# --- Data Loading ---
@st.cache_data
def load_data():
    if not os.path.exists("student_performance_data.xlsx"):
        st.error("⚠️ Dataset not found! Please run `python generate_data.py` first.")
        st.stop()
    df = pd.read_excel("student_performance_data.xlsx")
    # Clean data similar to EDA process
    if 'StudentID' in df.columns:
        df = df.drop(columns=['StudentID'])
    if df['StudyTime'].isnull().any():
        df['StudyTime'].fillna(df['StudyTime'].median(), inplace=True)
    
    # Segment creation
    def segment_students(gpa):
        if gpa > 3.0: return 'High Performer'
        elif 2.0 <= gpa <= 3.0: return 'Average Student'
        else: return 'At Risk'
    
    df['PerformanceSegment'] = df['GPA'].apply(segment_students)
    return df

df = load_data()

# --- Sidebar Controls ---
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/3135/3135810.png", width=100)
st.sidebar.title("🎓 Filter Dashboard")
st.sidebar.markdown("Use these filters to slice the academic data.")

# Filters
selected_gender = st.sidebar.multiselect("Select Gender", options=df['Gender'].unique(), default=df['Gender'].unique())
selected_support = st.sidebar.multiselect("Parental Support", options=df['ParentalSupport'].unique(), default=df['ParentalSupport'].unique())
selected_segment = st.sidebar.multiselect("Performance Segment", options=df['PerformanceSegment'].unique(), default=df['PerformanceSegment'].unique())

# Apply filters
filtered_df = df[
    (df['Gender'].isin(selected_gender)) & 
    (df['ParentalSupport'].isin(selected_support)) &
    (df['PerformanceSegment'].isin(selected_segment))
]

st.sidebar.markdown("---")
st.sidebar.info("💡 **Insight:** Use filtering to see how *At Risk* students interact with *Tutoring*.")

# --- Main Dashboard Setup ---
st.title("📊 Student Performance & Academic Analytics")
st.markdown("An interactive Exploratory Data Analysis (EDA) investigating the factors affecting **Student GPA**.")

# --- Key Metrics Row ---
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Students", len(filtered_df))
with col2:
    avg_gpa = filtered_df['GPA'].mean()
    st.metric("Average GPA", f"{avg_gpa:.2f}")
with col3:
    avg_study = filtered_df['StudyTime'].mean()
    st.metric("Avg Study Time (hrs)", f"{avg_study:.1f}")
with col4:
    avg_absences = filtered_df['Absences'].mean()
    st.metric("Avg Absences", f"{avg_absences:.1f}")

st.markdown("---")

# --- Visualizations Settings ---
# Set matplotlib background to black, text and axes to yellow/white
sns.set_theme(style="darkgrid", rc={
    "axes.facecolor": "#111111", 
    "figure.facecolor": "#000000",
    "axes.edgecolor": "#fbbf24",
    "axes.labelcolor": "#fbbf24",
    "text.color": "#ffffff",
    "xtick.color": "#ffffff",
    "ytick.color": "#ffffff",
    "grid.color": "#333333"
})

st.header("1️⃣ Academic Distributions")
col_a, col_b = st.columns(2)

with col_a:
    st.subheader("Distribution of GPA")
    fig_gpa, ax_gpa = plt.subplots(figsize=(8, 4))
    sns.histplot(filtered_df['GPA'], kde=True, bins=20, color='#fcd34d', alpha=0.9, ax=ax_gpa)
    ax_gpa.set_xlabel("GPA", fontsize=12, fontweight='bold')
    ax_gpa.set_ylabel("Count", fontsize=12, fontweight='bold')
    st.pyplot(fig_gpa)

with col_b:
    st.subheader("Distribution of Study Time")
    fig_study, ax_study = plt.subplots(figsize=(8, 4))
    sns.histplot(filtered_df['StudyTime'], kde=True, bins=20, color='#d97706', alpha=0.9, ax=ax_study)
    ax_study.set_xlabel("Study Time (Hours)", fontsize=12, fontweight='bold')
    ax_study.set_ylabel("Count", fontsize=12, fontweight='bold')
    st.pyplot(fig_study)

st.markdown("---")

st.header("2️⃣ Behavioral Impacts on GPA")
col_c, col_d = st.columns(2)

with col_c:
    st.subheader("Study Time vs. GPA")
    fig_scatter1, ax_scatter1 = plt.subplots(figsize=(8, 5))
    sns.scatterplot(data=filtered_df, x='StudyTime', y='GPA', alpha=0.9, s=60, color='#fef08a', edgecolor='black', ax=ax_scatter1) 
    sns.regplot(data=filtered_df, x='StudyTime', y='GPA', scatter=False, color='#fbbf24', line_kws={'linewidth': 3}, ax=ax_scatter1) 
    ax_scatter1.set_xlabel("Study Time", fontsize=12, fontweight='bold')
    ax_scatter1.set_ylabel("GPA", fontsize=12, fontweight='bold')
    st.pyplot(fig_scatter1)

with col_d:
    st.subheader("Absences vs. GPA")
    fig_scatter2, ax_scatter2 = plt.subplots(figsize=(8, 5))
    sns.scatterplot(data=filtered_df, x='Absences', y='GPA', alpha=0.9, s=60, color='#fef08a', edgecolor='black', ax=ax_scatter2) 
    sns.regplot(data=filtered_df, x='Absences', y='GPA', scatter=False, color='#ef4444', line_kws={'linewidth': 3}, ax=ax_scatter2) # Keep trendline red for negative impact
    ax_scatter2.set_xlabel("Absences", fontsize=12, fontweight='bold')
    ax_scatter2.set_ylabel("GPA", fontsize=12, fontweight='bold')
    st.pyplot(fig_scatter2)

st.markdown("---")

st.header("3️⃣ Categorical Influences")
tab1, tab2, tab3 = st.tabs(["👪 Parental Support", "📚 Tutoring", "⚽ Extracurriculars"])

# Deep, distinct categorical colors
yellow_palette = ['#fcd34d', '#f59e0b', '#b45309']

with tab1:
    fig_box1, ax_box1 = plt.subplots(figsize=(10, 4))
    sns.boxplot(data=filtered_df, x='ParentalSupport', y='GPA', palette=yellow_palette, hue='ParentalSupport', legend=False, linewidth=2, ax=ax_box1)
    ax_box1.set_xlabel("Parental Support", fontsize=12, fontweight='bold')
    ax_box1.set_ylabel("GPA", fontsize=12, fontweight='bold')
    st.pyplot(fig_box1)

with tab2:
    fig_box2, ax_box2 = plt.subplots(figsize=(10, 4))
    sns.boxplot(data=filtered_df, x='Tutoring', y='GPA', palette=yellow_palette, hue='Tutoring', legend=False, linewidth=2, ax=ax_box2)
    ax_box2.set_xlabel("Tutoring", fontsize=12, fontweight='bold')
    ax_box2.set_ylabel("GPA", fontsize=12, fontweight='bold')
    st.pyplot(fig_box2)

with tab3:
    fig_box3, ax_box3 = plt.subplots(figsize=(10, 4))
    sns.boxplot(data=filtered_df, x='ExtracurricularActivities', y='GPA', palette=yellow_palette, hue='ExtracurricularActivities', legend=False, linewidth=2, ax=ax_box3)
    ax_box3.set_xlabel("Extracurriculars", fontsize=12, fontweight='bold')
    ax_box3.set_ylabel("GPA", fontsize=12, fontweight='bold')
    st.pyplot(fig_box3)

st.markdown("---")

# --- Correlation & Composition ---
col_e, col_f = st.columns([1.5, 1])

with col_e:
    st.header("4️⃣ Correlation Matrix")
    st.markdown("Identifies the mathematical strength of relationships between variables.")
    numerical_cols = filtered_df.select_dtypes(include=['float64', 'int64', 'int32'])
    
    if not numerical_cols.empty:
        fig_corr, ax_corr = plt.subplots(figsize=(8, 6))
        # Swap colormap to a yellow/black/white map
        sns.heatmap(numerical_cols.corr(), annot=True, cmap='afmhot', fmt=".2f", linewidths=1, linecolor='black', annot_kws={'size': 12, 'weight': 'bold'}, ax=ax_corr)
        st.pyplot(fig_corr)
    else:
        st.warning("Not enough numerical data to map correlation.")

with col_f:
    st.header("5️⃣ Segment Breakdown")
    st.markdown("High = >3.0 | Avg = 2.0-3.0 | Risk = <2.0")
    
    segment_counts = filtered_df['PerformanceSegment'].value_counts()
    fig_pie, ax_pie = plt.subplots(figsize=(6, 6))
    
    # Yellow variations and one dark alert color for the pie chart
    pie_colors = ['#fbbf24', '#fef08a', '#333333']
    wedges, texts, autotexts = ax_pie.pie(
        segment_counts, 
        labels=segment_counts.index, 
        autopct='%1.1f%%', 
        startangle=90, 
        colors=pie_colors,
        wedgeprops={'linewidth': 2, 'edgecolor': '#fbbf24'}
    )
    plt.setp(autotexts, size=11, weight="bold", color="black")
    plt.setp(texts, size=12, weight="bold", color="white")
    st.pyplot(fig_pie)

st.markdown("---")
st.caption("Data source: Simulated Student Performance Dataset | Built using Streamlit, Python & Pandas")
