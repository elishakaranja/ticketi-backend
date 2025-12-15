from app import db, app
from sqlalchemy import text

def drop_all_tables():
    with app.app_context():
        # Get database connection
        conn = db.engine.connect()
        
        # Disable foreign key checks temporarily
        conn.execute(text("SET CONSTRAINTS ALL DEFERRED"))
        
        # Drop all tables forcefully
        conn.execute(text("""
            DO $$ DECLARE
                r RECORD;
            BEGIN
                FOR r IN (SELECT tablename FROM pg_tables WHERE schemaname = current_schema()) LOOP
                    EXECUTE 'DROP TABLE IF EXISTS ' || quote_ident(r.tablename) || ' CASCADE';
                END LOOP;
            END $$;
        """))
        
        print("All tables have been dropped successfully!")
        conn.close()

if __name__ == "__main__":
    drop_all_tables() 