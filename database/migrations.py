import sqlite3
import os
import shutil
from core.config import DB_PATH
from core.database import init_database, get_database_connection
from database.schema import *

def run_migrations():
    """Run migrations and combine legacy databases"""
    print("Running database migrations...")
    
    # 1. Initialize tables in the main database
    init_database()
    
    # 2. Check if a legacy feedback database exists and needs to be merged
    legacy_feedback_db = os.path.join("feedback", "feedback.db")
    if os.path.exists(legacy_feedback_db):
        print("Found legacy feedback database. Merging data...")
        try:
            # Connect to legacy database
            legacy_conn = sqlite3.connect(legacy_feedback_db)
            legacy_cursor = legacy_conn.cursor()
            
            # Fetch all feedback
            legacy_cursor.execute("SELECT * FROM feedback")
            columns = [col[0] for col in legacy_cursor.description]
            feedback_rows = legacy_cursor.fetchall()
            legacy_conn.close()
            
            if feedback_rows:
                # Open main database
                main_conn = get_database_connection()
                main_cursor = main_conn.cursor()
                
                # Check column count and names dynamically
                placeholders = ", ".join(["?"] * len(columns))
                column_names = ", ".join(columns)
                
                # Prepare statement
                stmt = f"INSERT OR IGNORE INTO feedback ({column_names}) VALUES ({placeholders})"
                
                # Batch insert
                main_cursor.executemany(stmt, feedback_rows)
                main_conn.commit()
                print(f"Successfully migrated {len(feedback_rows)} feedback records.")
                main_conn.close()
                
            # Create a backup and delete old file
            backup_path = f"{legacy_feedback_db}.bak"
            shutil.move(legacy_feedback_db, backup_path)
            print(f"Legacy database backed up to {backup_path}")
            
        except Exception as e:
            print(f"Error during legacy feedback database migration: {e}")
            
    print("Database migrations finished successfully.")

if __name__ == "__main__":
    run_migrations()
