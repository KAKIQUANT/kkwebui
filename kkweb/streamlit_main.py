import streamlit as st
import yaml
from streamlit_option_menu import option_menu
from pages import
# Function to load YAML configuration
def load_config(language):
    with open(f"cfg/config_{language}.yaml", "r", encoding='utf-8') as f:
        return yaml.safe_load(f)

# Set default language
default_language = "cn"

# Load configuration
config = load_config(default_language)

# Setup page config as the very first Streamlit command
st.set_page_config(
    page_title=config["app"]["page_title"],
    page_icon=config["app"]["page_icon"],
    layout=config["app"]["layout"],
)

sidebar_options = config["sidebar"]["options"]
option_names = [option["name"] for option in sidebar_options]
option_values = [option["value"] for option in sidebar_options]
icons = [option["icon"] for option in sidebar_options]

with st.sidebar:
    choose = option_menu(config["app"]["page_title"], option_names, icons=icons)
