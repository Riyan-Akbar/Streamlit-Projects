import sqlite3
import os
from datetime import datetime

# DATABASE PATH
DB_PATH = os.path.join(os.path.dirname(__file__), "tracker.db")

def get_connection():
    """Returns a connection to the SQLite database."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # This allows accessing columns by name
    return conn

def init_db():
    """Initializes the database by creating all 11 tables from the blueprints."""
    conn = get_connection()
    cursor = conn.cursor()

    # 1. DAILY CORE (The Master Table)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS daily_core (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date DATE UNIQUE,
            timestamp DATETIME,
            week_number INTEGER,
            month INTEGER,
            year INTEGER,
            day_of_week TEXT
        )
    """)

    # 2. STUDY LOG
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS study_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date DATE,
            study_hours_total REAL,
            study_sessions_count INTEGER,
            focus_score INTEGER,
            subject_name TEXT,
            topic_name TEXT,
            difficulty_level INTEGER,
            revision_done TEXT,
            notes_taken TEXT,
            active_recall_used TEXT,
            pomodoro_cycles INTEGER,
            distraction_minutes INTEGER,
            deep_work_minutes INTEGER,
            exam_type TEXT,
            syllabus_completion_percentage REAL,
            confidence_level INTEGER,
            mistakes_count INTEGER,
            time_per_question REAL,
            FOREIGN KEY (date) REFERENCES daily_core (date)
        )
    """)

    # 3. HEALTH LOG
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS health_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date DATE,
            sleep_hours REAL,
            sleep_quality INTEGER,
            wake_time TEXT,
            bed_time TEXT,
            exercise_type TEXT,
            exercise_duration INTEGER,
            steps INTEGER,
            calories_burned INTEGER,
            water_intake_liters REAL,
            posture_score INTEGER,
            screen_time_hours REAL,
            eye_strain INTEGER,
            FOREIGN KEY (date) REFERENCES daily_core (date)
        )
    """)

    # 4. SKILLS
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS skills (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date DATE,
            skill_name TEXT,
            skill_category TEXT,
            learning_hours REAL,
            practice_problems_solved INTEGER,
            projects_worked_on INTEGER,
            github_commits INTEGER,
            leetcode_solved INTEGER,
            difficulty_breakdown TEXT,
            concept_clarity INTEGER,
            real_world_application_done TEXT,
            interview_readiness_score INTEGER,
            resume_relevance_score INTEGER,
            industry_alignment TEXT,
            FOREIGN KEY (date) REFERENCES daily_core (date)
        )
    """)

    # 5. REFLECTIONS
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reflections (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date DATE,
            daily_win TEXT,
            daily_loss TEXT,
            lesson_learned TEXT,
            what_to_improve_tomorrow TEXT,
            self_rating_today INTEGER,
            future_self_message TEXT,
            regret_level INTEGER,
            pride_level INTEGER,
            FOREIGN KEY (date) REFERENCES daily_core (date)
        )
    """)

    # 6. MENTAL HEALTH
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS mental_health (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date DATE,
            mood_score INTEGER,
            stress_level INTEGER,
            anxiety_level INTEGER,
            motivation_level INTEGER,
            burnout_indicator TEXT,
            gratitude_entry TEXT,
            journal_entry TEXT,
            self_talk_quality TEXT,
            FOREIGN KEY (date) REFERENCES daily_core (date)
        )
    """)

    # 7. DISCIPLINE & HABITS
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS discipline (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date DATE,
            habit_name TEXT,
            habit_completed TEXT,
            habit_streak INTEGER,
            missed_habits_count INTEGER,
            discipline_score INTEGER,
            procrastination_minutes INTEGER,
            dopamine_triggers_used TEXT,
            morning_routine_completed TEXT,
            evening_review_completed TEXT,
            FOREIGN KEY (date) REFERENCES daily_core (date)
        )
    """)

    # 8. PRODUCTIVITY
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS productivity (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date DATE,
            total_awake_hours REAL,
            productive_hours REAL,
            wasted_time_hours REAL,
            task_completion_rate REAL,
            planned_vs_actual_ratio REAL,
            context_switches INTEGER,
            focus_blocks_completed INTEGER,
            energy_level_morning INTEGER,
            energy_level_evening INTEGER,
            FOREIGN KEY (date) REFERENCES daily_core (date)
        )
    """)

    # 9. SOCIAL
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS social (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date DATE,
            social_interactions_count INTEGER,
            meaningful_conversations INTEGER,
            networking_effort TEXT,
            mentor_interaction TEXT,
            help_given_to_others TEXT,
            help_received TEXT,
            confidence_in_social_settings INTEGER,
            FOREIGN KEY (date) REFERENCES daily_core (date)
        )
    """)

    # 10. FINANCE
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS finance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date DATE,
            money_spent_today REAL,
            money_invested_learning REAL,
            subscriptions_used TEXT,
            roi_score REAL,
            time_cost_vs_value REAL,
            FOREIGN KEY (date) REFERENCES daily_core (date)
        )
    """)

    # 11. AI FIELDS (Future Proofing)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ai_metrics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date DATE,
            predicted_productivity REAL,
            predicted_burnout_risk REAL,
            recommended_study_hours REAL,
            recommended_sleep_hours REAL,
            trend_deviation_score REAL,
            anomaly_detected TEXT,
            FOREIGN KEY (date) REFERENCES daily_core (date)
        )
    """)

    # 12. SUBJECTS LIST
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS subjects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE
        )
    """)

    # Populate default subjects if table is empty
    cursor.execute("SELECT COUNT(*) FROM subjects")
    if cursor.fetchone()[0] == 0:
        default_subjects = [
            "DBMS", "Image Processing", "ML / Pattern Recognition", 
            "Computer Networks", "Web Dev", "Python Skills", 
            "Research Methodology", "Human Resource Development", "Other"
        ]
        cursor.executemany("INSERT INTO subjects (name) VALUES (?)", [(s,) for s in default_subjects])

    conn.commit()
    conn.close()
    print("Leveling Up Database Initialized Successfully!")

# --- HELPER FUNCTIONS FOR APP ---

def add_daily_core():
    """Ensures today's entry exists in daily_core and returns the date string."""
    today = datetime.now().date()
    today_str = today.strftime("%Y-%m-%d")
    
    conn = get_connection()
    cursor = conn.cursor()
    
    # Check if today exists
    cursor.execute("SELECT date FROM daily_core WHERE date = ?", (today_str,))
    if not cursor.fetchone():
        now = datetime.now()
        cursor.execute("""
            INSERT INTO daily_core (date, timestamp, week_number, month, year, day_of_week)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            today_str, 
            now.strftime("%Y-%m-%d %H:%M:%S"),
            now.isocalendar()[1],
            now.month,
            now.year,
            now.strftime("%A")
        ))
        conn.commit()
    
    conn.close()
    return today_str

def log_study_session(data):
    """Saves a study session to the database."""
    date_str = add_daily_core()  # Ensure today exists first
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO study_log (
            date, subject_name, topic_name, study_hours_total, 
            focus_score, difficulty_level, revision_done, notes_taken
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        date_str, data['subject'], data['topic'], data['hours'],
        data['focus'], data['difficulty'], data['revision'], data['notes']
    ))
    
    conn.commit()
    conn.close()
    return True

def get_subjects():
    """Returns a list of all subjects from the database."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM subjects ORDER BY name ASC")
    subjects = [row['name'] for row in cursor.fetchall()]
    conn.close()
    return subjects

def add_subject(name):
    """Adds a new subject to the database."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO subjects (name) VALUES (?)", (name,))
        conn.commit()
        success = True
    except sqlite3.IntegrityError:
        success = False
    conn.close()
    return success

def delete_subject(name):
    """Deletes a subject from the database."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM subjects WHERE name = ?", (name,))
    conn.commit()
    conn.close()
    return True

if __name__ == "__main__":
    init_db()
