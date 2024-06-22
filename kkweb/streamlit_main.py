import streamlit as st
from streamlit_option_menu import option_menu
from kkweb.pages.analysis import build_page
from kkweb.pages import create_task
from kkweb.pages.strategies import strategies
import pages.single_factor_analysis as single_factor
import pages.factor_dashboard as page_factor_data
import kkweb.pages.alpha_gpt.alpha_gpt as page_ai_factor
import pages.about_us as page_about_us
import pages.factor_database as page_factor_database
import pages.data_download as page_data_download
import pages.open_vip as page_open_vip
import yaml


# Function to load YAML configuration
def load_config(language):
    with open(f"config_{language}.yaml", "r") as f:
        return yaml.safe_load(f)


# Function to set up Streamlit page config
def setup_page_config(config):
    st.set_page_config(
        page_title=config["app"]["page_title"],
        page_icon=config["app"]["page_icon"],
        layout=config["app"]["layout"],
    )


# Choose language
language = st.sidebar.selectbox("Choose Language", ["en", "cn"])
st.session_state["language"] = language

# Load configuration
config = load_config(language)

# Setup page config
setup_page_config(config)

# Define the sidebar navigation
sidebar_options = config["sidebar"]["options"]
option_names = [option["name"] for option in sidebar_options]
option_values = [option["value"] for option in sidebar_options]
icons = [option["icon"] for option in sidebar_options]

choose = option_menu(config["app"]["page_title"], option_names, icons=icons)

# Main content based on sidebar selection
if choose == "time_series":
    build_page()
elif choose == "create_strategy":
    create_task.build()
elif choose == "strategy_set":
    strategies()
elif choose == "single_factor":
    single_factor.show_single_factor_page()
elif choose == "ai_factor":
    page_ai_factor.show_ai_factor_page()
elif choose == "factor_data":
    page_factor_data.show_factor_data_page()
elif choose == "factor_database":
    page_factor_database.show_factor_database_page()
elif choose == "data_download":
    page_data_download.show_data_download_page()
elif choose == "open_vip":
    page_open_vip.show_open_vip_page()
elif choose == "about_us":
    page_about_us.show_about_us_page()
