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
def pmid_to_index():
    st.session_state.indx = pmids.index(st.session_state.pmid_select)
@st.cache(allow_output_mutation=True)
def get_data():
    return []
def update_data(df,pmid,patients_in, age_in, min_age_in, max_age_in, min_time_to_reinnervation_in, max_time_to_reinnervation_in, min_follow_up_in, max_follow_up_in):
    get_data().append(
            {"PMID": pmid, 
             "Patients": float(patients_in), 
             "Age": float(age_in), 
             "Min Age": float(min_age_in), 
             "Max Age": float(max_age_in), 
             "Min Time to Reinnervation": float(min_time_to_reinnervation_in), 
             "Max Time to Reinnervation": float(max_time_to_reinnervation_in), 
             "Min Follow up": float(min_follow_up_in), 
             "Max Follow up": float(max_follow_up_in)})
    
    df.loc[article_index,'patients']=float(patients_in)
    df.loc[article_index,'time_to_reinnervation_(min)']=float(min_time_to_reinnervation_in)
    df.loc[article_index,'time_to_reinnervation_(max)']= float(max_time_to_reinnervation_in)
    df.loc[article_index,'Age']= float(age_in)
    df.loc[article_index,'min age']= float(min_age_in)
    df.loc[article_index,'max age']= float(max_age_in)
    df.loc[article_index,'follow up min']= float(min_follow_up_in)
    df.loc[article_index,'follow up max']= float(max_follow_up_in)
    df.to_csv('./data/30-09-22_Facial-reanimation_data_time-to-reinnervation_v0002.csv', index=False)
def index_to_pmid():
    update_data(df,pmid,patients_in, age_in, min_age_in, max_age_in, min_time_to_reinnervation_in, max_time_to_reinnervation_in, min_follow_up_in, max_follow_up_in)
    st.session_state.indx +=1 
    st.session_state.pmid_select =my_list[st.session_state.indx]
def next_index_to_pmid():
    st.session_state.indx +=1 
    st.session_state.pmid_select =my_list[st.session_state.indx]
def back_index_to_pmid():
    if st.session_state.indx > 0:
        st.session_state.indx -=1 
        st.session_state.pmid_select =my_list[st.session_state.indx]

# get_data_from_csv(files[selected_source_file])
df = get_data_from_csv('./data/30-09-22_Facial-reanimation_data_time-to-reinnervation_v0002.csv')


pmids=df['pmid'].to_list()
my_list = pmids
# sidebar = st.sidebar

back_button,select, next_button,space = st.columns([1,2,1,10])
with back_button:
    st.write(' ')
    st.write(' ')
    st.button("      Back       ", key="back",on_click=back_index_to_pmid)
        
with next_button:
    st.write(' ')
    st.write(' ')
    st.button("      Next       ", key="next",on_click=next_index_to_pmid)
        
with select:
    pmid_select = st.selectbox('PMID' ,pmids,key='pmid_select',on_change =  pmid_to_index)
pmid_index=pmids.index(st.session_state.pmid_select)
if 'indx' not in st.session_state:
    st.session_state['indx'] = pmid_index
selected=(my_list[st.session_state.indx])
article_index=df[df['pmid'] == selected].index[0]


patients = df['patients'].loc[article_index]
    
    



models = load_models()


doc_title = df['title'].loc[article_index]
# width, height = pyautogui.size()
text_input = df['abstract'].loc[article_index]
selected_model = models["en"]
doc = selected_model(text_input)
anonymized_tokens = process_text(doc)
height = int(len(text_input) * 0.5) + 10

    # st.write('Expand to read the abstract')
# st.write("###",doc_title)
expander_title="Click to read: "+doc_title +" (Abstract)"

# st.session_state.article_index=article_index




pmid = df['pmid'][df['pmid']== pmid_select].values[0]
min_time_to_reinnervation = df['time_to_reinnervation_(min)'][df['pmid']== pmid_select].values[0]
max_time_to_reinnervation = df['time_to_reinnervation_(max)'][df['pmid']== pmid_select].values[0]
age= df['Age'][df['pmid']== pmid_select].values[0]
min_age= df['min age'][df['pmid']== pmid_select].values[0]
max_age= df['max age'][df['pmid']== pmid_select].values[0]
min_follow_up= df['follow up min'][df['pmid']== pmid_select].values[0]
max_follow_up= df['follow up max'][df['pmid']== pmid_select].values[0]
form,article= st.columns([3,10])
with form:
    with st.form(key='Paper Details', clear_on_submit=True):
        # inp1, inp2, inp3, inp4 = st.columns(4)
        # with inp1:
        patients_in = st.text_input('Patients', value=str(df['patients'].loc[article_index]))
        age_in = st.text_input('Age', value=str(age))
        # with inp2:
        min_age_in = st.text_input('Min Age', value=str(min_age))
        max_age_in = st.text_input('Max Age', value=str(max_age))
        # with inp3:
        min_time_to_reinnervation_in = st.text_input('Min Time to Reinnervation', value=str(min_time_to_reinnervation))
        max_time_to_reinnervation_in = st.text_input('Max Time to Reinnervation', value=str(max_time_to_reinnervation))
    # with inp4:
        min_follow_up_in = st.text_input('Min Follow up', value=str(min_follow_up))
        max_follow_up_in = st.text_input('Max Follow up', value=str(max_follow_up))
        
        submitted=st.form_submit_button("Save",on_click=index_to_pmid)
    
# df['link'] 
with article:        
    my_bar = st.progress(0)
    percent_complete=((st.session_state.indx)/len(pmids))
    with st.expander(expander_title):
        # st.markdown(f"**{doc_title}**")
        annotated_text(*anonymized_tokens)
    my_bar.progress(percent_complete)
    my_lit=pd.read_csv('./data/my_lit.csv')

    filename=f"{pmid}_sci_hub.pdf" #'10474465_sci_hub.pdf'#
    # import filename
    filelink='https://storage.googleapis.com/facial-reanimation.appspot.com/downloaded_articles/'+filename

    # df_links = pd.read_csv('pdf_file_links_2.csv')
    # index = open("pdf_render.html").read() #.format(url=filelink, location=filename)
    # index

    link1=gen_html(filelink,filename)
    # Func = open("link1.html","w")
    # Func.write(link1)
    # Func.close()

    # st.markdown("""---""")    
    # HtmlFile = open("link1.html", 'r', encoding='utf-8')
    # source_code = HtmlFile.read() 
    # print(source_code)
    # components.html(source_code)
    try:
        # file_link=df_links['link'][df_links['pmid']== pmid].values[0]
        # file_link=file_link.replace('view?usp=drivesdk','preview')
        # components.iframe(file_link,  height=1000)
        components.html(link1, height=1000)
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
