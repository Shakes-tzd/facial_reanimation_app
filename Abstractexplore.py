import pandas as pd  # pip install pandas openpyxl
import streamlit as st  # pip install streamlit
from annotated_text import annotated_text
import streamlit.components.v1 as components
from fr_modules.fr_text_analysis import load_models, process_text, resamble, map_entities
from fr_modules.html_gen import gen_html

# emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title="Facial Reanimation Article Explorer",
                   page_icon="📑", layout="wide")

@st.cache(show_spinner=False, allow_output_mutation=True, suppress_st_warning=True)
def get_data_from_csv(source_file):
    df = pd.read_csv(source_file)
    return df
# def update_submit():
#         st.session_state.submitted = True
def pmid_to_index():
    st.session_state.indx = pmids.index(st.session_state.pmid_selection)
@st.cache(allow_output_mutation=True)
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
    
    st.session_state.indx +=1 
    st.session_state.pmid_selection = pmids[st.session_state.indx]
def next_index_to_pmid():
    st.session_state.indx +=1 
    st.session_state.pmid_selection =pmids[st.session_state.indx]
def back_index_to_pmid():
    if st.session_state.indx > 0:
        st.session_state.indx -=1 
        st.session_state.pmid_selection =pmids[st.session_state.indx]

# get_data_from_csv(files[selected_source_file])


df = get_data_from_csv('./data/30-09-22_Facial-reanimation_data_time-to-reinnervation_v0002.csv')
pmids=df['pmid'].to_list()
# my_list = pmids
# sidebar = st.sidebar

back_button,select, next_button,abstr = st.columns([1,2,1,10])
with back_button:
    st.write(' ')
    st.write(' ')
    st.button("      Back       ", key="back",on_click=back_index_to_pmid)
        
with next_button:
    st.write(' ')
    st.write(' ')
    st.button("      Next       ", key="next",on_click=next_index_to_pmid)
        
with select:
    pmid_selection = st.selectbox('PMID' ,pmids,key='pmid_selection',on_change =  pmid_to_index)
    
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
anonymized_tokens = process_text(doc)
height = int(len(text_input) * 0.5) + 10

expander_title="Click to read: "+ doc_title +" (Abstract)"

with abstr:
    st.write(' ')
    st.write(' ')
    with st.expander(expander_title):
            # st.markdown(f"**{doc_title}**")
            annotated_text(*anonymized_tokens)
pmid =pmid_selection# df['pmid'][df['pmid']== pmid_selection].values[0]
# if 'submitted' not in st.session_state:
#     st.session_state['submitted' ]=False
# if st.session_state.submitted:
#         df=update_data()
#         df.to_csv('./data/30-09-22_Facial-reanimation_data_time-to-reinnervation_v0002.csv', index=False) 
#         st.session_state['submitted' ]=False  


min_time_to_reinnervation = df['time_to_reinnervation_(min)'][df['pmid']== pmid_selection].values[0]
max_time_to_reinnervation = df['time_to_reinnervation_(max)'][df['pmid']== pmid_selection].values[0]
age= df['Age'][df['pmid']== pmid_selection].values[0]
min_age= df['min age'][df['pmid']== pmid_selection].values[0]
max_age= df['max age'][df['pmid']== pmid_selection].values[0]
min_follow_up= df['follow up min'][df['pmid']== pmid_selection].values[0]
max_follow_up= df['follow up max'][df['pmid']== pmid_selection].values[0]
form_col,article= st.columns([3,10])

with form_col:
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

    
            
            
nav_back,nav_forward,padding = st.columns([1,1,10])
with nav_forward:
    forward=st.button("      Next       ", key="forward",on_click=index_to_pmid)   
with nav_back:
    back=st.button("      Back       ", key="backward",on_click=back_index_to_pmid)
# Paper_Details     
# my_lit=pd.read_csv('./data/my_lit.csv')
filename=f"{pmid}_sci_hub.pdf" #'10474465_sci_hub.pdf'#
filelink='https://storage.googleapis.com/facial-reanimation.appspot.com/downloaded_articles/'+filename

with article:        
    my_bar = st.progress(0)
    percent_complete=((st.session_state.indx)/len(pmids))
    my_bar.progress(percent_complete)
    
    link1=gen_html(filelink,filename)
    try:
        components.html(link1, height=750)
    except:
        st.markdown("# The full text is not available in the folder")


st.write(pd.DataFrame(get_data()))
file_to_download=pd.DataFrame(get_data())
@st.cache
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
# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            MainMenu {visibility: visible;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
