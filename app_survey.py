import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils import sections

# Load the data
data = pd.read_csv("data/survey_output.csv")  # Update with the actual file path or data source

# Dashboard title
st.title("Exploratory Data Visualization Dashboard")

# Sidebar for subgroup selection
st.sidebar.header("Filters")
subgroup_question = st.sidebar.selectbox(
    "Select a question to define subgroups:",
    ["No Subgroup"] + sections["Demographics"]  # Add "No Subgroup" option
)

# Sidebar for section selection
st.sidebar.header("Sections")
selected_section = st.sidebar.radio("Select a Section", list(sections.keys()))

# Display all questions in the selected section
st.header(f"Section: {selected_section}")

# Loop through each question in the selected section
for question in sections[selected_section]:
    st.subheader(question)
    
    # Calculate frequency and percentage
    if subgroup_question == "No Subgroup":
        freq_table = data[question].value_counts(normalize=False).reset_index()
        freq_table.columns = ["Response", "Frequency"]
        freq_table["Percentage"] = (freq_table["Frequency"] / freq_table["Frequency"].sum() * 100).round(2)
    else:
        freq_table = data.groupby(subgroup_question)[question].value_counts(normalize=False).reset_index(name="Frequency")
        freq_table["Percentage"] = freq_table.groupby(subgroup_question)["Frequency"].transform(
            lambda x: (x / x.sum() * 100).round(2)
        )

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