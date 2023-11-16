import pandas as pd
import streamlit as st
from fr_modules.fr_text_analysis import load_models, process_text,

def load_data(source_file):
    """Load data from a CSV file."""
    return pd.read_csv(source_file)

def update_data_entry(df, index, entry):
    """Update a single entry in the DataFrame."""
    for key, value in entry.items():
        if key in df.columns:
            df.at[index, key] = value
    return df
def render_navigation_buttons(pmids, index, on_previous, on_next):
    col1, col2, col3 = st.columns([1, 2, 1])

    with col1:
        if index > 0:
            st.button("Back", on_click=on_previous)

    with col3:
        if index < len(pmids) - 1:
            st.button("Next", on_click=on_next)
def render_data_form(df, index):
    with st.form(key='Paper_Details'):
        # Extract data for the current index
        current_entry = df.iloc[index]
        updated_entry = {}

        # Create form fields for each column
        for column in df.columns:
            updated_entry[column] = st.text_input(column, value=current_entry[column])
        
        submitted = st.form_submit_button("Save")
        
        if submitted:
            return updated_entry
    return None
def next_index(index, max_index):
    return min(index + 1, max_index)

def previous_index(index):
    return max(index - 1, 0)
def convert_df_to_csv(df):
    return df.to_csv().encode('utf-8')

def render_download_buttons(main_df, input_df):
    csv_main = convert_df_to_csv(main_df)
    csv_input = convert_df_to_csv(input_df)

    st.download_button("Download Main Data as CSV", csv_main, "main_data.csv", "text/csv")
    st.download_button("Download Input Data as CSV", csv_input, "input_data.csv", "text/csv")
def apply_custom_styling():
    hide_st_style = """
        <style>
        MainMenu {visibility: visible;}
        footer {visibility: hidden;}
        </style>
    """
    st.markdown(hide_st_style, unsafe_allow_html=True)
def render_pdf_viewer(df, index):
    pmid = df.iloc[index]['pmid']
    filename = f"{pmid}_sci_hub.pdf"
    file_link = f'https://storage.googleapis.com/facial-reanimation.appspot.com/downloaded_articles/{filename}'

    with st.container():
        link_html = gen_html(file_link, filename)
        try:
            components.html(link_html, height=750)
        except:
            st.markdown("# The full text is not available in the folder")

def process_abstract(text, model):
    doc = model(text)
    anonymized_tokens = process_text(doc)
    return anonymized_tokens

def display_abstract(df, index, models):
    doc_title = df['title'].iloc[index]
    text_input = df['abstract'].iloc[index]
    selected_model = models["en"]

    anonymized_tokens = process_abstract(text_input, selected_model)

    expander_title = "Click to read: " + doc_title + " (Abstract)"
    with st.expander(expander_title):
        annotated_text(*anonymized_tokens)
