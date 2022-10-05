

import pandas as pd  # pip install pandas openpyxl
import plotly.express as px  # pip install plotly-express
import streamlit as st  # pip install streamlit

# emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title="Facial Reanimation Dashboard",
                   page_icon=":bar_chart:", layout="wide")

# ---- READ EXCEL ----


def get_data_from_excel():
    df = pd.read_csv('30-09-22_Ficial-reanimation_data_extraction_v0001.csv')
    return df


df = get_data_from_excel()
df
# df['year']=df['year'].apply(int)
# df["positive_outcome"]=df["positive_outcome"].fillna(0)
# df["tool_category"]=df["tool_category"].fillna(0)
# df["measuring_tool"]=df["measuring_tool"].fillna(0)
# df_look_up = pd.read_excel(
#         io="Complete_Facial_Reanimation_MWN.xlsx",
#         engine="openpyxl",
#         sheet_name="look_up",
#         skiprows=0,
#         usecols="A:L",
#         nrows=13,
#     )
# nerve_transfer_look_up=df_look_up[[	'nerve_transfer_key',	'nerve_transfer_value']].dropna().rename(columns={'nerve_transfer_key':'key',	'nerve_transfer_value':'value'}).set_index('value',drop=True)

# free_flap_look_up=df_look_up[[	'free_flap_key',	'free_flap_value']].dropna().rename(columns={'free_flap_key':'key',	'free_flap_value':'value'}).set_index('value',drop=True)

# other_tissue_look_up=df_look_up[[	'other_tissue_key',	'other_tissue_value']].dropna().rename(columns={'other_tissue_key':'key',	'other_tissue_value':'value'}).set_index('value',drop=True)

# positive_outcome_look_up=df_look_up[[	'positive_outcome_key',	'positive_outcome_value']].dropna().rename(columns={'positive_outcome_key':'key',	'positive_outcome_value':'value'}).set_index('value',drop=True)

# tool_category_look_up=df_look_up[[	'tool_category_key',	'tool_category_value']].dropna().rename(columns={'tool_category_key':'key',	'tool_category_value':'value'}).set_index('value',drop=True)

# measuring_tool_look_up=df_look_up[[	'measuring_tool_key',	'measuring_tool_value']].dropna().rename(columns={'measuring_tool_key':'key',	'measuring_tool_value':'value'}).set_index('value',drop=True)
# loop_up_dict={'nerve_transfer':nerve_transfer_look_up,
#          'free_flap':free_flap_look_up,
#          'positive_outcome':positive_outcome_look_up,
#          'other_tissue':other_tissue_look_up,
#          'measuring_tool':measuring_tool_look_up,
#          'tool_category':tool_category_look_up}

# def look_up(x,y):
#     return loop_up_dict[y].loc[x,'key']
# def grouped_gen(col):
#   df_att=df[[col]]
#   df_att['key']=df_att[col].apply(look_up,y=col)
#   data=df_att.groupby(by='key').count().reset_index().sort_values(by=col)
#   return data
# def pie_plotter(col,color_p):
#   import string
#   df_att=df[[col]]
#   df_att['key']=df_att[col].apply(look_up,y=col)
#   data=df_att.groupby(by='key').count().reset_index().sort_values(by=col)
#   fig = px.pie(data, values=col, names='key', labels={col:'Number of articles','key':col.replace('_',' ')  },hole=.3,color_discrete_sequence=color_p,hover_data={'key':False})
#   fig.update_traces(textposition='inside', textinfo='percent+label')
#   fig.update_layout(legend_title_text='Types of '+string.capwords(col.replace('_',' '))+'s')
#   return fig

# ---- SIDEBAR ----
st.sidebar.header("Please Filter Here:")
nerve_transfer = st.sidebar.multiselect(
    "Select the Nerve Transfer:",
    options=[df["nerve_transfer"].unique()],
    default=df["nerve_transfer"].unique(),
)

# # positive_outcomes = st.sidebar.multiselect(
# #     "Select Outcome:",
# #     options=df["Positive_Outcomes"].unique(),
# #     default=df["Positive_Outcomes"].unique(),
# # )

# # year = st.sidebar.multiselect(
# #     "Select Measuring Tool:",
# #     options=df["Year"].unique(),
# #     default=df["Year"].unique()
# # )

# # df_selection = df.query(
# #     "Year == @year & Positive_Outcomes ==@positive_outcomes & Nerve_Transfer == @nerve_transfer"
# # )

# # ---- MAINPAGE ----
# st.title("Facial Reanimation Dashboard")
# st.markdown("##")

# # TOP KPI's
# # total_sales = int(len(df_selection))
# # average_rating = round(df_selection["Tool_Category"].mean(), 1)
# # star_rating = ":star:" * int(round(average_rating, 0))
# # average_sale_by_transaction = round(df_selection["Measuring_tool"].mean(), 2)

# # left_column, middle_column, right_column = st.columns(3)
# # with left_column:
# #     st.subheader("Total Articles:")
# #     st.subheader(f"{total_sales:,}")
# # with middle_column:
# #     st.subheader("Average Tool Category:")
# #     st.subheader(f"{average_rating} {star_rating}")
# # with right_column:
# #     st.subheader("Average Tool:")
# #     st.subheader(f" {average_sale_by_transaction}")

# st.markdown("""---""")

# # SALES BY PRODUCT LINE [BAR CHART]
# # sales_by_product_line = (
# #     df_selection.groupby(by=["Nerve_Transfer"]).count()['Title']
# # )
# fig_free_flaps = pie_plotter('free_flap',px.colors.qualitative.Bold)
# fig_nerve_transfer = pie_plotter('nerve_transfer',px.colors.qualitative.Safe)

# # # SALES BY HOUR [BAR CHART]
# # sales_by_hour = df_selection.groupby(by=["Year"]).count()['Title']
# # fig_hourly_sales = px.bar(
# #     sales_by_hour,
# #     x=sales_by_hour.index,
# #     y="Title",
# #     title="<b>Sales by hour</b>",
# #     color_discrete_sequence=["#0083B8"] * len(sales_by_hour),
# #     template="plotly_white",
# # )
# # fig_hourly_sales.update_layout(
# #     xaxis=dict(tickmode="linear"),
# #     plot_bgcolor="rgba(0,0,0,0)",
# #     yaxis=(dict(showgrid=False)),
# # )


# left_column, right_column = st.columns(2)
# left_column.plotly_chart(fig_free_flaps, use_container_width=True)
# right_column.plotly_chart(fig_nerve_transfer, use_container_width=True)


# # ---- HIDE STREAMLIT STYLE ----
# hide_st_style = """
#             <style>
#             #MainMenu {visibility: hidden;}
#             footer {visibility: hidden;}
#             header {visibility: hidden;}
#             </style>
#             """
# st.markdown(hide_st_style, unsafe_allow_html=True)
