import streamlit as st
import pandas as pd 
from numerize.numerize import numerize
from datetime import datetime
import plotly.express as px
import plotly.subplots as sp
import time
import matplotlib.pyplot as plt

#set page
now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
st.set_page_config(page_title="Mapato | Dashboard", page_icon="🌎", layout="wide")  
st.subheader(f"📈 Buhigwe Mapato Dashboard 🕒 {now}")


# load CSS Style
with open('style.css')as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)

#get data from mysql

# df = pd.read_csv('csv_collection_transactions.csv', encoding='latin1')
df = pd.read_excel('excel_collection_transactions.xlsx', sheet_name='Sheet1')

#switcher

st.sidebar.header("Please filter")



region= st.sidebar.multiselect(
    "Select the Region:",
    options=df["Region"].unique(),
    default=df["Region"].unique(),
)
district = st.sidebar.multiselect(
    "Select the District:",
    options=df["District"].unique(),
    default=df["District"].unique(),
)
ward = st.sidebar.multiselect(
    "Select the Ward:",
    options=df["Ward"].unique(),
    default=df["Ward"].unique(),
)

df['Date'] = pd.to_datetime(df['Date'])
date_range = st.sidebar.date_input("Select date range", [df['Date'].min(), df['Date'].max()])

start_date, end_date = date_range

start_str = pd.to_datetime(start_date).strftime('%d-%m-%Y')
end_str = pd.to_datetime(end_date).strftime('%d-%m-%Y')

num_days = (end_date - start_date).days + 1


df_selection=df.query(
    "Region==@region & District==@district & Ward ==@ward & Date >= @start_str and Date <= @end_str"
)



#variables
target=1515838600
nonprotected=1310727600
protected=205111000

target_perday=target/num_days

overall_collected=df_selection['Amount'].sum()
overall_collected_percent=round((overall_collected/target*100),2)

nonprotected_collected = df_selection.query("SourceCategory == 'Non-Protected'")['Amount'].sum()
nonprotected_collected_percent=round((nonprotected_collected/nonprotected*100),2)

protected_collected = df_selection.query("SourceCategory == 'Protected'")['Amount'].sum()
protected_collected_percent=round((protected_collected/protected*100),2)


collection_by_month = df_selection.groupby(by=["Month"]).count()[["Amount"]].sort_values(by="Month")


pos_collection = df_selection.query("SourceType == 'POS'")['Amount'].sum()
service_levy_collection = df_selection.query("SourceType == 'SERVICE LEVY'")['Amount'].sum()
business_licence_collection = df_selection.query("SourceType == 'BUSINESS LICENCE'")['Amount'].sum()
land_sales_collection = df_selection.query("SourceType == 'LAND SALES'")['Amount'].sum()
building_permit_collection = df_selection.query("SourceType == 'BUILDING PERMIT'")['Amount'].sum()
bilboards_collection = df_selection.query("SourceType == 'BILBOARDS'")['Amount'].sum()
property_tax_collection = df_selection.query("SourceType == 'PROPERTY TAX'")['Amount'].sum()












#-----PROGRESS BAR-----
# Define at the top
container,= st.columns(1)
def ProgressBar():
    target = 1515838600
    collected = df_selection['Amount'].sum()
    progress = collected / target

    with container:
        st.progress(progress)
        st.markdown(f"""
<div style="font-size: 20px; color: #1a73e8; font-weight: 600;">
    Collected: {collected:,.0f} / Target: {target:,.0f} ({progress:.2%})
</div>
""", unsafe_allow_html=True)
# def ProgressBartwo():
#   st.markdown("""<style>.stProgress > div > div > div > div { background-image: linear-gradient(to right, #99ff99 , #FFFF00)}</style>""",unsafe_allow_html=True,)
#   target=12646805000
#   current=df_selection['Amount'].sum()
#   percent=round((current/target*100))
#   my_bar = st.progress(0)

