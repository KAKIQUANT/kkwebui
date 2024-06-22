import streamlit as st
import yaml
# Import page functions
from streamlit_pages.analysis import build_page as time_series_page
from streamlit_pages import create_task
from streamlit_pages.strategies import strategies
import streamlit_pages.single_factor_analysis as single_factor
import streamlit_pages.factor_dashboard as factor_data
import kkweb.pages.alpha_gpt.alpha_gpt as ai_factor
import streamlit_pages.about_us as about_us
import streamlit_pages.factor_database as factor_database
import streamlit_pages.data_download as data_download
import streamlit_pages.open_vip as open_vip


# Function to load YAML configuration
def load_config(language):
    with open(f"cfg/config_{language}.yaml", "r") as f:
        return yaml.safe_load(f)


# # Function to set up Streamlit page config
# def setup_config(config):
#     st.set_page_config(
#         page_title=config["app"]["page_title"],
#         page_icon=config["app"]["page_icon"],
#         layout=config["app"]["layout"],
#     )


# Choose language
language = st.sidebar.selectbox("Choose Language", ["en", "cn"])
st.session_state["language"] = language

# Load configuration
config = load_config(language)

# Setup page config
# setup_config(config)


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
        ai_factor,
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
