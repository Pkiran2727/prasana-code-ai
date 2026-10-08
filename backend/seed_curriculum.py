import os
import sys
import psycopg2
from psycopg2.extras import DictCursor
import json
import uuid

# Import the hardcoded data
try:
    from curriculum_data import JOURNEYS_DATA
except ImportError:
    print("Could not import JOURNEYS_DATA from curriculum_data.py")
    sys.exit(1)

DB_HOST = os.environ.get("DB_HOST", "localhost")
DB_PORT = os.environ.get("DB_PORT", "5432")
DB_USER = os.environ.get("DB_USER", "prasana_user")
DB_PASS = os.environ.get("DB_PASS", "PrasanaSecureDBPassword2026")
DB_NAME = os.environ.get("DB_NAME", "prasana_code_ai")

def get_db_connection():
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASS,
            dbname=DB_NAME
        )
        return conn
    except Exception as e:
        print(f"Failed to connect to DB: {e}")
        sys.exit(1)

def run_migrations(conn):
    print("Running schema migrations...")
    try:
        with open("database_schema.sql", "r") as f:
            schema_sql = f.read()
        with conn.cursor() as cur:
            cur.execute(schema_sql)
        conn.commit()
        print("Schema created successfully.")
    except Exception as e:
        print(f"Migration error: {e}")
        conn.rollback()
        sys.exit(1)

def slugify(text):
    return text.lower().replace(" ", "-").replace("&", "and").replace(",", "").replace(".", "").strip()

def seed_data(conn, dry_run=False):
    print(f"Starting seed process (Dry Run: {dry_run})...")
    
    cat_count = 0
    course_count = 0
    module_count = 0
    lesson_count = 0
    
    try:
        with conn.cursor(cursor_factory=DictCursor) as cur:
            for cat_index, journey in enumerate(JOURNEYS_DATA):
                # 1. UPSERT Category
                cat_slug = slugify(journey.get("category", "Uncategorized"))
                cat_title = journey.get("category", "Uncategorized")
                
                cur.execute("""
                    INSERT INTO categories (slug, title, sort_order) 
                    VALUES (%s, %s, %s)
                    ON CONFLICT (slug) DO UPDATE SET title = EXCLUDED.title
                    RETURNING id;
                """, (cat_slug, cat_title, cat_index))
                cat_id = cur.fetchone()['id']
                cat_count += 1
                
                # 2. UPSERT Course
                course_slug = journey["id"]
                course_title = journey["title"]
                course_desc = journey.get("description", "")
                
                cur.execute("""
                    INSERT INTO courses (category_id, slug, title, description, difficulty, is_premium, sort_order)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (slug) DO UPDATE SET 
                        title = EXCLUDED.title,
                        description = EXCLUDED.description
                    RETURNING id;
                """, (cat_id, course_slug, course_title, course_desc, 'beginner', False, cat_index))
                course_id = cur.fetchone()['id']
                course_count += 1
                
                # 3. Modules (Courses inside Journey)
                for mod_index, module in enumerate(journey.get("courses", [])):
                    mod_slug = module["id"]
                    mod_title = module["title"]
                    
                    cur.execute("""
                        INSERT INTO modules (course_id, slug, title, sort_order)
                        VALUES (%s, %s, %s, %s)
                        ON CONFLICT (course_id, slug) DO UPDATE SET title = EXCLUDED.title
                        RETURNING id;
                    """, (course_id, mod_slug, mod_title, mod_index))
                    mod_id = cur.fetchone()['id']
                    module_count += 1
                    
                    # 4. Lessons / Challenges
                    for les_index, lesson in enumerate(module.get("lessons", [])):
                        les_slug = lesson["id"]
                        les_title = lesson["title"]
                        
                        # Upsert lesson
                        cur.execute("""
                            INSERT INTO lessons (module_id, slug, title, type, xp_reward, sort_order)
                            VALUES (%s, %s, %s, 'challenge', 10, %s)
                            ON CONFLICT (module_id, slug) DO UPDATE SET title = EXCLUDED.title
                            RETURNING id;
                        """, (mod_id, les_slug, les_title, les_index))
                        lesson_id = cur.fetchone()['id']
                        lesson_count += 1
                        
                        instructions = lesson.get("instructions", "Complete the challenge.")
                        starter_code = lesson.get("starterCode", "")
                        
                        # Upsert Challenge (1:1 with lesson)
                        cur.execute("""
                            INSERT INTO challenges (lesson_id, instructions_md, language, starter_code)
                            VALUES (%s, %s, 'python', %s)
                            ON CONFLICT (lesson_id) DO UPDATE SET 
                                instructions_md = EXCLUDED.instructions_md,
                                starter_code = EXCLUDED.starter_code;
                        """, (lesson_id, instructions, starter_code))
                        
                        # Insert Hint
                        hint_text = lesson.get("hint")
                        if hint_text:
                            cur.execute("""
                                INSERT INTO challenge_hints (lesson_id, level, content)
                                VALUES (%s, 1, %s)
                                ON CONFLICT (lesson_id, level) DO UPDATE SET content = EXCLUDED.content;
                            """, (lesson_id, hint_text))
                            
                        # Insert Test Case
                        expected_output = lesson.get("expectedOutput")
                        if expected_output:
                            # Basic dummy insert for now if we don't have inputs
                            cur.execute("""
                                DELETE FROM test_cases WHERE lesson_id = %s;
                            """, (lesson_id,))
                            
                            cur.execute("""
                                INSERT INTO test_cases (lesson_id, input_data, expected_output, is_hidden, sort_order)
                                VALUES (%s, '', %s, FALSE, 0);
                            """, (lesson_id, expected_output))
                            
        if dry_run:
            conn.rollback()
            print("Dry run completed. Transaction rolled back.")
        else:
            conn.commit()
            print("Seed completed and committed.")
            
        print(f"Categories: {cat_count}")
        print(f"Courses: {course_count}")
        print(f"Modules: {module_count}")
        print(f"Lessons/Challenges: {lesson_count}")
        
    except Exception as e:
        print(f"Seed error: {e}")
        conn.rollback()
        sys.exit(1)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true", help="Run seed without saving")
    args = parser.parse_args()
    
    conn = get_db_connection()
    if not args.dry_run:
        run_migrations(conn)
    seed_data(conn, dry_run=args.dry_run)
    conn.close()
