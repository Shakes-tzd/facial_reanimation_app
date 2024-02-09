import pandas as pd  # pip install pandas openpyxl
import streamlit as st  # pip install streamlit
from annotated_text import annotated_text
import streamlit.components.v1 as components
from fr_modules.fr_text_analysis import load_models, process_text, resamble, map_entities
from fr_modules.html_gen import gen_html
import spacy_streamlit
from spacy_streamlit import visualize_ner, visualize_spans
import spacy
from spacy.matcher import PhraseMatcher
from spacy.tokens import Span
from spacy import displacy
st.set_page_config(page_title="Facial Reanimation Article Explorer",
                   page_icon="📑", layout="wide")
nlp = spacy.load('en_core_web_sm')

# "G":['In this paper',"Methods:","Methods","METHODS","MATERIALS AND METHODS","MATERIALS AND METHODS:",
#                  "MATERIALS AND METHODS","Results:","Results","RESULTS","Discussion:","Discussion",
#                  "DISCUSSION","DISCUSSION:","discussion","discussion:","Discussion and Conclusion",
#                  "Discussion and Conclusions","Discussion and conclusion","Discussion and conclusions",
#                  "Discussion and Conclusions:","Discussion and Conclusion:","Discussion and conclusion:","Discussion and conclusions:","Discussion and Conclusions.","Discussion and Conclusion.","Discussion and conclusion.","Discussion and conclusions.","Discussion and Conclusions:","Discussion and Conclusion:","Discussion and conclusion:","Discussion and conclusions:","Discussion and Conclusions.","Discussion and Conclusion.","Discussion and conclusion.","Discussion and conclusions.","Discussion and Conclusions","Discussion and Conclusion","Discussion and conclusion","Discussion and conclusions","Discussion and Conclusions:","Discussion and Conclusion:","Discussion and conclusion:","Discussion and conclusions:","Discussion and Conclusions.","Discussion and Conclusion.","Discussion and conclusion.","Discussion and conclusions."],
procedures={
    "Exclude":['animal',"animals",'cadaver','cadaveric'],
    "GEN":['transplant',"transfer",'anastomosis','transplantation'],
"NT":['nerve graft','nerve transfer','facial nerve','facial nerve grafting',
                   'nerve grafting','cable graft','nerve harvest'],
"NT-CF":["cfng","cross-face", "cross facial", "cross face",
            "cross-mental", "cross-facial", "cross-face nerve grafting"],
"NT-M":["masseteric","masseteric nerve", "masseter nerve", "masseteric-to-facial",'trigeminal nerve','trigeminal','ipsilateral nerve'],
"NT-H":["hypoglossal", "hypoglossal-to-facial",'ansa cervicalis','faciohypoglossal',"hypoglossal-facial nerve"],
"NT-O":['posterior auricular nerve','muscle-nerve-muscle','great auricular nerve',"infracostal nerve",'sural nerve','deep temporal nerves',
          'interposition nerve','spinal accessory nerve',
          'mylohyoid nerve','suprascapular nerve','long throracic nerve',
          'intercostal nerve','radial nerve', 'neuroanastomosis',
          'homolateral eighth cranial nerve','intratemporal facial nerve','femoral cutaneous nerve',
          'phrenic nerve','obturator nerve','thoracodorsal','thoracodorsal nerve','abducens nerve',
          'vestibulocochlear nerve','long saphenous nerve graft','hemihypoglossal-facial nerve anastomosis',
          'HHFA','faciohypoglossal','faciohypoglossal transposition','motor nerve'],
 "FF":['free flap','free','muscle transplant','flap'],
            
            "FF-G":["gracilis muscle",'fgmt','gracilis-muscle','free gracilis-muscle','free gracilis'],
 "FF-O":['free latissimus','fascia lata','sternocleidomastoid muscle','sternohyoid muscle','sternohyoid','free','free muscle',
          'free muscle transfer','muscle as a donor','free muscle transplants','sartorius flap','sartorius',
          'serratus anterior muscle','zmin and zmaj','free anterolateral thigh flap', 'anterolateral thigh flap',
          'alt','lateral trapezius flap','latissimus dorsi','latissimus','omohyoid', 'pectoralis major','pectoralis minor',
          'free platysma','platysma',' extensor digitorum brevis','adductor longus','biceps femoris','rectus femoris','rectus abdominis',
          'teres major','trapezius','extensor digitorum','dual-vector flap','biceps femoris muscle','musculoseptal flap',
          'peroneus brevis free flap','peroneus brevis','tensor fascia lata','fascial','fascia','abductor hallucis','palmaris longus tendon','palmaris longus']
,
 "OT-L":['regional muscle transposition','local muscle transfer','temporalis','temporalis flap','masseter','masseter flap',
            'local flap','digastric','pedicle flap transfer','platysma myocutaneous flap',
            'oris','obicularis oculi','masseter muscle transfer']}