#   if percent>100:
#     st.subheader("Congratulation Target 100 complited")
#   else:
#    st.write("You have ", percent, " % " ," of ", (format(target, ',d')), " TZS")
#    for percent_complete in range(percent):
#     time.sleep(0.1)
#     my_bar.progress(percent_complete + 1,text="Target percentage")
















def head_card(title, value,color):
    st.markdown(f"""
        <div style="
            background-color: {color};
            padding: 10px;
            border-color: green;
            border-radius: 15px;
            box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
            text-align: center;
            font-family: 'Arial';
        ">
            <h4 style="color:white; margin-bottom: 5px;">{title}</h4>
            <h2 style="color:white; margin: 0;">{value}</h2>
        </div>
    """, unsafe_allow_html=True)





col4, col5, col6= st.columns(3)
with col4:
    head_card(" 💰 OVERALL", f"TZS {overall_collected:,} - {overall_collected_percent}%", "#5409DA")
with col5:
    head_card(" 💰 UNPROTECTED", f"TZS {nonprotected_collected:,} - {nonprotected_collected_percent}%", "#309898")
with col6:
    head_card(" 💰 UNPROTECTED", f"TZS {protected_collected:,} - {protected_collected_percent}%", "#670D2F")


st.markdown("&nbsp;", unsafe_allow_html=True)  # Adds vertical space











#pie chat ya collected vs uncloocted na protected vs unproted na Wilayas
div1, div2, div3=st.columns(3)

def pieCollected():
    with div1:  # or use `div1` if it's already defined
        target_collection = 1515838600
        collected = df_selection['Amount'].sum()
        uncollected = target_collection - collected
        labels = ['Collected', 'Uncollected']
        collection = [collected, uncollected]
        # Create a DataFrame for Plotly
        pie_data = {
            'Status': labels,
            'Amount': collection
        }
        custom_colors = {
            'Collected': '#00CC96',     # green
            'Uncollected': '#EF553B'    # red/orange
        }

        fig = px.pie(
            pie_data,
            values='Amount',
            names='Status',
            hole=0.3,
            color='Status',
            color_discrete_map=custom_colors
        )

        fig.update_layout(
            title_text="COLLECTED VS UNCOLLECTED",
            title_x=0.2,
            margin=dict(t=40, b=20, l=0, r=0),
            showlegend=True
        )

        st.plotly_chart(fig, use_container_width=True)

def pieProtected():
    with div2:  # or use `div1` if it's already defined
        target_collection = 1515838600
        collected = df_selection['Amount'].sum()
        uncollected = target_collection - collected
        labels = ['Protected', 'Unprotected']
        collection = [collected, uncollected]
        # Create a DataFrame for Plotly
        pie_data = {
            'Status': labels,
            'Amount': collection
        }
        custom_colors = {
            'Protected': '#3A0519',     # green
            'Unprotected': '#537D5D'    # red/orange
        }

        fig = px.pie(
            pie_data,
            values='Amount',
            names='Status',
            hole=0.0,
            color='Status',
            color_discrete_map=custom_colors
        )

        fig.update_layout(
            title_text="PROTECTED VS UNPROTECTED",
            title_x=0.2,
            margin=dict(t=40, b=20, l=0, r=0),
            showlegend=True
        )

        st.plotly_chart(fig, use_container_width=True)

def barchartdistrictwise():
    with div3:
        grouped_df = df_selection.groupby('District', as_index=False)['Amount'].sum()

        # Create bar chart
        fig = px.bar(
            grouped_df,
            y='Amount',
            x='District',
            text_auto='.2s',
            title="COLLECTION BY COUNCIL"
        )

        # Optional: center title and style
        fig.update_layout(
            title_x=0.2,
            xaxis_title="Council",
            yaxis_title="Total Amount Collected"
        )

        st.plotly_chart(fig, use_container_width=True)






# Using the rounded subheader style
st.subheader(f"💰 Collection by Main Source")

