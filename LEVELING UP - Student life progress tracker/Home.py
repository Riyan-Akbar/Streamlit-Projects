import streamlit as st
import pandas as pd
#from streamlit_navigation_bar import st_navbar

# PAGE TAB TITLE---------------
st.set_page_config(
    page_title="LEVELING UP",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)

# PAGE HEADING / NAME ------------------
st.title(":green[_LEVELING_ _UP_]",text_alignment="center")

# st.set_page_config(initial_sidebar_state="collapsed")

# pages = ["Home", "Library", "Tutorials", "Development", "Download"]
# styles = {
#     "nav": {
#         "background-color": "rgba(0,0,0,0)",
#     },
#     "div": {
#         "max-width": "32rem",
#     },
#     "span": {
#         "border-radius": "0.5rem",
#         "color": "rgb(123, 209, 146)",
#         "margin": "0 0.125rem",
#         "padding": "0.4375rem 0.625rem",
#     },
#     "hover": {
#         "color": "rgba(255, 255, 255, 0.35)",
#     },
# }

# page = st_navbar(pages, styles=styles)
# st.write(page)

# PAGE SIDEBAR ----------------
st.sidebar.header("RIYAN")
# st.page_link("Home.py", label="Home", icon="🏠")
# st.page_link("pages/page_1.py", label="Page 1", icon="1️⃣")
# st.page_link("pages/page_2.py", label="Page 2", icon="2️⃣")
# st.page_link("http://www.google.com", label="Google", icon="🌎")
