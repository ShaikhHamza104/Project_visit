import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Page Config
st.set_page_config(page_title="Skill Development Program Analysis", page_icon="🎓", layout="wide")

# Custom CSS for Metrics AND Multiselect Tags
st.markdown("""
<style>
    /* Metric Card Styling */
    [data-testid="stMetric"] {
        background-color: #ffffff;
        border-radius: 12px;
        padding: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        border: 1px solid #e2e8f0;
    }
    [data-testid="stMetric"] label, 
    [data-testid="stMetric"] div {
        color: #1f2937 !important; 
    }

    /* Sleek Multiselect Tag Styling */
    span[data-baseweb="tag"] {
        background-color: #3b82f6 !important; /* Modern Blue */
        border-radius: 15px !important;
        padding: 2px 12px !important;
        border: none !important;
    }
    /* Force tag text and 'x' button to be white */
    span[data-baseweb="tag"] span {
        color: #ffffff !important; 
    }
</style>
""", unsafe_allow_html=True)


# 2. Data Loading
@st.cache_data
def load_and_clean_data():
    df = pd.read_csv('data.csv')
    df['year'] = pd.to_numeric(df['year'], errors='coerce').fillna(0).astype(int)
    df['projects'] = df['projects'].str.strip().str.lower()
    return df


@st.cache_data
def get_exploded_counts(df, column):
    """Safely splits by comma and returns counts."""
    exploded = df[column].str.split(r',\s*').explode()
    counts = exploded.value_counts().reset_index()
    counts.columns = [column, 'count']
    return counts


try:
    df = load_and_clean_data()
except FileNotFoundError:
    st.error("Data file 'Hamza.csv' not found. Please ensure the file is in the correct directory.")
    st.stop()

# 3. Interactive Sidebar
with st.sidebar:
    st.title("⚙️ Filters")
    st.markdown("Tailor your data view:")

    # Year Selection
    st.subheader("📅 Academic Year")
    years = sorted(df['year'].unique())
    sel_year = st.multiselect("Select Year(s)", options=years, default=years)

    # Course Selection (Improved UX)
    st.subheader("📚 Courses")
    courses = df['current_course'].unique()

    # "Select All" toggle prevents massive tag clutter
    select_all_courses = st.checkbox("Select All Courses", value=True)

    if select_all_courses:
        sel_course = courses
        st.success(f"Viewing all {len(courses)} courses.")
    else:
        # Only show the multiselect box if they want specific courses
        sel_course = st.multiselect(
            "Choose specific course(s)",
            options=courses,
            default=[courses[0]] if len(courses) > 0 else []
        )

    # Apply Filters
    mask = df['year'].isin(sel_year) & df['current_course'].isin(sel_course)
    filtered_df = df[mask]

# 4. KPI Section
st.title("🎓 Student Insights Dashboard")

if not filtered_df.empty:
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total Students", len(filtered_df))
    m2.metric("Avg. Skill Rating", f"{filtered_df['rating'].mean():.2f}")
    project_count = len(filtered_df[filtered_df['projects'] == 'yes'])
    m3.metric("Project Participation", project_count)
    m4.metric("Career Categories", filtered_df['career_interest'].nunique())

    st.divider()

    # 5. Visualizations
    tab1, tab2, tab3 = st.tabs(["🎯 Career", "🛠️ Skills", "⚠️ Challenges"])

    with tab1:
        col_a, col_b = st.columns(2)
        with col_a:
            fig_pie = px.pie(filtered_df, names='career_interest', hole=0.5, title="Career Interests")
            st.plotly_chart(fig_pie, width='stretch')
        with col_b:
            method_counts = filtered_df['method'].value_counts().reset_index()
            method_counts.columns = ['method', 'count']
            fig_donut = px.pie(method_counts, names='method', values='count', hole=0.7, title="Learning Methods")
            st.plotly_chart(fig_donut, width='stretch')

    with tab2:
        col_c, col_d = st.columns(2)
        with col_c:
            tech_skills = get_exploded_counts(filtered_df, 'technical_skills').head(10)
            fig_tech = px.bar(tech_skills, x='count', y='technical_skills', orientation='h', title="Top Tech Skills")
            st.plotly_chart(fig_tech, width='stretch')
        with col_d:
            soft_skills = get_exploded_counts(filtered_df, 'soft_skills').head(10)
            fig_soft = px.bar(soft_skills, x='count', y='soft_skills', orientation='h', title="Top Soft Skills")
            st.plotly_chart(fig_soft, width='stretch')

    with tab3:
        c1, c2 = st.columns(2)
        with c1:
            ch_counts = filtered_df['challenges'].value_counts().reset_index()
            ch_counts.columns = ['challenge', 'count']
            fig_ch = px.bar(ch_counts, x='count', y='challenge', orientation='h', title="Top Challenges")
            st.plotly_chart(fig_ch, width='stretch')
        with c2:
            sup_counts = filtered_df['support_required'].value_counts().reset_index()
            sup_counts.columns = ['support', 'count']
            fig_funnel = px.funnel(sup_counts, x='count', y='support', title="Support Funnel")
            st.plotly_chart(fig_funnel, width='stretch')

else:
    st.warning("Please select at least one filter option to view analytics.")