def style_metric_card(title, value,color):
    st.markdown(f"""
        <div style="
            background-color: {color};
            padding: 10px;
            border-radius: 15px;
            box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
            text-align: center;
            font-family: 'Arial';
        ">
            <h4 style="color:white; margin-bottom: 5px;">{title}</h4>
            <h2 style="color:white; margin: 0;">{value}</h2>
        </div>
    """, unsafe_allow_html=True)




col4, col5, col6= st.columns(3)
with col4:
    style_metric_card(" 🧾 POS COLLECTION", f"TZS {pos_collection:,}", "#4CAF50")
with col5:
    style_metric_card(" 📋 SERVICE LEVY", f"TZS {service_levy_collection:,}", "#2196F3")
with col6:
    style_metric_card(" 📜🏛️ BUSINESS LICENCE", f"TZS {business_licence_collection:,}", "#FF5722")


st.markdown("&nbsp;", unsafe_allow_html=True)  # Adds vertical space


col4, col5, col6,col7= st.columns(4)
with col4:
    style_metric_card(" 🏞️💰 LAND SALES", f"TZS {land_sales_collection:,}", "#2196F3")
with col5:
    style_metric_card(" 🚧📄 BUILDING PERMIT", f"TZS {building_permit_collection:,}", "#4CAF50")
with col6:
    style_metric_card(" 🏙️ BILLBOARDS", f"TZS {bilboards_collection:,}", "#FF5722")
with col7:
    style_metric_card(" 🏠💵🧾 PROPERTY TAX", f"TZS {property_tax_collection:,}", "#2196F3")


st.markdown("&nbsp;", unsafe_allow_html=True)  # Adds vertical space


# Create div
col1, = st.columns(1)

# Bar chart by Month
def barchartByMonth():
    with col1:
        month_order = [
            'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
            'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
        ]
        # Ensure Month column is ordered correctly
        df_selection['Month'] = pd.Categorical(df_selection['Month'], categories=month_order, ordered=True)
        grouped_df = df_selection.groupby('Month', as_index=False)['Amount'].sum()
        # Create bar chart
        fig = px.bar(
            grouped_df,
            y='Amount',
            x='Month',
            text_auto='.2s',
            title="COLLECTION BY COUNCIL"
        )
        # Optional: center title and style
        fig.update_layout(
            title_x=0.2,
            xaxis_title="Month",
            yaxis_title="Amount Collected"
        )
        st.plotly_chart(fig, use_container_width=True)
#pie chart



st.markdown("&nbsp;", unsafe_allow_html=True)  # Adds vertical space





# Create div
col1, = st.columns(1)
# Bar chart by Month
def barchartByWard():
    with col1:
        grouped_df = df_selection.groupby('Ward', as_index=False)['Amount'].sum()
        grouped_df = grouped_df.sort_values('Ward')  # Sort by Ward name alphabetically
        # Create bar chart
        fig = px.bar(
            grouped_df,
            y='Amount',
            x='Ward',
            text_auto='.2s',
            title="COLLECTION BY Ward"
        )
        # Optional: center title and style
        fig.update_layout(
            title_x=0.2,
            xaxis_title="Ward",
            yaxis_title="Amount Collected"
        )
        st.plotly_chart(fig, use_container_width=True)
# Sample data








#option menu
from streamlit_option_menu import option_menu
with st.sidebar:
        selected=option_menu(
        menu_title="Main Menu",
         #menu_title=None,
        options=["Home","Table"],
        icons=["house","book"],
        menu_icon="cast", #option
        default_index=0, #option
        orientation="vertical",
        )
 

if selected=="Home":
    ProgressBar()
    pieProtected()
    pieCollected()
    barchartdistrictwise()
    barchartByMonth()
    barchartByWard()



if selected=="Table":
   table()
   table_district()
   st.dataframe(df_selection.describe().T,use_container_width=True)
 

 
 
