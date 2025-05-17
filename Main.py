import streamlit as st
import pandas as pd 
from numerize.numerize import numerize
from datetime import datetime
import plotly.express as px
import plotly.subplots as sp
import time
import matplotlib.pyplot as plt
import io
import xlsxwriter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
from pathlib import Path
from werkzeug.security import check_password_hash
import json
from login import login

#set page
now = datetime.now().strftime("%Y-%m-%d      %H:%M:%S")
st.set_page_config(page_title="Mapato | Dashboard", page_icon="🌎", layout="wide")  
st.subheader(f"📈 Buhigwe Mapato Dashboard 📆🕒 {now}")


# load CSS Style
with open('style.css')as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)

#get data from mysql

# df = pd.read_csv('csv_collection_transactions.csv', encoding='latin1')
df = pd.read_excel('excel_collection_transactions/excel_collection_transactions.xlsx', sheet_name='Sheet1')

#switcher

st.sidebar.header("Please filter")


# 🗂️ Load your dataframe (replace with your actual loading logic)
# df = pd.read_excel("your_file.xlsx")
# For demo purposes, ensure 'Date' is in datetime
df['Date'] = pd.to_datetime(df['Date'])

# -----------------------------
# SIDEBAR FILTERS WITH DEFAULT "All"
# -----------------------------

# REGION
region_options = ["All"] + sorted(df["Region"].dropna().unique().tolist())
region = st.sidebar.selectbox("🌍 Select Region:", region_options)

# Filter Region if not All
if region != "All":
    df = df[df["Region"] == region]

# DISTRICT
district_options = ["All"] + sorted(df["District"].dropna().unique().tolist())
district = st.sidebar.selectbox("🏙️ Select District:", district_options)

if district != "All":
    df = df[df["District"] == district]

# WARD
ward_options = ["All"] + sorted(df["Ward"].dropna().unique().tolist())
ward = st.sidebar.selectbox("📍 Select Ward:", ward_options)

if ward != "All":
    df = df[df["Ward"] == ward]

# -----------------------------
# DATE RANGE FILTER
# -----------------------------
date_range = st.sidebar.date_input("🗓️ Select date range", [df["Date"].min(), df["Date"].max()])
start_date, end_date = pd.to_datetime(date_range)

# Filter by date
df_selection = df[(df["Date"] >= start_date) & (df["Date"] <= end_date)]

# -----------------------------
# SAFETY CHECK
# -----------------------------
if df_selection.empty:
    st.warning("⚠️ No data available for selected filters.")
# else:
#     st.success(f"✅ Total {len(df_selection)} Data rows Processed records")
#     st.dataframe(df_selection, use_container_width=True)



# ------------ 📁 Upload Excel File from Sidebar ------------
st.sidebar.header("📄 Upload Excel File")
uploaded_file = st.sidebar.file_uploader("Choose an Excel file", type=["xlsx", "xls"])

