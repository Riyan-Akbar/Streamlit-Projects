import streamlit as st
from database.database import log_study_session, get_connection, get_subjects, add_subject
from datetime import datetime

# PAGE CONTENT
st.markdown('<p style="color: #8b949e; text-align: center; margin-top: -1rem;">"The only way to do great work is to love what you do."</p>', unsafe_allow_html=True)

# Layout Columns
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.markdown("### 🛠️ Craft a Session")
    
    # Dynamic Subject List
    subjects = get_subjects()
    
    with st.expander("Session Details", expanded=True):
        subject = st.selectbox("Select Project / Subject", subjects)
        
        # Subject Management Popover
        with st.popover("⚙️ Manage Subjects"):
            # Add Section
            st.markdown("##### Add New")
            new_sub = st.text_input("New Subject Name", key="new_sub_input")
            if st.button("Add to Database", use_container_width=True):
                if new_sub:
                    from database.database import add_subject
                    if add_subject(new_sub):
                        st.success(f"Added {new_sub}!")
                        st.rerun()
                    else:
                        st.error("Subject already exists.")
            
            st.divider()
            
            # Delete Section
            st.markdown("##### Remove")
            sub_to_del = st.selectbox("Choose to delete", subjects, key="del_sub_select")
            if st.button("🗑️ Delete Subject", use_container_width=True, type="secondary"):
                from database.database import delete_subject
                if delete_subject(sub_to_del):
                    st.warning(f"Deleted {sub_to_del}")
                    st.rerun()
        
        topic = st.text_input("What specific topic did you work on?", placeholder="e.g. SQL Joins, UI Design...")
        
        c1, c2 = st.columns(2)
        with c1:
            hours = st.number_input("Hours", min_value=0.1, max_value=24.0, value=1.0, step=0.5)
        with c2:
            focus = st.slider("Focus Score", 1, 10, 7)
            
        difficulty = st.select_slider("Difficulty Level", options=[1, 2, 3, 4, 5], value=3)
        
        col_rev, col_note = st.columns(2)
        with col_rev:
            revision = st.toggle("Revision Done?")
        with col_note:
            notes = st.toggle("Notes Taken?")

    if st.button("🔥 FORGE IT!", use_container_width=True, type="primary"):
        if topic:
            session_data = {
                "subject": subject,
                "topic": topic,
                "hours": hours,
                "focus": focus,
                "difficulty": difficulty,
                "revision": "Yes" if revision else "No",
                "notes": "Yes" if notes else "No"
            }
            if log_study_session(session_data):
                st.balloons()
                st.success(f"Successfully Forged! +{int(hours * 10)} XP earned in {subject}")
                st.rerun() # Refresh to show in history
        else:
            st.warning("Please enter a topic name to forge the session.")

with col2:
    st.markdown("### 📜 Today's Activity")
    
    # Fetch today's logs from DB
    today_str = datetime.now().strftime("%Y-%m-%d")
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM study_log WHERE date = ? ORDER BY id DESC", (today_str,))
    logs = cursor.fetchall()
    conn.close()
    
    if logs:
        for log in logs:
            with st.container():
                st.markdown(f"""
                <div style="background: rgba(255,255,255,0.05); padding: 1rem; border-radius: 10px; border-left: 4px solid #00ff88; margin-bottom: 10px;">
                    <div style="display: flex; justify-content: space-between;">
                        <span style="font-weight: bold; color: #00ff88;">{log['subject_name']}</span>
                        <span style="font-size: 0.8rem; color: #8b949e;">{log['study_hours_total']} hrs</span>
                    </div>
                    <div style="font-size: 0.9rem; margin-top: 5px;">{log['topic_name']}</div>
                    <div style="font-size: 0.7rem; color: #444; margin-top: 5px;">Focus: {log['focus_score']}/10 | Diff: {log['difficulty_level']}/5</div>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info("No work forged yet today. Get to the anvil! 🔨")

# Stats footer
st.divider()
st.markdown(f'<div style="text-align: center; color: #30363d;">Session ID: {datetime.now().strftime("%H%M%S")} | Status: Online</div>', unsafe_allow_html=True)

