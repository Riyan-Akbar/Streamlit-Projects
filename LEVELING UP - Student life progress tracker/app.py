import streamlit as st
import pandas as pd

# PAGE CONFIG ---------------
st.set_page_config(
    page_title="LEVELING UP",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)

# LOAD CUSTOM CSS
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Define all pages
all_pages = [
    st.Page("daily_log.py", title="Forge", icon="🛠️", default=(True)),
    st.Page("task.py", title="Tasks", icon="📝"),
    st.Page("progress.py", title="Progress", icon="📈"),
    st.Page("notes.py", title="Notes", icon="📓"),
    st.Page("portfolio.py", title="Portfolio", icon="👤"),
    st.Page("settings.py", title="Settings", icon="⚙️"),
]

# Initialize navigation but hide the default sidebar menu
pg = st.navigation(all_pages, position="hidden")

# CUSTOM SIDEBAR NAVIGATION
with st.sidebar:
    st.markdown('<div style="text-align: center; margin-bottom: 2rem;">', unsafe_allow_html=True)
    st.markdown('<h2 style="color: #00ff88; margin-bottom: 0;">🚀 LEVEL UP</h2>', unsafe_allow_html=True)
    st.markdown('<p style="color: #8b949e; font-size: 0.8rem;">Student Life Tracker</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="sidebar-title">Main Menu</div>', unsafe_allow_html=True)
    
    # Simple Button Navigation
    for p in all_pages:
        # Check if the current page in the loop is the active one
        is_active = (p.title == pg.title)
        
        # Display button - using primary type for the active page
        if st.button(
            f"{p.icon} {p.title}", 
            key=f"nav_{p.title}", 
            type="primary" if is_active else "secondary",
            use_container_width=True
        ):
            st.switch_page(p)
            
    st.markdown('<div style="position: fixed; bottom: 20px; color: #30363d; font-size: 0.7rem;">v1.0.0</div>', unsafe_allow_html=True)

# PAGE HEADER
st.markdown(f'<h1 class="main-title">{pg.title}</h1>', unsafe_allow_html=True)

# Run the selected page content
pg.run()