if uploaded_file:
    try:
        # Get filename without extension
        file_name = Path(uploaded_file.name).stem
        folder_path = Path(f"{file_name}")
        folder_path.mkdir(parents=True, exist_ok=True)

        # Save uploaded file to the folder
        saved_file_path = folder_path / uploaded_file.name
        with open(saved_file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        # Load the file into a DataFrame
        df = pd.read_excel(saved_file_path)
        df.columns = df.columns.str.strip()

        st.success(f"✅ File saved to: {saved_file_path}")
        st.subheader("📊 Data Preview")
        st.dataframe(df, use_container_width=True)

    except Exception as e:
        st.error(f"❌ Error reading or saving file: {e}")
# else:
#     st.info("ℹ️ Please upload an Excel file to display and save.")


num_days = 1525
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
        nonprotected_collected = df_selection.query("SourceCategory == 'Non-Protected'")['Amount'].sum()
        protected_collected = df_selection.query("SourceCategory == 'Protected'")['Amount'].sum()
        labels = ['Protected', 'Unprotected']
        collection = [protected_collected, nonprotected_collected]
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
        grouped_df = df_selection[df_selection['SourceType'] == 'POS'] \
    .groupby('Month', as_index=False)['Amount'].sum()
        # Create bar chart
        fig = px.bar(
            grouped_df,
            y='Amount',
            x='Month',
            text_auto='.2s',
            title="POS COLLECTION BY COUNCIL"
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


#mysql table
# def table_district():
#    source_type_filter = 'POS'
#    grouped_df = df_selection[df_selection['SourceType'] == source_type_filter] \
# 	    .groupby('District', as_index=False)['Amount'].sum()
# 	# Show directly
#    st.subheader(f"📊 TABLE - COLLECTION BY SOURCE DISTRICTWISE {source_type_filter}")
#    st.dataframe(grouped_df, use_container_width=True)
















 #***************************** START DISTRICT BY MAIN-SOURCE ******************
df_selection.columns = df_selection.columns.str.strip()
# ** Required COLUMN *****
required_columns = {"Amount", "District", "SourceType"}
if not required_columns.issubset(df_selection.columns):
    st.error(f"❌ Data must contain: {', '.join(required_columns)}.\n\nFound: {df_selection.columns.tolist()}")
else:
    # Group & pivot
    grouped = df_selection.groupby(["District", "SourceType"], as_index=False)["Amount"].sum()
    pivot_df = grouped.pivot(index="District", columns="SourceType", values="Amount").fillna(0).reset_index()
 # Dynamically get all source types
    source_types = df_selection["SourceType"].unique().tolist()
# Ensure all source types exist in the pivot table
    for col in source_types:
        if col not in pivot_df.columns:
            pivot_df[col] = 0
# Total = sum of all source type columns
    pivot_df["Total"] = pivot_df[source_types].sum(axis=1)
    pivot_df.insert(0, "NO", range(1, len(pivot_df) + 1))
    # Add grand total row
    total_row = {
    "NO": "Total",
    "District": "",
    **{col: pivot_df[col].sum() for col in source_types},
    "Total": pivot_df["Total"].sum()
    }
    pivot_df = pd.concat([pivot_df, pd.DataFrame([total_row])], ignore_index=True)

# ---- 📥 Download as Excel ----
def to_excel(df):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Collection Summary')
    return output.getvalue()
excel_data = to_excel(pivot_df)

# ---- 📄 Download as PDF ----
def to_pdf(df):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer)
    table_data = [df.columns.tolist()] + df.astype(str).values.tolist()
    table = Table(table_data)
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('FONTSIZE', (0, 0), (-1, -1), 7),
    ])
    table.setStyle(style)
    doc.build([table])
    return buffer.getvalue()
pdf_data = to_pdf(pivot_df)

#save as PNG function
def to_png(df):
    fig, ax = plt.subplots(figsize=(8, 2 + len(df) * 0.5))
    ax.axis('off')
    table = ax.table(cellText=df.values, colLabels=df.columns, loc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(8)
    table.scale(1.2, 1.2)
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight')
    buffer.seek(0)
    return buffer

#Header and SAVE as PDF EXCEL AND PNG ICON
col11, col12, col13, col14 = st.columns([6, 1, 1, 1])
with col11:
    st.subheader("📊 District Collection Summary")
with col12:
    st.download_button("📥 Excel", data=to_excel(pivot_df),
                       file_name="collection_summary.xlsx",
                       mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
with col13:
    st.download_button("📄 PDF", data=to_pdf(pivot_df),
                       file_name="collection_summary.pdf",
                       mime="application/pdf")
with col14:
    st.download_button("🖼️ PNG", data=to_png(pivot_df),
                       file_name="collection_summary.png",
                       mime="image/png")
    # Display table
st.dataframe(pivot_df, use_container_width=True)

#***********************************END District by MAIN-SOURCE*********************
st.markdown("&nbsp;", unsafe_allow_html=True)  # Adds vertical space








#***************************** START TABLE BY SUB-SOURCE ******************
# Assume df_selection is already loaded
df_selection.columns = df_selection.columns.str.strip()

required_columns = {"Amount", "District", "ItemName"}
if not required_columns.issubset(df_selection.columns):
    st.error(f"❌ Data must contain: {', '.join(required_columns)}.\n\nFound: {df_selection.columns.tolist()}")
else:
    # Pivot: Rows = ItemName, Columns = District, Values = Sum of Amount
    pivot_df = df_selection.pivot_table(
        index="ItemName",
        columns="District",
        values="Amount",
        aggfunc="sum",
        fill_value=0
    ).reset_index()

    # Add Total column per row
    districts = [col for col in pivot_df.columns if col != "ItemName"]
    pivot_df["Total"] = pivot_df[districts].sum(axis=1)
    pivot_df.insert(0, "NO", range(1, len(pivot_df) + 1))

    # Add Grand Total row
    total_row = {
        "NO": "Total",
        "ItemName": "",
        **{district: pivot_df[district].sum() for district in districts},
        "Total": pivot_df["Total"].sum()
    }
    pivot_df = pd.concat([pivot_df, pd.DataFrame([total_row])], ignore_index=True)



    # ---- Export: Excel ----
    def to_excel(df):
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='Summary')
        return output.getvalue()

    # ---- Export: PDF ----
    def to_pdf(df):
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer)
        table_data = [df.columns.tolist()] + df.astype(str).values.tolist()
        table = Table(table_data)
        style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
            ('FONTSIZE', (0, 0), (-1, -1), 7),
        ])
        table.setStyle(style)
        doc.build([table])
        return buffer.getvalue()

