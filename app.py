import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt

# Set the page layout
st.set_page_config(layout="wide")

# Load dataset
@st.cache_data
def load_data():
    return pd.read_csv("StudentPerformanceFactors.csv")

# Load the data
df = load_data()

# Strip any extra spaces from column names
df.columns = df.columns.str.strip()

# Title of the app
st.title("📊 Student Performance Explorer")

# Sidebar filters for selecting student characteristics
with st.sidebar:
    st.header("Filter Students")
    Gender = st.multiselect("Gender", options=df["Gender"].unique(), default=df["Gender"].unique())
    Attendance = st.selectbox("Attendance", options=df["Attendance"].unique())
    Parental_Involvement = st.selectbox("Parental Involvement", options=df["Parental_Involvement"].unique())

# Apply filters to the dataset
filtered_df = df[
    (df["Gender"].isin(Gender)) &
    (df["Attendance"] == Attendance) &
    (df["Parental_Involvement"] == Parental_Involvement)
]

# Show the filtered data
st.dataframe(filtered_df.head())

# Visualizations
st.subheader("Distribution of Scores")

# Create two columns for side-by-side visualizations
col1, col2 = st.columns(2)

# Distribution of scores based on the selected score type
with col1:
    score_type = st.selectbox("Select Score to Visualize", ["math score", "reading score", "writing score"])

    # Ensure the column exists before accessing it
    if score_type in df.columns:
        fig, ax = plt.subplots()
        sns.histplot(filtered_df[score_type], kde=True, ax=ax)
        st.pyplot(fig)
    else:
        st.write(f"Column '{score_type}' not found in dataset.")

# Boxplot showing average score by gender
with col2:
    st.write("Average Score by Gender")

    # Ensure the column exists before accessing it
    if score_type in df.columns:
        fig, ax = plt.subplots()
        sns.boxplot(x="Gender", y=score_type, data=filtered_df, ax=ax)
        st.pyplot(fig)
    else:
        st.write(f"Column '{score_type}' not found in dataset.")
