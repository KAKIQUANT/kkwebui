import streamlit as st
import yaml
# Import page functions
from pages.analysis import build_page as time_series_page
from pages import create_task
from pages.strategies import strategies
import pages.single_factor_analysis as single_factor
import pages.factor_dashboard as factor_data
import kkweb.pages.alpha_gpt.alpha_gpt as ai_factor
import pages.about_us as about_us
import pages.factor_database as factor_database
import pages.data_download as data_download
import pages.open_vip as open_vip


# Function to load YAML configuration
def load_config(language):
    with open(f"config_{language}.yaml", "r") as f:
        return yaml.safe_load(f)


# Function to set up Streamlit page config
def setup_config(config):
    st.set_config(
        title=config["app"]["title"],
        icon=config["app"]["icon"],
        layout=config["app"]["layout"],
    )


# Choose language
language = st.sidebar.selectbox("Choose Language", ["en", "cn"])
st.session_state["language"] = language

# Load configuration
config = load_config(language)

# Setup page config
setup_config(config)


# Define pages using st.Page
pages = [
    st.Page(time_series_page, title=config["sidebar"]["options"][6]["name"]),
    st.Page(create_task.build, title=config["sidebar"]["options"][4]["name"]),
    st.Page(strategies, title=config["sidebar"]["options"][5]["name"]),
    st.Page(
        single_factor.show_single_factor_page,
        title=config["sidebar"]["options"][2]["name"],
    ),
    st.Page(
        ai_factor.show_ai_factor_page,
        title=config["sidebar"]["options"][1]["name"],
    ),
    st.Page(
        factor_data.show_factor_data_page,
        title=config["sidebar"]["options"][0]["name"],
    ),
    st.Page(
        factor_database.show_factor_database_page,
        title=config["sidebar"]["options"][3]["name"],
    ),
    st.Page(
        data_download.show_data_download_page,
        title=config["sidebar"]["options"][7]["name"],
    ),
    st.Page(
        open_vip.show_open_vip_page, title=config["sidebar"]["options"][8]["name"]
    ),
    st.Page(
        about_us.show_about_us_page, title=config["sidebar"]["options"][9]["name"]
    ),
]

# Define navigation
pg = st.navigation(pages)
pg.run()
