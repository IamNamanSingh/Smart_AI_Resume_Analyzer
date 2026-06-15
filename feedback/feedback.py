import streamlit as st
import sqlite3
from datetime import datetime
import pandas as pd
class FeedbackManager:
    def __init__(self):
        self.db_path = "feedback/feedback.db"
        self.setup_database()

    def setup_database(self):
        """Create feedback table and add columns if they don't exist"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS feedback (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                rating INTEGER,
                usability_score INTEGER,
                feature_satisfaction INTEGER,
                missing_features TEXT,
                improvement_suggestions TEXT,
                user_experience TEXT,
                timestamp DATETIME
            )
        ''')
        
        # Add new columns for simplified feedback if they don't exist
        try:
            c.execute("ALTER TABLE feedback ADD COLUMN name TEXT")
        except sqlite3.OperationalError:
            pass
        try:
            c.execute("ALTER TABLE feedback ADD COLUMN email TEXT")
        except sqlite3.OperationalError:
            pass
        try:
            c.execute("ALTER TABLE feedback ADD COLUMN category TEXT")
        except sqlite3.OperationalError:
            pass
        try:
            c.execute("ALTER TABLE feedback ADD COLUMN feedback_text TEXT")
        except sqlite3.OperationalError:
            pass
            
        conn.commit()
        conn.close()

    def save_feedback(self, feedback_data):
        """Save feedback to database"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''
            INSERT INTO feedback (
                rating, usability_score, feature_satisfaction,
                missing_features, improvement_suggestions,
                user_experience, name, email, category, feedback_text, timestamp
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            feedback_data.get('rating', 5),
            feedback_data.get('usability_score', 5),
            feedback_data.get('feature_satisfaction', 5),
            feedback_data.get('missing_features', ''),
            feedback_data.get('improvement_suggestions', ''),
            feedback_data.get('user_experience', ''),
            feedback_data.get('name', ''),
            feedback_data.get('email', ''),
            feedback_data.get('category', ''),
            feedback_data.get('feedback_text', ''),
            datetime.now()
        ))
        conn.commit()
        conn.close()

    def get_feedback_stats(self):
        """Get feedback statistics"""
        conn = sqlite3.connect(self.db_path)
        df = pd.read_sql_query("SELECT * FROM feedback", conn)
        conn.close()
        
        if df.empty:
            return {
                'avg_rating': 0,
                'avg_usability': 0,
                'avg_satisfaction': 0,
                'total_responses': 0
            }
        
        return {
            'avg_rating': df['rating'].mean(),
            'avg_usability': df['usability_score'].mean(),
            'avg_satisfaction': df['feature_satisfaction'].mean(),
            'total_responses': len(df)
        }

    def render_feedback_form(self):
        """Render the feedback form"""
        if 'feedback_submitted' not in st.session_state:
            st.session_state.feedback_submitted = False

        # Center the feedback form card
        col_left, col_center, col_right = st.columns([1, 2, 1])

        with col_center:
            if st.session_state.feedback_submitted:
                # Success view inside the card
                with st.container():
                    st.markdown("""
                        <div style="text-align: center; padding: 20px 10px;">
                            <div style="font-size: 3.5rem; margin-bottom: 15px;">🎉</div>
                            <h3 style="color: var(--accent); margin-bottom: 10px; font-weight: 600;">Thank You for Your Feedback!</h3>
                            <p style="color: var(--text-secondary); line-height: 1.6; margin-bottom: 25px;">
                                Your thoughts and suggestions help us improve Smart Resume AI. 
                                We review every submission carefully!
                            </p>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    if st.button("Submit Another Response", use_container_width=True):
                        st.session_state.feedback_submitted = False
                        st.rerun()
            else:
                # Form view inside the card
                with st.container():
                    st.markdown("""
                        <div style="margin-bottom: 20px;">
                            <h3 style="margin: 0 0 5px 0; font-weight: 600;">Share Your Thoughts</h3>
                            <p style="margin: 0; font-size: 0.9rem; color: var(--text-secondary);">Help us improve by submitting a quick report or suggestion.</p>
                        </div>
                    """, unsafe_allow_html=True)
                    # Optional name and email fields

                    feedback_text = st.text_area(
                        "Your Feedback",
                        placeholder="Tell us what you liked, disliked, or what we should improve...",
                        height=180
                    )

                    st.markdown('<div style="margin-top: 15px;"></div>', unsafe_allow_html=True)

                    # Submit button
                    if st.button("Submit Feedback", key="submit_feedback", use_container_width=True):
                        if not feedback_text.strip():
                            st.error("Please enter your feedback detail before submitting.")
                        else:
                            try:
                                # Save feedback
                                feedback_data = {
                                    'rating': 5,
                                    'usability_score': 5,
                                    'feature_satisfaction': 5,
                                    'missing_features': '',
                                    'improvement_suggestions': f"Name: {'Anonymous'}\nEmail: {'N/A'}",
                                    'user_experience': feedback_text,
                                    'name': '',
                                    'email': '',
                                    'category': 'General Feedback',
                                    'feedback_text': feedback_text
                                }
                                self.save_feedback(feedback_data)
                                
                                # Set submission state
                                st.session_state.feedback_submitted = True
                                st.balloons()
                                st.rerun()
                                
                            except Exception as e:
                                st.error(f"Error submitting feedback: {str(e)}")
