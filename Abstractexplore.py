import pandas as pd  # pip install pandas openpyxl
import streamlit as st  # pip install streamlit
from annotated_text import annotated_text
import streamlit.components.v1 as components
from fr_modules.fr_text_analysis import load_models, process_text, resamble, map_entities
from fr_modules.html_gen import gen_html
import time

# emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title="Facial Reanimation Article Explorer",
                   page_icon="📑", layout="wide")

@st.cache(show_spinner=False, allow_output_mutation=True, suppress_st_warning=True)
def get_data_from_csv(source_file):
    df = pd.read_csv(source_file)
    return df


# get_data_from_csv(files[selected_source_file])
df = get_data_from_csv('30-09-22_Facial-reanimation_data_time-to-reinnervation_v0002.csv')


pmids=df['pmid'].to_list()
my_list = pmids
# sidebar = st.sidebar
left_col,right_col = st.columns([1,5])
def pmid_to_index():
    st.session_state.indx = pmids.index(st.session_state.pmid_select)

    
with left_col:
    pmid_select = st.selectbox('' ,pmids,key='pmid_select',on_change =  pmid_to_index)
    pmid_index=pmids.index(st.session_state.pmid_select)
    if 'indx' not in st.session_state:
        st.session_state['indx'] = pmid_index
    # st.session_state['article_index'] = 
    # show_next =pmid_index #st.number_input('PMID Index',  key= "indx", on_change =  index_to_pmid,value=pmid_index)
    selected=(my_list[st.session_state.indx])
    abs_num=df[df['pmid'] == selected].index[0]
    
    patients = df['patients'].loc[abs_num]
    my_bar = st.progress(0)
    



models = load_models()


doc_title = df['title'].loc[abs_num]
# width, height = pyautogui.size()
text_input = df['abstract'].loc[abs_num]
selected_model = models["en"]
doc = selected_model(text_input)
anonymized_tokens = process_text(doc)
height = int(len(text_input) * 0.5) + 10
with right_col:
    # st.write('Expand to read the abstract')
    st.write('##',doc_title)
    with st.expander("Abstract"):
        st.markdown(f"**{doc_title}**")
        annotated_text(*anonymized_tokens)
# st.session_state.abs_num=abs_num

@st.cache(allow_output_mutation=True)
def get_data():
    return []
def update_data(df,patients, age_in, min_age_in, max_age_in, min_time_to_reinnervation_in, max_time_to_reinnervation_in, min_follow_up_in, max_follow_up_in):
    get_data().append(
            {"PMID": pmid, "Patients": patients, 
             "Age": age_in, 
             "Min Age": min_age_in, 
             "Max Age": max_age_in, 
             "Min Time to Reinnervation": min_time_to_reinnervation_in, 
             "Max Time to Reinnervation": max_time_to_reinnervation_in, 
             "Min Follow up": min_follow_up_in, 
             "Max Follow up": max_follow_up_in})
    
    df.loc[abs_num,'patients']=patients
    df.loc[abs_num,'time_to_reinnervation_(min)']=min_time_to_reinnervation_in
    df.loc[abs_num,'time_to_reinnervation_(max)']= max_time_to_reinnervation_in
    df.loc[abs_num,'Age']= age_in
    df.loc[abs_num,'min age']= min_age_in
    df.loc[abs_num,'max age']= max_age_in
    df.loc[abs_num,'follow up min']= min_follow_up_in
    df.loc[abs_num,'follow up max']= max_follow_up_in
    df.to_csv('30-09-22_Facial-reanimation_data_time-to-reinnervation_v0002.csv', index=False)
def index_to_pmid():
    # 
    update_data(df,patients, age_in, min_age_in, max_age_in, min_time_to_reinnervation_in, max_time_to_reinnervation_in, min_follow_up_in, max_follow_up_in)
    st.session_state.indx +=1 
    st.session_state.pmid_select =my_list[st.session_state.indx]
def next_index_to_pmid():
    st.session_state.indx +=1 
    st.session_state.pmid_select =my_list[st.session_state.indx]
def back_index_to_pmid():
    st.session_state.indx -=1 
    st.session_state.pmid_select =my_list[st.session_state.indx]

pmid = df['pmid'].loc[abs_num]
min_time_to_reinnervation = df['time_to_reinnervation_(min)'].loc[abs_num]
max_time_to_reinnervation = df['time_to_reinnervation_(max)'].loc[abs_num]
age= df['Age'].loc[abs_num]
min_age= df['min age'].loc[abs_num]
max_age= df['max age'].loc[abs_num]
min_follow_up= df['follow up min'].loc[abs_num]
max_follow_up= df['follow up max'].loc[abs_num]

inp1, inp2, inp3, inp4,nav = st.columns(5)
with inp1:
    patients = st.number_input('Patients', value=float(patients), min_value=0.0, max_value=1000.0)
with inp2:
    age_in = st.number_input('Age', value=float(age), min_value=0.0, max_value=1000.0)
with inp3:
    min_age_in = st.number_input('Min Age', value=float(min_age), min_value=0.0, max_value=1000.0)
with inp4:
    max_age_in = st.number_input('Max Age', value=float(max_age), min_value=0.0, max_value=1000.0)
with nav:
    if st.button("      Next       ", key="next",on_click=next_index_to_pmid):
        
        percent_complete=st.session_state.indx
        my_bar.progress(percent_complete + 1)
    if st.button("      Back       ", key="back",on_click=back_index_to_pmid):
        percent_complete=st.session_state.indx
        my_bar.progress(percent_complete - 1)
    
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
    if st.button("      Save       ", key="add",on_click=index_to_pmid):
        percent_complete=st.session_state.indx
        my_bar.progress(percent_complete + 1)
        

        # for percent_complete in range(100):
        #     time.sleep(0.1)
            
        # st.session_state.indx +=1  
        # st.session_state.pmid_select =my_list[st.session_state.indx]
        

my_lit=pd.read_csv('my_lit.csv')

filename=f"{pmid}_sci_hub.pdf" #'10474465_sci_hub.pdf'#
# import filename
filelink='https://storage.googleapis.com/facial-reanimation.appspot.com/downloaded_articles/'+filename

df_links = pd.read_csv('pdf_file_links_2.csv')
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

# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            MainMenu {visibility: visible;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