st.markdown("""
            <style>
                .block-container {
                    padding-top: 1rem;
                    padding-bottom: 1rem;
                    padding-left: 5rem;
                    padding-right: 5rem;
                }
            </style>
           """, unsafe_allow_html=True)

st.markdown("""<style>
            .entity {
   display:inline-block;
}</style>""", unsafe_allow_html=True)
def create_patterns(nlp, phrase_dict):
    patterns = {}
    for key, texts in phrase_dict.items():
        patterns[key] = [nlp.make_doc(text.lower()) for text in texts]
    return patterns

def resolve_overlaps(matches, doc):
    sorted_matches = sorted(matches, key=lambda m: (m[1], -m[2]))
    resolved_entities = []
    seen_tokens = set()

    for match_id, start, end in sorted_matches:
        if start in seen_tokens or any(token in seen_tokens for token in range(start, end)):
            continue

        resolved_entities.append(Span(doc, start, end, label=nlp.vocab.strings[match_id]))
        seen_tokens.update(range(start, end))

    return resolved_entities

def process_text(text, nlp, procedures):
    patterns = create_patterns(nlp, procedures)
    matcher = PhraseMatcher(nlp.vocab, attr="LOWER")
    for key, pattern in patterns.items():
        matcher.add(key, pattern)
    
    doc = nlp(text)
    matches = matcher(doc)
    new_ents = resolve_overlaps(matches, doc)
    doc.ents = new_ents
    return doc

# models = ["en_core_web_sm", "en_core_web_md"]

# emojis: https://www.webfx.com/tools/emoji-cheat-sheet/


@st.cache_data #(show_spinner=False, allow_output_mutation=True, suppress_st_warning=True)
def load_data(source_file):
    """Load data from a CSV file."""
    return pd.read_csv(source_file)

def update_data_entry(df, index, entry):
    """Update a single entry in the DataFrame."""
    for key, value in entry.items():
        if key in df.columns:
            df.at[index, key] = value
    return df

def get_data_from_csv(source_file):
    df = pd.read_csv(source_file)
    return df
# def update_submit():
#         st.session_state.submitted = True
def pmid_to_index():
    st.session_state.indx = pmids.index(st.session_state.pmid_selection)
@st.cache_data#(allow_output_mutation=True)
def get_data():
    return []
