# db.py
import psycopg2
from psycopg2 import extras

db_host = "localhost"
db_name = "ocr"
db_user = "postgres"
db_password = "Welc0me#123"

# Insert Query
def insert_into_table(original_filename, file_size, upload_timestamp, document_type, structured_data) -> str:
    conn = None
    try:
        conn = psycopg2.connect(host=db_host, database=db_name, user=db_user, password=db_password)
        cur = conn.cursor()

        # Execute a query to create a table if it doesn't exist
        cur.execute("""
            CREATE TABLE IF NOT EXISTS Documents (
                document_id SMALLSERIAL PRIMARY KEY,
                original_filename VARCHAR(255) NOT NULL,
                storage_path VARCHAR(255) NOT NULL,
                upload_timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                ocr_status VARCHAR(20) DEFAULT 'pending',
                file_size BIGINT,
                document_type VARCHAR(50),
                structured_data JSONB,
                error_message TEXT
            )
        """)
        conn.commit()
        print("Document table created or already exists.")

        # Insert a new document
        storage_path = "local machine"
        cur.execute("""
            INSERT INTO Documents (original_filename, upload_timestamp, file_size, storage_path, document_type, structured_data)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (original_filename, upload_timestamp, file_size, storage_path, document_type, extras.Json(structured_data)))
        conn.commit()
        print(f"Document '{original_filename}' OCR data uploaded.")

    except psycopg2.Error as e:
        print(f"Database error: {e}")
        if conn:
            conn.rollback()  # Rollback any uncommitted changes

    finally:
        if conn:
            cur.close()
            conn.close()
            print("Database connection closed.")


# Select Query
def fetch_from_table() -> str:
    conn = None
    try:
        conn = psycopg2.connect(host=db_host, database=db_name, user=db_user, password=db_password)
        cur = conn.cursor()

        # Retrieve all documents
        cur.execute("SELECT document_id, original_filename, storage_path, file_size, document_type, structured_data FROM Documents")
        rows = cur.fetchall()
        
        column_names = [desc[0] for desc in cur.description]

        data_with_keys = []
        for row in rows:
            row_dict = {}
            for i, col_name in enumerate(column_names):
                row_dict[col_name] = row[i]
            data_with_keys.append(row_dict)
        
        return data_with_keys

    except psycopg2.Error as e:
        print(f"Database error: {e}")
        if conn:
            conn.rollback()  # Rollback any uncommitted changes

    finally:
        if conn:
            cur.close()
            conn.close()
            print("Database connection closed.")

