import os
import sys
import psycopg2
from psycopg2.extras import DictCursor
import json
import uuid

try:
    from backend.curriculum_data import JOURNEYS_DATA
except ImportError:
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
        schema_path = "backend/database_schema.sql" if os.path.exists("backend/database_schema.sql") else ("database_schema.sql" if os.path.exists("database_schema.sql") else os.path.join(os.path.dirname(__file__), "database_schema.sql"))
        with open(schema_path, "r") as f:
            schema_sql = f.read()
        with conn.cursor() as cur:
            cur.execute(schema_sql)
        conn.commit()
        print("Schema created successfully.")
    except Exception as e:
        print(f"Migration notice: {e}")
        conn.rollback()

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
                        lesson_lang = lesson.get("language", "python")
                        
                        # Upsert Challenge (1:1 with lesson)
                        cur.execute("""
                            INSERT INTO challenges (lesson_id, instructions_md, language, starter_code)
                            VALUES (%s, %s, %s, %s)
                            ON CONFLICT (lesson_id) DO UPDATE SET 
                                instructions_md = EXCLUDED.instructions_md,
                                language = EXCLUDED.language,
                                starter_code = EXCLUDED.starter_code;
                        """, (lesson_id, instructions, lesson_lang, starter_code))
                        
                        # Insert Hints
                        hints = lesson.get("hints", [])
                        if not hints and lesson.get("hint"):
                            hints = [lesson.get("hint")]
                        for h_idx, h_text in enumerate(hints):
                            cur.execute("""
                                INSERT INTO challenge_hints (lesson_id, level, content)
                                VALUES (%s, %s, %s)
                                ON CONFLICT (lesson_id, level) DO UPDATE SET content = EXCLUDED.content;
                            """, (lesson_id, h_idx + 1, h_text))
                            
                        # Insert Test Cases
                        test_cases = lesson.get("testCases") or []
                        if test_cases:
                            cur.execute("DELETE FROM test_cases WHERE lesson_id = %s;", (lesson_id,))
                            for tc_idx, tc in enumerate(test_cases):
                                cur.execute("""
                                    INSERT INTO test_cases (lesson_id, input_data, expected_output, is_hidden, sort_order)
                                    VALUES (%s, %s, %s, FALSE, %s);
                                """, (lesson_id, tc.get("input", ""), tc.get("expected", ""), tc_idx))
                        elif lesson.get("expectedOutput"):
                            cur.execute("DELETE FROM test_cases WHERE lesson_id = %s;", (lesson_id,))
                            cur.execute("""
                                INSERT INTO test_cases (lesson_id, input_data, expected_output, is_hidden, sort_order)
                                VALUES (%s, '', %s, FALSE, 0);
                            """, (lesson_id, lesson.get("expectedOutput")))

                        # Insert Bilingual Content
                        if lesson.get("theory_en"):
                            cur.execute("""
                                INSERT INTO lesson_content (lesson_id, lang, title, body_md)
                                VALUES (%s, 'en', %s, %s)
                                ON CONFLICT (lesson_id, lang) DO UPDATE SET title = EXCLUDED.title, body_md = EXCLUDED.body_md;
                            """, (lesson_id, lesson.get("title", ""), lesson.get("theory_en", "")))
                        if lesson.get("theory_te"):
                            cur.execute("""
                                INSERT INTO lesson_content (lesson_id, lang, title, body_md)
                                VALUES (%s, 'te', %s, %s)
                                ON CONFLICT (lesson_id, lang) DO UPDATE SET title = EXCLUDED.title, body_md = EXCLUDED.body_md;
                            """, (lesson_id, lesson.get("title_te", lesson.get("title", "")), lesson.get("theory_te", "")))
                            
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
