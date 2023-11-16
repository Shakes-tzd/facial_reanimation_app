import streamlit as st
import pandas as pd
from fr_modules.fr_text_analysis import load_models
from  fr_modules.helper_functions  import (load_data, update_data_entry, render_navigation_buttons, 
                       render_data_form, next_index, previous_index, 
                       render_download_buttons, apply_custom_styling,render_pdf_viewer,display_abstract,process_abstract)

# Initialize State and Load Data
df = load_data('path_to_your_data.csv')
if 'current_index' not in st.session_state:
    st.session_state['current_index'] = 0

# Main App Logic
def main():
    apply_custom_styling()
    current_index = st.session_state['current_index']
    max_index = len(df) - 1

    # Render Navigation Buttons
    def on_previous():
        st.session_state['current_index'] = previous_index(current_index)

    def on_next():
        st.session_state['current_index'] = next_index(current_index, max_index)

    render_navigation_buttons(df['pmid'].tolist(), current_index, on_previous, on_next)

    # Render Data Form and Update Data
    updated_entry = render_data_form(df, current_index)
    if updated_entry:
        df = update_data_entry(df, current_index, updated_entry)
    render_pdf_viewer(df, current_index)
    models = load_models()
    # Display Abstract
    display_abstract(df, current_index, models)
    # Render Download Buttons
    render_download_buttons(df, df) # Assuming you're downloading the same df for both buttons

# Run the main function
if __name__ == "__main__":
    main()
