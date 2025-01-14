import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Load the data
data = pd.read_csv("data/survey_output.csv")  # Update with the actual file path or data source

# Dashboard title
st.title("Exploratory Data Visualization Dashboard")

# Group questions into sections
sections = {
    "Demographics": [
        'Which country are you located in?',
        'Which region best describes your program or institution’s location?',
        'What is your title?',
        'Which faculty/discipline/team do you belong to? Select all that apply.'
    ],
    "Program Details": [
        'How many students do you target enrolling each year?',
        'What is the average applicant-to-seat ratio at your school?',
        'Which of the following best describes your program or institution?'
    ],
    "Recruitment Strategies": [
        'What primary recruitment strategy does your institution plan to focus on in 2025? Select all that apply.',
        'Which recruitment challenges do you anticipate will be most significant in 2025? Select all that apply.',
        'How does your institution plan to respond to the "enrollment cliff" (projected decline in high school graduates)? Select all that apply.'
    ],
    "AI and Admissions": [
        'How has your institution integrated AI tools into the admissions process? Select all that apply.',
        'What role do you believe AI will play in admissions processes within the next two years? Select all that apply.',
        'How concerned is your institution about applicants using AI tools (e.g., ChatGPT, Grammarly) during the admissions process?',
        'What resources or guidance is your institution providing to applicants regarding AI usage (e.g., ChatGPT, Grammarly) in the admissions process? Select all that apply.'
    ],
    "Policy and Adaptation": [
        'How prepared is your institution to adapt to potential policy changes in higher education?',
        'What areas of proposed legislation do you anticipate will most impact admissions policies? Select all that apply.',
        'What solutions is your institution considering to adapt to new or proposed higher education policies? Select all that apply.'
    ],
    "Holistic Admissions": [
        'How is your institution evolving its approach to holistic review in admissions? Select all that apply.',
        'How are AI and predictive analytics being used in your institution\'s holistic admissions process? Select all that apply.',
        'What factors are receiving increased emphasis in your institution\'s holistic review process? Select all that apply.'
    ],
    "Value and Communication": [
        'What is your institution\'s primary strategy to demonstrate the value of a higher education degree to prospective students?',
        'What alternative educational pathways is your institution developing to attract a broad range of students? Select all that apply.',
        'How does your institution communicate its unique value proposition to prospective students and families? Select all that apply.',
        'What do you see as the biggest obstacle to communicating the value of higher education today?'
    ],
    "Brand Awareness": [
        'Which of the following brands have you heard of? Select all that apply.',
        'Which of the following brands would you recommend to colleagues? Select all that apply.'
    ]
}

# Display all sections as buttons in the sidebar
st.sidebar.header("Sections")
selected_section = st.sidebar.radio("Select a Section", list(sections.keys()))

# Display all questions in the selected section
st.header(f"Section: {selected_section}")

# Loop through each question in the selected section
for question in sections[selected_section]:
    st.subheader(question)
    
    # Calculate frequency
    freq_table = data[question].value_counts().reset_index()
    freq_table.columns = ["Response", "Frequency"]

    # Display frequency table
    st.dataframe(freq_table)

    # Create an interactive bar chart using Plotly
    fig = px.bar(
        freq_table,
        x="Response",
        y="Frequency",
        title=f"Response Frequency for: {question}",
        labels={"Frequency": "Count", "Response": "Response"},
        text="Frequency"
    )
    fig.update_traces(textposition="outside")
    fig.update_layout(
        xaxis_title="Response",
        yaxis_title="Frequency",
        title_x=0.5
    )

    # Display the chart
    st.plotly_chart(fig)