def update_data(): #df,pmid_in,patients_in, age_in, min_age_in, max_age_in, min_time_to_reinnervation_in, max_time_to_reinnervation_in, min_follow_up_in, max_follow_up_in
    get_data().append(
                {"PMID": float(pmid), 
                "Patients": float(patients), 
                "Age": float(age), 
                "Min Age": float(min_age), 
                "Max Age": float(max_age), 
                "Min Time to Reinnervation": float(min_time_to_reinnervation), 
                "Max Time to Reinnervation": float(max_time_to_reinnervation), 
                "Min Follow up": float(min_follow_up), 
                "Max Follow up": float(max_follow_up)})  
    # file_to_download=pd.DataFrame(get_data())
    df.loc[article_index,'patients']=float(patients)
    df.loc[article_index,'time_to_reinnervation_(min)']=float(min_time_to_reinnervation)
    df.loc[article_index,'time_to_reinnervation_(max)']= float(max_time_to_reinnervation)
    df.loc[article_index,'Age']= float(age)
    df.loc[article_index,'min age']= float(min_age)
    df.loc[article_index,'max age']= float(max_age)
    df.loc[article_index,'follow up min']= float(min_follow_up)
    df.loc[article_index,'follow up max']= float(max_follow_up)
    return df #,file_to_download #.to_csv('./data/30-09-22_Facial-reanimation_data_time-to-reinnervation_v0002.csv', index=False)

    
    
def index_to_pmid():
    # update_data()#df,pmid_in,patients_in, age_in, min_age_in, max_age_in, min_time_to_reinnervation_in, max_time_to_reinnervation_in, min_follow_up_in, max_follow_up_in
    if st.session_state.indx < len(pmids)-1:
        st.session_state.indx +=1 
        st.session_state.pmid_selection = pmids[st.session_state.indx]
# def next_index_to_pmid():
#     if st.session_state.indx < len(pmids)-1:
#         st.session_state.indx +=1 
#         st.session_state.pmid_selection =pmids[st.session_state.indx]
    
        # next_article.disabled=True 
def back_index_to_pmid():
    if st.session_state.indx > 0:
        st.session_state.indx -=1 
        st.session_state.pmid_selection =pmids[st.session_state.indx]
        

# get_data_from_csv(files[selected_source_file])


df = get_data_from_csv('./data/8-10-22_Facial-reanimation_data_extraction_with_time_to_reinervation_linkedDB.csv')
pmids=df['pmid'].to_list()
# my_list = pmids
# sidebar = st.sidebar
with st.sidebar:
    # st.[element_name]
# buffer,back_button,select, next_button,buffer = st.columns([3,1,2,1,3])
# with back_button:
#     st.write(' ')
#     st.write(' ')
    bck,pumedid,nxt=st.columns([1,2,1])
    with bck:
        st.button("Back", key="back",on_click=back_index_to_pmid)
    with nxt:
        next_article=st.button("Next", key="next",on_click=index_to_pmid,disabled=False)
    with pumedid:
        pmid_selection = st.selectbox('PMID' ,pmids,key='pmid_selection',on_change =  pmid_to_index,label_visibility="hidden")    
        

    
    
#find index of selected pmid    

if 'indx' not in st.session_state:
    st.session_state['indx'] = pmids.index(st.session_state.pmid_selection) #set index to index of selected pmid

article_index=df[df['pmid'] == pmid_selection].index[0]


patients = df['patients'].loc[article_index]
    
models = load_models()


doc_title = df['title'].loc[article_index]

text_input = df['abstract'].loc[article_index]
selected_model = models["en"]
doc = selected_model(text_input)
# docOut = nlp(doc)
# anonymized_tokens = process_text(doc)
height = int(len(text_input) * 0.5) + 10

expander_title="Click to read: "+ doc_title +" (Abstract)"


# st.write(' ')
# st.write(' ')
# with st.expander(expander_title):
st.markdown(f"**{doc_title}**")
# annotated_text(*anonymized_tokens)
# spacy_streamlit.visualize(models, text_input)
v_abstract= process_text(doc, nlp, procedures)
processed_html =displacy.render(v_abstract, style="ent", jupyter=False, options={
        "colors": {
            "NT": "#BEA375",
            "NT-CF": "#AC8336",
            "NT-M": "#E1785C",
            "NT-H": "#B88965",
            "NT-O": "#E18B58",
            "FF": "#D8588C",
            "FF-G": "#3AC1E6",
            "FF-O": "#b0e0e6",
            "OT-L": "#5851A5",
            "Exclude":"red",
            "GEN":"yellow",
        }
        })
    # processed_html
