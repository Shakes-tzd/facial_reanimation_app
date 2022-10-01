
import pandas as pd  # pip install pandas openpyxl
import streamlit as st  # pip install streamlit
import spacy
from annotated_text import annotated_text
import streamlit.components.v1 as components



# emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title="Facial Reanimation Article Explorer",
                   page_icon="📑", layout="wide")

# ---- READ EXCEL ----


@st.cache(show_spinner=False, allow_output_mutation=True, suppress_st_warning=True)
def load_models():
    # french_model = spacy.load("models/fr/")
    english_model = spacy.load("models/en")
    models = {"en": english_model}  # , "fr": french_model}
    return models


@st.cache(show_spinner=False, allow_output_mutation=True, suppress_st_warning=True)
def get_data_from_csv(source_file):
    df = pd.read_csv(source_file)
    return df


# get_data_from_csv(files[selected_source_file])
df = get_data_from_csv('30-09-22_Facial-reanimation_data_time-to-reinnervation_v0002.csv')


def process_text(doc):
    tokens = []
    for token in doc:

        if (token.ent_type_ == "CARDINAL") or token.like_num:
            tokens.append((token.text, "", "#faa"))
        # else:
        #     if (token.text == "patients") or (token.text == "patient") or (token.text == "case") or (token.text == "cases"):
        #         tokens.append((token.text, "", "#00968C"))
        #     else:
        #         if (token.text == "double") or (token.text == "dual"):
        #             tokens.append((token.text, "", "#8ef"))
        else:
            tokens.append(" " + token.text + " ")
    return tokens


ent_color_mapping = {
    "ORG": "#faa",
    "CARDINAL": "#00968C"}


def resamble(plain_text, entities):
    ll = []
    entities_copy = entities.copy()
    prev_ent_idx = 0
    current_ent_idx = 0
    while len(entities) > 0:
        if len(ll) == 0:
            ll.append(plain_text[:entities[current_ent_idx]["start"]])
            ll.append((plain_text[entities[0]["start"]:entities[0]["end"]],
                      entities[0]["label"], ent_color_mapping[entities[0]["label"]]))
        else:
            ll.append(
                plain_text[entities_copy[prev_ent_idx-1]["end"]:entities[0]["start"]])
            ll.append((plain_text[entities[0]["start"]:entities[0]["end"]],
                      entities[0]["label"], ent_color_mapping[entities[0]["label"]]))
        if len(entities) > 1:
            del entities[0]
            prev_ent_idx += 1
            continue
        else:
            ll.append(plain_text[entities[0]["end"]:])
            del entities[0]
    return ll


def map_entities(doc):
    plain_text = doc.text
    entities = text.entities
    return resamble(plain_text, entities)


# st.markdown("**Abstracts**")
# st.markdown("---")
# df
pmids=df['pmid'].to_list()
my_list = pmids
# sidebar = st.sidebar
left_col,mid_col,next_col = st.columns([1, 1,1])
with mid_col:
    pmid_selector = st.selectbox("Select a PMID", pmids)
    selected=pmid_selector
    inititial=pmids.index(pmid_selector)
    show_next =st.number_input('PMID Index', value=pmids.index(pmid_selector))
    st.session_state.current_index = show_next 
    selected=(my_list[st.session_state.current_index])



models = load_models()
abs_num=df[df['pmid'] == selected].index[0]
# abs_num = st.number_input("Choose Abstract to Show",value=0, min_value=0, max_value=max(df['pmid'])-1)

    


doc_title = df['title'].loc[abs_num]
# width, height = pyautogui.size()
text_input = df['abstract'].loc[abs_num]
selected_model = models["en"]
doc = selected_model(text_input)
anonymized_tokens = process_text(doc)
st.markdown(f"**{doc_title}**")
height = int(len(text_input) * 0.5) + 10
annotated_text(*anonymized_tokens)
col1, col2 = st.columns([1, 3])

with col1:
    
    st.session_state.abs_num=abs_num

    @st.cache(allow_output_mutation=True)
    def get_data():
        return []
    

    pmid = df['pmid'].loc[abs_num]
    patients = df['patients'].loc[abs_num]
    min_time_to_reinnervation = df['time_to_reinnervation_(min)'].loc[abs_num]
    max_time_to_reinnervation = df['time_to_reinnervation_(max)'].loc[abs_num]
    age= df['Age'].loc[abs_num]
    min_age= df['min age'].loc[abs_num]
    max_age= df['max age'].loc[abs_num]
    min_follow_up= df['follow up min'].loc[abs_num]
    max_follow_up= df['follow up max'].loc[abs_num]
    

    st.markdown(f"**PMID**: {pmid}")
    patients = st.number_input('Patients', value=float(patients), min_value=0.0, max_value=1000.0)
    age_in = st.number_input('Age', value=float(age), min_value=0.0, max_value=1000.0)
    min_age_in = st.number_input('Min Age', value=float(min_age), min_value=0.0, max_value=1000.0)
    max_age_in = st.number_input('Max Age', value=float(max_age), min_value=0.0, max_value=1000.0)
    min_time_to_reinnervation_in = st.number_input('Min Time to Reinnervation', value=float(min_time_to_reinnervation), min_value=0.0, max_value=1000.0)
    max_time_to_reinnervation_in = st.number_input('Max Time to Reinnervation', value=float(max_time_to_reinnervation), min_value=0.0, max_value=1000.0)
    min_follow_up_in = st.number_input('Min Follow up', value=float(min_follow_up), min_value=0.0, max_value=1000.0)
    max_follow_up_in = st.number_input('Max Follow up', value=float(max_follow_up), min_value=0.0, max_value=1000.0)
    

    if st.button("Add row"):
        get_data().append(
            {"PMID": pmid, "Patients": patients, "Age": age_in, "Min Age": min_age_in, "Max Age": max_age_in, "Min Time to Reinnervation": min_time_to_reinnervation_in, "Max Time to Reinnervation": max_time_to_reinnervation_in, "Min Follow up": min_follow_up_in, "Max Follow up": max_follow_up_in})
        st.session_state.abs_num += 1
        df['patients'].loc[abs_num]=patients
        df['time_to_reinnervation_(min)'].loc[abs_num]=min_time_to_reinnervation_in
        df['time_to_reinnervation_(max)'].loc[abs_num]= max_time_to_reinnervation_in
        df['Age'].loc[abs_num]= age_in
        df['min age'].loc[abs_num]= min_age_in
        df['max age'].loc[abs_num]= max_age_in
        df['follow up min'].loc[abs_num]= min_follow_up_in
        df['follow up max'].loc[abs_num]= max_follow_up_in
        df.to_csv('30-09-22_Facial-reanimation_data_time-to-reinnervation_v0002.csv', index=False)

    st.write(pd.DataFrame(get_data()))




with col2:
    try:
        
        df_links = pd.read_csv('pdf_file_links_2.csv')
        pdf_link=df_links['link'][df_links['pmid']==pmid].values[0].replace('view','preview')
        components.iframe(pdf_link,height=1200)  # width=900, height=1000, frameborder=0, style="border:0;")
    except:
        st.markdown("# The full text is not available in the folder")
        


# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            MainMenu {visibility: visible;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
