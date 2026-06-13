import pytest
import os
import tempfile
import shutil

# Create a module-level temporary directory and set the environment variable
# BEFORE any test module imports core.config or core.database.
TEMP_DIR = tempfile.mkdtemp()
TEST_DB_FILE = os.path.join(TEMP_DIR, "test_resume_data.db")
os.environ["DB_PATH"] = TEST_DB_FILE

from core.database import init_database

# Initialize the schema inside the test database
init_database()

@pytest.fixture(scope="session", autouse=True)
def test_db_session():
    """Session-scoped fixture to manage the lifetime of the temporary test database directory"""
    yield TEST_DB_FILE
    
    # Cleanup temporary directory at the end of the session
    try:
        shutil.rmtree(TEMP_DIR)
    except Exception as e:
        print(f"Error cleaning up test DB directory: {e}")

@pytest.fixture(autouse=True)
def clean_database():
    """Function-scoped fixture to clear all table records before running each test case"""
    from core.database import get_database_connection
    conn = get_database_connection()
    cursor = conn.cursor()
    
    # Disable foreign key constraints temporarily to clear tables safely
    cursor.execute("PRAGMA foreign_keys = OFF;")
    
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")
    tables = [row[0] for row in cursor.fetchall()]
    
    for table in tables:
        cursor.execute(f"DELETE FROM {table};")
        
    cursor.execute("PRAGMA foreign_keys = ON;")
    conn.commit()
    conn.close()
