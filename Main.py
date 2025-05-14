import streamlit as st
import pandas as pd 
from numerize.numerize import numerize


#set page
now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
st.set_page_config(page_title="Mapato | Dashboard", page_icon="🌎", layout="wide")  
st.subheader(f"📈 Kigoma Mapato Dashboard 🕒 {now}")


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
target=12646805000
nonprotected=9000000000
protected=3000000000

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


st.markdown("""
    <style>
        .border-box {
            border: 3px solid #4CAF50;   /* Green border */
            border-radius: 10px;         /* Rounded corners */
            padding: 20px;               /* Space inside the border */
            background-color: #f9f9f9;   /* Light background */
            height: 100%;
        }
    </style>
""", unsafe_allow_html=True)

# Define columns
col1, col2 = st.columns(2)

# Use HTML to apply a border inside col1
with col1:
    st.markdown('<div class="border-box">', unsafe_allow_html=True)
    st.subheader("Bordered Column")
    st.write("This content is inside a bordered container.")
    st.markdown('</div>', unsafe_allow_html=True)

# Plain content in col2
with col2:
    st.subheader("Regular Column")
    st.write("This column has no border.")




col4, col5, col6, = st.columns(3)
with col4.container():
    st.subheader("💰  **Overall 2024-2025**")
    st.subheader(f"Target - {target:,}")
    st.subheader(f"Collected - {overall_collected:,} - {overall_collected_percent}%")


with col5.container():
    st.markdown("###  💰  **Uprotected Collection**")
    st.subheader(f"Target - {nonprotected:,}")
    st.subheader(f"Collected - {nonprotected_collected:,} - {nonprotected_collected_percent}%")


with col6.container():
    st.markdown("### 💰 **Protected Collection**")
    st.subheader(f"Target - {protected:,}")
    st.subheader(f"Collected - {protected_collected:,} - {protected_collected_percent}%")





# Using the rounded subheader style





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

#-----PROGRESS BAR-----
def ProgressBar():
  st.markdown("""<style>.stProgress > div > div > div > div { background-image: linear-gradient(to right, #99ff99 , #FFFF00)}</style>""",unsafe_allow_html=True,)
  target=12646805000
  current=df_selection['Amount'].sum()
  percent=round((current/target*100))
  my_bar = st.progress(0)

  if percent>100:
    st.subheader("Target 100 complited")
  else:
   st.write("you have ", percent, " % " ," of ", (format(target, ',d')), " TZS")
   for percent_complete in range(percent):
    time.sleep(0.1)
    my_bar.progress(percent_complete + 1,text="Target percentage")

#create divs
div1, div2, div3=st.columns(3)

#pie chart

# Sample data

target_collection=12646805000
collected=df_selection['Amount'].sum()
uncollected=target_collection-collected

labels = ['Collected', 'Uncolected']
collection = [collected, uncollected]

# Create pie chart
fig, ax = plt.subplots()
ax.pie(collection, labels=labels, autopct='%1.1f%%', startangle=90)
ax.axis('equal')  # Equal aspect ratio ensures the pie is circular.

st.pyplot(fig)


st.markdown("&nbsp;", unsafe_allow_html=True)  # Adds vertical space


def pie():
 with div1:
  theme_plotly = None # None or streamlit
  fig = px.pie(df_selection, values='Amount', names='Department', title='Collected vs Uncollected')
  fig.update_layout(legend_title="Collection", legend_y=0.9)
  fig.update_traces(textinfo='percent+label', textposition='inside')
  st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

#bar chart by Month

def barchart():
  theme_plotly = None # None or streamlit
  with div3:
    fig = px.bar(df_selection, y='Amount', x='District', text_auto='.2s',title="Collection by Council")
    fig.update_traces(textfont_size=18, textangle=0, textposition="outside", cliponaxis=False)
    st.plotly_chart(fig, use_container_width=True, theme="streamlit")





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
    pie()
    barchart()
    barchartDistrictwise()


if selected=="Table":
   table()
   table_district()
   st.dataframe(df_selection.describe().T,use_container_width=True)
 

 
 