#Header and SAVE as PDF EXCEL AND PNG ICON
col11, col12, col13, col14 = st.columns([6, 1, 1, 1])
with col11:
    st.subheader("📊 📊 Collection by ItemName and District")
with col12:
    st.download_button("📥 Excel", data=to_excel(pivot_df),
                       file_name="collection_summary.xlsx",
                       mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
with col13:
    st.download_button("📄 PDF", data=to_pdf(pivot_df),
                       file_name="collection_summary.pdf",
                       mime="application/pdf")
with col14:
    st.download_button("🖼️ PNG", data=to_png(pivot_df),
                       file_name="collection_summary.png",
                       mime="image/png")
    # Display table
st.dataframe(pivot_df, use_container_width=True)
#***********************************END District by MAIN-SOURCE*********************















#***********************************END District by MAIN-SOURCE*********************
# Clean column names
df_selection.columns = df_selection.columns.str.strip()

# Ensure required columns exist
required_columns = {"Amount", "ItemName", "SourceType"}
if not required_columns.issubset(df_selection.columns):
    st.error(f"❌ Data must contain: {', '.join(required_columns)}.\n\nFound: {df_selection.columns.tolist()}")
else:
    # 🔍 Filter for SourceType == "POS"
    filtered_df = df_selection[df_selection["SourceType"].str.upper() == "POS"]

    # 📊 Group by ItemName, sum Amount, get top 10
    top_items_df = (
        filtered_df.groupby("ItemName", as_index=False)["Amount"]
        .sum()
        .sort_values(by="Amount", ascending=False)
        .head(10)
    )

    # Add thousands separator
    top_items_df["Amount"] = top_items_df["Amount"].apply(lambda x: f"{x:,.0f}")

    # Add row numbers
    top_items_df.insert(0, "NO", range(1, len(top_items_df) + 1))

#Header and SAVE as PDF EXCEL AND PNG ICON
col11, col12, col13, col14 = st.columns([6, 1, 1, 1])
with col11:
    st.subheader("🏆 Top 10 POS Items by Amount (All Districts)")
with col12:
    st.download_button("📥 Excel", data=to_excel(top_items_df),
                       file_name="top_ten_items_by_Pos.xlsx",
                       mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
with col13:
    st.download_button("📄 PDF", data=to_pdf(top_items_df),
                       file_name="top_ten_items_by_Pos.pdf",
                       mime="application/pdf")
with col14:
    st.download_button("🖼️ PNG", data=to_png(top_items_df),
                       file_name="top_ten_items_by_Pos.png",
                       mime="image/png")
    # Display table
st.dataframe(top_items_df, use_container_width=True)









#***********************************Top 10 POS COLLECTION*********************
# Clean column names
df_selection.columns = df_selection.columns.str.strip()

# Ensure required columns exist
required_columns = {"Amount", "PosNo", "SourceType"}
if not required_columns.issubset(df_selection.columns):
    st.error(f"❌ Data must contain: {', '.join(required_columns)}.\n\nFound: {df_selection.columns.tolist()}")
else:
    # 🔍 Filter for SourceType == "POS"
    filtered_df = df_selection[df_selection["SourceType"].str.upper() == "POS"]

    # 📊 Group by ItemName, sum Amount, get top 10
    all_pos_df = (
        filtered_df.groupby("PosNo", as_index=False)["Amount"]
        .sum()
        .sort_values(by="Amount", ascending=False)
    )

    # Add thousands separator
    all_pos_df["Amount"] = all_pos_df["Amount"].apply(lambda x: f"{x:,.0f}")

    # Add row numbers
    all_pos_df.insert(0, "NO", range(1, len(all_pos_df) + 1))

#Header and SAVE as PDF EXCEL AND PNG ICON
col111, col121, col131, col141 = st.columns([6, 1, 1, 1])
with col111:
    st.subheader("POS Collection by Amount")
with col121:
    st.download_button("📥 Excel", data=to_excel(all_pos_df),
                       file_name="Pos_Collection.xlsx",
                       mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
with col131:
    st.download_button("📄 PDF", data=to_pdf(all_pos_df),
                       file_name="Pos_Collection.pdf",
                       mime="application/pdf")
with col141:
    st.download_button("🖼️ PNG", data=to_png(all_pos_df),
                       file_name="Pos_Collection.png",
                       mime="image/png")
    # Display table
st.dataframe(all_pos_df, use_container_width=True)











#***********************************END District by MAIN-SOURCE*********************
# Clean column names
df_selection.columns = df_selection.columns.str.strip()

# Ensure required columns exist
required_columns = {"Amount", "CollectorName", "SourceType"}
if not required_columns.issubset(df_selection.columns):
    st.error(f"❌ Data must contain: {', '.join(required_columns)}.\n\nFound: {df_selection.columns.tolist()}")
else:
    # 🔍 Filter for SourceType == "POS"
    filtered_df = df_selection[df_selection["SourceType"].str.upper() == "POS"]

    # 📊 Group by ItemName, sum Amount, get top 10
    top_collector_df = (
        filtered_df.groupby("CollectorName", as_index=False)["Amount"]
        .sum()
        .sort_values(by="Amount", ascending=False)
        .head(10)
    )

    # Add thousands separator
    top_collector_df["Amount"] = top_collector_df["Amount"].apply(lambda x: f"{x:,.0f}")

    # Add row numbers
    top_collector_df.insert(0, "NO", range(1, len(top_collector_df) + 1))

#Header and SAVE as PDF EXCEL AND PNG ICON
col111, col121, col131, col141 = st.columns([6, 1, 1, 1])
with col111:
    st.subheader("🏆 Top 10 POS Collectors by Amount (All Districts)")
with col121:
    st.download_button("📥 Excel", data=to_excel(top_collector_df),
                       file_name="top_ten_Collector_by_Pos.xlsx",
                       mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
with col131:
    st.download_button("📄 PDF", data=to_pdf(top_collector_df),
                       file_name="top_ten_Collector_by_Pos.pdf",
                       mime="application/pdf")
with col141:
    st.download_button("🖼️ PNG", data=to_png(top_collector_df),
                       file_name="top_ten_Collector_by_Pos.png",
                       mime="image/png")
    # Display table
st.dataframe(top_collector_df, use_container_width=True)












#***********************************END District by MAIN-SOURCE*********************
# Clean column names
df_selection.columns = df_selection.columns.str.strip()

# Ensure required columns exist
required_columns = {"Amount", "CollectorName", "SourceType"}
if not required_columns.issubset(df_selection.columns):
    st.error(f"❌ Data must contain: {', '.join(required_columns)}.\n\nFound: {df_selection.columns.tolist()}")
else:
    # 🔍 Filter for SourceType == "POS"
    filtered_df = df_selection[df_selection["SourceType"].str.upper() == "POS"]

    # 📊 Group by ItemName, sum Amount, get top 10
    all_collector_df = (
        filtered_df.groupby("CollectorName", as_index=False)["Amount"]
        .sum()
        .sort_values(by="Amount", ascending=False)
    )

    # Add thousands separator
    all_collector_df["Amount"] = all_collector_df["Amount"].apply(lambda x: f"{x:,.0f}")

    # Add row numbers
    all_collector_df.insert(0, "NO", range(1, len(all_collector_df) + 1))

#Header and SAVE as PDF EXCEL AND PNG ICON
col111, col121, col131, col141 = st.columns([6, 1, 1, 1])
with col111:
    st.subheader("POS Collectors Sorted by Amount")
with col121:
    st.download_button("📥 Excel", data=to_excel(all_collector_df),
                       file_name="Collector_by_Pos.xlsx",
                       mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
with col131:
    st.download_button("📄 PDF", data=to_pdf(all_collector_df),
                       file_name="Collector_by_Pos.pdf",
                       mime="application/pdf")
with col141:
    st.download_button("🖼️ PNG", data=to_png(all_collector_df),
                       file_name="Collector_by_Pos.png",
                       mime="image/png")
    # Display table
st.dataframe(all_collector_df, use_container_width=True)

















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

    # table_district()



if selected=="Table":
   table()
   
   st.dataframe(df_selection.describe().T,use_container_width=True)
 

 
 
