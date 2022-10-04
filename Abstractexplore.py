import pandas as pd  # pip install pandas openpyxl
import streamlit as st  # pip install streamlit
import spacy
from annotated_text import annotated_text
import streamlit.components.v1 as components
import firebase_admin
from firebase_admin import credentials,storage

# emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title="Facial Reanimation Article Explorer",
                   page_icon="📑", layout="wide")

# ---- READ EXCEL ----

# my_lit
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
left_col,mid_col,next_col = st.columns([2, 1,2])
def pmid_to_index():
    st.session_state.indx = pmids.index(st.session_state.pmid_select)

    
with mid_col:
    pmid_select = st.selectbox("Select a PMID", pmids,key='pmid_select',on_change =  pmid_to_index)
    pmid_index=pmids.index(st.session_state.pmid_select)
    if 'indx' not in st.session_state:
        st.session_state['indx'] = pmid_index

    # st.session_state['article_index'] = 
    show_next =pmid_index #st.number_input('PMID Index',  key= "indx", on_change =  index_to_pmid,value=pmid_index)
    selected=(my_list[show_next])
    abs_num=df[df['pmid'] == selected].index[0]
    patients = df['patients'].loc[abs_num]
    



models = load_models()

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
st.session_state.abs_num=abs_num

@st.cache(allow_output_mutation=True)
def get_data():
    return []
def update_data(patients, age_in, min_age_in, max_age_in, min_time_to_reinnervation_in, max_time_to_reinnervation_in, min_follow_up_in, max_follow_up_in):
    get_data().append(
            {"PMID": pmid, "Patients": patients, "Age": age_in, "Min Age": min_age_in, "Max Age": max_age_in, "Min Time to Reinnervation": min_time_to_reinnervation_in, "Max Time to Reinnervation": max_time_to_reinnervation_in, "Min Follow up": min_follow_up_in, "Max Follow up": max_follow_up_in})
    df['patients'].loc[abs_num]=patients
    df['time_to_reinnervation_(min)'].loc[abs_num]=min_time_to_reinnervation_in
    df['time_to_reinnervation_(max)'].loc[abs_num]= max_time_to_reinnervation_in
    df['Age'].loc[abs_num]= age_in
    df['min age'].loc[abs_num]= min_age_in
    df['max age'].loc[abs_num]= max_age_in
    df['follow up min'].loc[abs_num]= min_follow_up_in
    df['follow up max'].loc[abs_num]= max_follow_up_in
    df.to_csv('30-09-22_Facial-reanimation_data_time-to-reinnervation_v0002.csv', index=False)
def index_to_pmid():
    st.session_state.pmid_select =my_list[st.session_state.indx]
    update_data(patients, age_in, min_age_in, max_age_in, min_time_to_reinnervation_in, max_time_to_reinnervation_in, min_follow_up_in, max_follow_up_in)
pmid = df['pmid'].loc[abs_num]
min_time_to_reinnervation = df['time_to_reinnervation_(min)'].loc[abs_num]
max_time_to_reinnervation = df['time_to_reinnervation_(max)'].loc[abs_num]
age= df['Age'].loc[abs_num]
min_age= df['min age'].loc[abs_num]
max_age= df['max age'].loc[abs_num]
min_follow_up= df['follow up min'].loc[abs_num]
max_follow_up= df['follow up max'].loc[abs_num]
st.markdown("""---""")
inp1, inp2, inp3, inp4, = st.columns(4)
with inp1:
    patients = st.number_input('Patients', value=float(patients), min_value=0.0, max_value=1000.0)
with inp2:
    age_in = st.number_input('Age', value=float(age), min_value=0.0, max_value=1000.0)
with inp3:
    min_age_in = st.number_input('Min Age', value=float(min_age), min_value=0.0, max_value=1000.0)
with inp4:
    max_age_in = st.number_input('Max Age', value=float(max_age), min_value=0.0, max_value=1000.0)
inp5, inp6, inp7, inp8,inp9 = st.columns(5)
with inp5:
    min_time_to_reinnervation_in = st.number_input('Min Time to Reinnervation', value=float(min_time_to_reinnervation), min_value=0.0, max_value=1000.0)
with inp6:
    max_time_to_reinnervation_in = st.number_input('Max Time to Reinnervation', value=float(max_time_to_reinnervation), min_value=0.0, max_value=1000.0)
with inp7:
    min_follow_up_in = st.number_input('Min Follow up', value=float(min_follow_up), min_value=0.0, max_value=1000.0)
with inp8:
    max_follow_up_in = st.number_input('Max Follow up', value=float(max_follow_up), min_value=0.0, max_value=1000.0)

with inp9:
    st.write("Save Inputs")
    if st.button("Save All", key="add",on_click=index_to_pmid):
        st.session_state.indx +=1  
    

       

df_links = pd.read_csv('pdf_file_links_2.csv')



st.markdown("""---""")    
try:
    file_link=df_links['link'][df_links['pmid']== pmid].values[0]
    file_link=file_link.replace('view?usp=drivesdk','preview')
    components.iframe(file_link,  height=1000)
except:
    st.markdown("# The full text is not available in the folder")

# link1       
st.write(pd.DataFrame(get_data()))

# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            MainMenu {visibility: visible;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
