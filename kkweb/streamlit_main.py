import streamlit as st
import yaml
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from streamlit_option_menu import option_menu
from streamlit_pages import create_task
from streamlit_pages.strategies import strategies
from streamlit_pages.alpha_gpt import alpha_gpt
from streamlit_pages.page_analysis import build_page
from streamlit_pages import page_create_task
from streamlit_pages.factor_dashboard import dashboard
from streamlit_pages.factor_database import database
from streamlit_pages.strategy_combination import build_strategy
from streamlit_pages.drag_and_drop import drag_and_drop
from streamlit_pages.download_data import download_data
import os
from config import DATA_DIR
from task import task_from_json
from streamlit_pages import single_factor_analysis
from streamlit_pages.settings import settings
from streamlit_pages.python_online import python_online

# Function to load YAML configuration
def load_config(language):
    with open(f"cfg/config_{language}.yaml", "r", encoding='utf-8') as f:
        return yaml.safe_load(f)


# Function to send email
def send_email(subject, message, to_email):
    try:
        sender_email = "your-email@gmail.com"
        sender_password = "your-email-password"

        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = to_email
        msg["Subject"] = subject

        msg.attach(MIMEText(message, "plain"))

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, to_email, msg.as_string())
        server.close()

        st.success("Your message has been sent successfully!")
    except Exception as e:
        st.error(f"Failed to send message. Error: {e}")


# Set default language
default_language = "cn"

# Load configuration
config = load_config(default_language)

# Sidebar construction
sidebar_options = config["sidebar"]["options"]
option_names = [option["name"] for option in sidebar_options]
option_values = [option["value"] for option in sidebar_options]
icons = [option["icon"] for option in sidebar_options]

with st.sidebar:
    choose = option_menu(config["app"]["page_title"], option_names, icons=icons)
    create_task.show_tasks()

if choose == "单因子分析":
    single_factor_analysis.build_page()

elif choose == "因子数据看板":
    dashboard()

elif choose == '时间序列分析':
    build_page()

elif choose == '创建策略向导':
    page_create_task.build()

elif choose == "因子数据库":
    database()

elif choose == "AI因子挖掘助手":
    alpha_gpt.main()

elif choose == "策略集合":
    build_strategy()

elif choose == "开通会员":
    drag_and_drop()

elif choose == "数据下载":
    download_data()

elif choose == "设置":
    settings()

elif choose == "线上编辑":
    python_online()

# Add About and Contact Us sections at the bottom
st.sidebar.title("About")
if st.sidebar.button("About"):
    st.write("""
        ### About Us
        This application is designed to assist users with factor analysis, strategy creation, and more.

        **Address:**
        Somewhere over the rainbow

        **Phone:**
        114514

        For more details, visit our [website](kakiquant.io).
    """)

st.sidebar.title("Contact Us")
if st.sidebar.button("Contact Us"):
    st.write(
        "### Contact Us\nIf you have any questions or feedback, please fill in your contact information below and send it to us.")
    with st.form(key='contact_form'):
        name = st.text_input("Name")
        email = st.text_input("Email")
        subject = st.text_input("Subject")
        message = st.text_area("Message")
        submit_button = st.form_submit_button(label='Send')

    if submit_button:
        email_subject = f"Message from {name}: {subject}"
        email_message = f"From: {name}\nEmail: {email}\n\n{message}"
        send_email(email_subject, email_message, "zz324@duke.edu")