st.markdown(processed_html, unsafe_allow_html=True)
# visualize_spans(docOut, spans_key="job_role", displacy_options={"colors": {"CEO": "#09a3d5"}})
pmid =pmid_selection


min_time_to_reinnervation = df['time_to_reinnervation_(min)'][df['pmid']== pmid_selection].values[0]
max_time_to_reinnervation = df['time_to_reinnervation_(max)'][df['pmid']== pmid_selection].values[0]
age= df['Age'][df['pmid']== pmid_selection].values[0]
min_age= df['min age'][df['pmid']== pmid_selection].values[0]
max_age= df['max age'][df['pmid']== pmid_selection].values[0]
min_follow_up= df['follow up min'][df['pmid']== pmid_selection].values[0]
max_follow_up= df['follow up max'][df['pmid']== pmid_selection].values[0]
# form_col,article= st.columns([3,10])

# with form_col:
percent_complete=((st.session_state.indx)/(len(pmids)-1))
articles_remaining=len(pmids)-st.session_state.indx-1
# st.metric(label="Completion", value=f"{round(percent_complete*100)}%", delta=-articles_remaining)

with st.form(key='Paper_Details', clear_on_submit=True):
    pmid_in= pmid
    patients = st.text_input('Patients', value=patients)
    age = st.text_input('Age', value=age)
    min_age = st.text_input('Min Age', value=min_age)
    max_age = st.text_input('Max Age', value=max_age)
    min_time_to_reinnervation = st.text_input('Min Time to Reinnervation', value=min_time_to_reinnervation)
    max_time_to_reinnervation = st.text_input('Max Time to Reinnervation', value=max_time_to_reinnervation)
    min_follow_up = st.text_input('Min Follow up', value=min_follow_up)
    max_follow_up = st.text_input('Max Follow up', value=max_follow_up)
    submitted=st.form_submit_button("Save")
    if submitted:
        df=update_data()
        df.to_csv('./data/30-09-22_Facial-reanimation_data_time-to-reinnervation_v0002.csv', index=False) 
        st.experimental_rerun()

    
            
            
nav_back,nav_forward,padding = st.columns([1,1,8])
with nav_forward:
    forward=st.button("Next", key="forward",on_click=index_to_pmid)
   
with nav_back:
    back=st.button("Back", key="backward",on_click=back_index_to_pmid)
# Paper_Details     
# my_lit=pd.read_csv('./data/my_lit.csv')
filename=f"{pmid}_sci_hub.pdf" #'10474465_sci_hub.pdf'#
filelink='https://storage.googleapis.com/facial-reanimation.appspot.com/downloaded_articles/'+filename

# with article:        
#     my_bar = st.progress(0)
    
#     my_bar.progress(percent_complete)
    
#     link1=gen_html(filelink,filename)
#     try:
#         components.html(link1, height=750)
#     except:
#         st.markdown("# The full text is not available in the folder")
# components.iframe(src='https://docs.google.com/spreadsheets/d/1LlFmB-apPVuC7iBtO7_QxkVnyGXvNjIWB45H-0dTkWw/edit?usp=sharing', height=1000)

# st.write(pd.DataFrame(get_data()))
file_to_download=pd.DataFrame(get_data())
# @st.cache
def convert_df(df):
   return df.to_csv().encode('utf-8')


csv = convert_df(df)
input_csv = convert_df(file_to_download)

st.download_button(
   "Download Main Dataframe as CSV",
   csv,
   "file.csv",
   "text/csv",
   key='download-csv'
)
st.download_button(
   "Download input df  as CSV",
   input_csv ,
   "file.csv",
   "text/csv",
   key='download-input_csv'
)
df
# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            MainMenu {visibility: visible;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
