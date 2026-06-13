import sqlite3
from datetime import datetime
from core.database import get_database_connection

class FeedbackService:
    def __init__(self):
        pass

    def save_feedback(self, feedback_data):
        """Save user feedback to unified SQLite database"""
        conn = get_database_connection()
        c = conn.cursor()
        try:
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
            return True
        except Exception as e:
            print(f"Error saving feedback: {e}")
            conn.rollback()
            return False
        finally:
            conn.close()
            
    def get_feedback_stats(self):
        """Get statistics about user feedback submissions"""
        conn = get_database_connection()
        c = conn.cursor()
        try:
            c.execute("SELECT COUNT(*) FROM feedback")
            total = c.fetchone()[0]
            
            c.execute("SELECT AVG(rating) FROM feedback")
            avg_rating = c.fetchone()[0] or 0.0
            
            c.execute("SELECT category, COUNT(*) as count FROM feedback GROUP BY category")
            categories = [{"category": row[0], "count": row[1]} for row in c.fetchall()]
            
            return {
                'total_responses': total,
                'avg_rating': round(avg_rating, 2),
                'categories': categories
            }
        except Exception as e:
            print(f"Error compiling feedback stats: {e}")
            return {
                'total_responses': 0,
                'avg_rating': 0.0,
                'categories': []
            }
        finally:
            conn.close()
