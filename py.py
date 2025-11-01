import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title="Walmart Sales Dashboard", layout="wide")
st.title("📊 Walmart Sales Revenue & Profit Dashboard")

# قراءة الملف مباشرة
df = pd.read_csv("Walmart_Sales.csv")

st.subheader("Raw Data")
st.dataframe(df.head(1000))  # عرض أول 1000 صف فقط لتسريع الأداء

# تنظيف البيانات
df['Revenue'] = pd.to_numeric(df['Revenue'], errors='coerce')
df['Expense'] = pd.to_numeric(df['Expense'], errors='coerce')

# لو فيه عمود للتاريخ اسمه مختلف، عدله هنا:
# df['Date'] = pd.to_datetime(df['DateColumnName'], errors='coerce')
df['Date'] = pd.to_datetime(df['Date'], errors='coerce')  # تأكد العمود موجود باسم Date

df = df.dropna(subset=['Date','Revenue','Expense'])

# حساب الأرباح
df['Profit'] = df['Revenue'] - df['Expense']

# عرض ملخص شامل
st.subheader("Summary")
total_revenue = df['Revenue'].sum()
total_expense = df['Expense'].sum()
total_profit = df['Profit'].sum()
st.write(f"**Total Revenue:** {total_revenue}")
st.write(f"**Total Expense:** {total_expense}")
st.write(f"**Total Profit:** {total_profit}")

# اختيار طريقة التجميع
view_option = st.radio("View Data By:", ("Daily","Monthly"))

if view_option == "Daily":
    summary = df.groupby('Date')[['Revenue','Expense','Profit']].sum()
else:  # Monthly
    summary = df.groupby(df['Date'].dt.to_period('M'))[['Revenue','Expense','Profit']].sum()

st.subheader(f"{view_option} Summary")
st.dataframe(summary)

# رسم بياني
st.subheader(f"{view_option} Revenue, Expense & Profit")
fig, ax = plt.subplots(figsize=(12,6))
summary.plot(kind='bar', ax=ax)
ax.set_ylabel("Amount")
ax.set_title(f"{view_option} Revenue, Expense & Profit")
st.pyplot(fig)
