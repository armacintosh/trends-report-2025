import streamlit as st
import pandas as pd
import plotly.express as px
from utils import sections

# Load the data
data = pd.read_csv("data/survey_output.csv")  # Main survey data
gd = pd.read_csv("data/greatest_differences.csv")  # Greatest differences data

# Dashboard title
st.title("Exploratory Data Visualization Dashboard")

# Sidebar for cohort selection
st.sidebar.header("Cohort Selection")
cohort = st.sidebar.radio("Filter Responses by Cohort", ["All", "United States", "Other"])

# Filter data based on cohort
if cohort == "United States":
    filtered_data = data[data['Which country are you located in?'] == 'United States']
elif cohort == "Other":
    filtered_data = data[data['Which country are you located in?'] != 'United States']
else:
    filtered_data = data

# Sidebar for subgroup selection
st.sidebar.header("Filters")
subgroup_question = st.sidebar.selectbox(
    "Select a question to define subgroups:",
    ["No Subgroup"] + sections["Demographics"]  # Add "No Subgroup" option
)

# Sidebar for section selection
st.sidebar.header("Sections")
selected_section = st.sidebar.radio("Select a Section", list(sections.keys()))

# Add Region Comparison button in the sidebar
st.sidebar.header("Region Comparison")
region_comparison = st.sidebar.button("View Region Comparison")

# Handle Region Comparison separately
if region_comparison:
    st.title("Region Comparison")

    # Display the interactive gd table
    st.subheader("Greatest Differences Table")
    st.dataframe(gd)

    # Visualize the greatest differences using a Plotly bar chart
    st.subheader("Visualizing Greatest Differences")
    fig = px.bar(
        gd,
        x="Difference",
        y="Question",
        color="Response",
        orientation="h",
        text="Difference",
        hover_data=["US_Percentage", "Other_Percentage", "Section"],
        title="Questions with Greatest Differences Between United States and Other Countries",
        labels={
            "Difference": "Absolute Difference (%)",
            "Question": "Survey Question",
            "Response": "Response"
        }
    )
    fig.update_traces(textposition="outside")
    fig.update_layout(
        yaxis=dict(title="Survey Question"),
        xaxis=dict(title="Absolute Difference (%)"),
        title_x=0.5,
        height=800  # Adjust height for better visualization
    )
    st.plotly_chart(fig)
else:
    # Main dashboard logic
    st.header(f"Section: {selected_section}")

    # Loop through each question in the selected section
    for question in sections[selected_section]:
        st.subheader(question)

        # Calculate frequency and percentage
        if subgroup_question == "No Subgroup":
            freq_table = filtered_data[question].value_counts(normalize=False).reset_index()
            freq_table.columns = ["Response", "Frequency"]
            total_frequency = freq_table["Frequency"].sum()
            freq_table["Percentage"] = (freq_table["Frequency"] / total_frequency * 100).round(2)
        else:
            freq_table = filtered_data.groupby(subgroup_question)[question].value_counts(normalize=False).reset_index(name="Frequency")
            total_frequency = freq_table["Frequency"].sum()
            freq_table["Percentage"] = (freq_table["Frequency"] / total_frequency * 100).round(2)

        # Display frequency table with percentages
        st.dataframe(freq_table)

        # Create an interactive bar chart using Plotly
        if subgroup_question == "No Subgroup":
            fig = px.bar(
                freq_table,
                x="Response",
                y="Frequency",
                title=f"Response Frequency for: {question}",
                labels={"Frequency": "Count", "Response": "Response"},
                text="Frequency"
            )
        else:
            fig = px.bar(
                freq_table,
                x=subgroup_question,
                y="Frequency",
                color=question,
                barmode="group",
                text="Frequency",
                title=f"Response Frequencies for: {question} by {subgroup_question}",
                labels={subgroup_question: "Subgroup", question: "Response"}
            )

        fig.update_traces(textposition="outside")
        fig.update_layout(
            xaxis_title="Response" if subgroup_question == "No Subgroup" else "Subgroup",
            yaxis_title="Frequency",
            title_x=0.5
        )

        # Display the chart
        st.plotly_chart(fig)