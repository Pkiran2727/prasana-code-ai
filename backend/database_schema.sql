DO $$ BEGIN
    CREATE TYPE lesson_type AS ENUM ('lesson', 'challenge');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

DO $$ BEGIN
    CREATE TYPE progress_status AS ENUM ('not_started', 'in_progress', 'completed');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

CREATE TABLE IF NOT EXISTS categories (
  id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  slug        TEXT UNIQUE NOT NULL,
  title       TEXT NOT NULL,
  description TEXT,
  sort_order  INT NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS courses (
  id           UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  category_id  UUID NOT NULL REFERENCES categories(id) ON DELETE CASCADE,
  slug         TEXT UNIQUE NOT NULL,
  title        TEXT NOT NULL,
  description  TEXT,
  difficulty   TEXT CHECK (difficulty IN ('beginner','intermediate','advanced')),
  is_premium   BOOLEAN NOT NULL DEFAULT FALSE,
  is_published BOOLEAN NOT NULL DEFAULT TRUE,
  sort_order   INT NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS modules (
  id         UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  course_id  UUID NOT NULL REFERENCES courses(id) ON DELETE CASCADE,
  slug       TEXT NOT NULL,
  title      TEXT NOT NULL,
  is_premium BOOLEAN,              -- NULL = inherit from course
  sort_order INT NOT NULL DEFAULT 0,
  UNIQUE (course_id, slug)
);

CREATE TABLE IF NOT EXISTS lessons (
  id           UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  module_id    UUID NOT NULL REFERENCES modules(id) ON DELETE CASCADE,
  slug         TEXT NOT NULL,
  title        TEXT NOT NULL,
  type         lesson_type NOT NULL,
  content_md   TEXT,               -- theory / explanation
  xp_reward    INT NOT NULL DEFAULT 10,
  is_premium   BOOLEAN,            -- NULL = inherit from module
  is_published BOOLEAN NOT NULL DEFAULT TRUE,
  sort_order   INT NOT NULL DEFAULT 0,
  UNIQUE (module_id, slug)
);

CREATE TABLE IF NOT EXISTS challenges (          -- 1:1 with lessons (type='challenge')
  lesson_id       UUID PRIMARY KEY REFERENCES lessons(id) ON DELETE CASCADE,
  instructions_md TEXT NOT NULL,
  language        TEXT NOT NULL DEFAULT 'python',
  starter_code    TEXT NOT NULL DEFAULT '',
  solution_code   TEXT,            -- server-only
  time_limit_ms   INT NOT NULL DEFAULT 3000,
  memory_limit_mb INT NOT NULL DEFAULT 128
);

CREATE TABLE IF NOT EXISTS challenge_hints (
  id        UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  lesson_id UUID NOT NULL REFERENCES challenges(lesson_id) ON DELETE CASCADE,
  level     INT NOT NULL,          -- 1 = చిన్న hint, 2, 3 = దాదాపు answer
  content   TEXT NOT NULL,
  UNIQUE (lesson_id, level)
);

CREATE TABLE IF NOT EXISTS test_cases (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  lesson_id       UUID NOT NULL REFERENCES challenges(lesson_id) ON DELETE CASCADE,
  input_data      TEXT NOT NULL DEFAULT '',
  expected_output TEXT NOT NULL,
  is_hidden       BOOLEAN NOT NULL DEFAULT FALSE,
  sort_order      INT NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS user_progress (
  user_id         UUID NOT NULL,   -- user_profiles.id / auth.users.id
  lesson_id       UUID NOT NULL REFERENCES lessons(id) ON DELETE CASCADE,
  status          progress_status NOT NULL DEFAULT 'in_progress',
  attempts        INT NOT NULL DEFAULT 0,
  xp_earned       INT NOT NULL DEFAULT 0,   -- మొదటిసారి pass అయినప్పుడే set
  last_code       TEXT,                     -- ఎక్కడ ఆగాడో అక్కడి నుండి resume
  first_started_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  completed_at    TIMESTAMPTZ,
  updated_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
  PRIMARY KEY (user_id, lesson_id)
);

CREATE TABLE IF NOT EXISTS submissions (          -- history / analytics / anti-abuse
  id           UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id      UUID NOT NULL,
  lesson_id    UUID NOT NULL REFERENCES lessons(id) ON DELETE CASCADE,
  code         TEXT NOT NULL,
  passed       BOOLEAN NOT NULL,
  tests_passed INT NOT NULL,
  tests_total  INT NOT NULL,
  runtime_ms   INT,
  created_at   TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS user_profiles (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email           TEXT UNIQUE,
  role            TEXT NOT NULL DEFAULT 'user',
  plan            TEXT NOT NULL DEFAULT 'free',
  plan_expires_at TIMESTAMPTZ,
  total_xp        INT NOT NULL DEFAULT 0,
  created_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_modules_course_order ON modules (course_id, sort_order);
CREATE INDEX IF NOT EXISTS idx_lessons_module_order ON lessons (module_id, sort_order);
CREATE INDEX IF NOT EXISTS idx_test_cases_lesson_order ON test_cases (lesson_id, sort_order);
CREATE INDEX IF NOT EXISTS idx_user_progress_status ON user_progress (user_id, status);
CREATE INDEX IF NOT EXISTS idx_submissions_user_lesson_time ON submissions (user_id, lesson_id, created_at DESC);

-- Part 11 Additions
ALTER TYPE lesson_type ADD VALUE IF NOT EXISTS 'concept';
ALTER TYPE lesson_type ADD VALUE IF NOT EXISTS 'quiz';
ALTER TYPE lesson_type ADD VALUE IF NOT EXISTS 'project';
ALTER TYPE lesson_type ADD VALUE IF NOT EXISTS 'checkpoint';

CREATE TABLE IF NOT EXISTS lesson_content (
  lesson_id UUID REFERENCES lessons(id) ON DELETE CASCADE,
  lang      TEXT NOT NULL DEFAULT 'en',
  title     TEXT NOT NULL,
  body_md   TEXT NOT NULL,
  PRIMARY KEY (lesson_id, lang)
);

ALTER TABLE lessons
  ADD COLUMN IF NOT EXISTS teaching_notes TEXT,
  ADD COLUMN IF NOT EXISTS difficulty INT CHECK (difficulty BETWEEN 1 AND 5),
  ADD COLUMN IF NOT EXISTS content_version INT NOT NULL DEFAULT 1;

CREATE TABLE IF NOT EXISTS quiz_questions (
  id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  lesson_id   UUID NOT NULL REFERENCES lessons(id) ON DELETE CASCADE,
  qtype       TEXT NOT NULL CHECK (qtype IN ('mcq_single','mcq_multi','predict_output','reorder','fill_blank')),
  prompt_md   TEXT NOT NULL,
  options     JSONB,
  answer      JSONB NOT NULL,
  explanation_md TEXT NOT NULL,
  sort_order  INT NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS roadmaps (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  slug TEXT UNIQUE NOT NULL, title TEXT NOT NULL, description TEXT,
  sort_order INT NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS roadmap_courses (
  roadmap_id UUID REFERENCES roadmaps(id) ON DELETE CASCADE,
  course_id  UUID REFERENCES courses(id)  ON DELETE CASCADE,
  position   INT NOT NULL,
  PRIMARY KEY (roadmap_id, course_id)
);

CREATE TABLE IF NOT EXISTS ai_usage (
  user_id UUID NOT NULL, day DATE NOT NULL, feature TEXT NOT NULL,
  calls INT NOT NULL DEFAULT 0, tokens_in INT NOT NULL DEFAULT 0, tokens_out INT NOT NULL DEFAULT 0,
  PRIMARY KEY (user_id, day, feature)
);

CREATE TABLE IF NOT EXISTS ai_feedback (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL, lesson_id UUID, mode TEXT, model TEXT,
  helpful BOOLEAN, created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS streaks (
  user_id UUID PRIMARY KEY, current INT NOT NULL DEFAULT 0, longest INT NOT NULL DEFAULT 0,
  last_active_date DATE, freezes_left INT NOT NULL DEFAULT 1
);

CREATE TABLE IF NOT EXISTS daily_activity (
  user_id UUID NOT NULL, day DATE NOT NULL,
  lessons_completed INT NOT NULL DEFAULT 0, xp INT NOT NULL DEFAULT 0,
  PRIMARY KEY (user_id, day)
);

CREATE TABLE IF NOT EXISTS daily_challenges (
  day DATE PRIMARY KEY, lesson_id UUID NOT NULL REFERENCES lessons(id)
);

CREATE TABLE IF NOT EXISTS content_reports (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  lesson_id UUID NOT NULL REFERENCES lessons(id) ON DELETE CASCADE,
  user_id UUID, kind TEXT, message TEXT, status TEXT NOT NULL DEFAULT 'open',
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS certificates (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  verify_code TEXT UNIQUE NOT NULL,
  user_id UUID NOT NULL, course_id UUID NOT NULL REFERENCES courses(id),
  display_name TEXT NOT NULL, issued_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS challenge_wrong_solutions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  lesson_id UUID NOT NULL REFERENCES challenges(lesson_id) ON DELETE CASCADE,
  label TEXT NOT NULL, code TEXT NOT NULL
);

-- ==============================================================================
-- 1. AUTH TRIGGER: Auto-create user_profile on auth.users sign-up (Supabase)
-- ==============================================================================
CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS trigger AS $$
BEGIN
  INSERT INTO public.user_profiles (id, email, role, plan, total_xp)
  VALUES (new.id, new.email, 'user', 'free', 0)
  ON CONFLICT (id) DO UPDATE SET email = EXCLUDED.email;
  RETURN new;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

DO $$ BEGIN
  IF EXISTS (SELECT 1 FROM pg_namespace WHERE nspname = 'auth') THEN
    DROP TRIGGER IF EXISTS on_auth_user_created ON auth.users;
    CREATE TRIGGER on_auth_user_created
      AFTER INSERT ON auth.users
      FOR EACH ROW EXECUTE FUNCTION public.handle_new_user();
  END IF;
END $$;

-- ==============================================================================
-- 2. ROW LEVEL SECURITY (RLS): Enable on ALL 22 public tables
-- ==============================================================================
ALTER TABLE categories ENABLE ROW LEVEL SECURITY;
ALTER TABLE courses ENABLE ROW LEVEL SECURITY;
ALTER TABLE modules ENABLE ROW LEVEL SECURITY;
ALTER TABLE lessons ENABLE ROW LEVEL SECURITY;
ALTER TABLE challenges ENABLE ROW LEVEL SECURITY;
ALTER TABLE challenge_hints ENABLE ROW LEVEL SECURITY;
ALTER TABLE test_cases ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_progress ENABLE ROW LEVEL SECURITY;
ALTER TABLE submissions ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE lesson_content ENABLE ROW LEVEL SECURITY;
ALTER TABLE quiz_questions ENABLE ROW LEVEL SECURITY;
ALTER TABLE roadmaps ENABLE ROW LEVEL SECURITY;
ALTER TABLE roadmap_courses ENABLE ROW LEVEL SECURITY;
ALTER TABLE ai_usage ENABLE ROW LEVEL SECURITY;
ALTER TABLE ai_feedback ENABLE ROW LEVEL SECURITY;
ALTER TABLE streaks ENABLE ROW LEVEL SECURITY;
ALTER TABLE daily_activity ENABLE ROW LEVEL SECURITY;
ALTER TABLE daily_challenges ENABLE ROW LEVEL SECURITY;
ALTER TABLE content_reports ENABLE ROW LEVEL SECURITY;
ALTER TABLE certificates ENABLE ROW LEVEL SECURITY;
ALTER TABLE challenge_wrong_solutions ENABLE ROW LEVEL SECURITY;

-- Allow public read of published curriculum structure (excluding solution/hidden tests)
DO $$ BEGIN
  CREATE POLICY "Public read categories" ON categories FOR SELECT USING (true);
  CREATE POLICY "Public read published courses" ON courses FOR SELECT USING (is_published = true);
  CREATE POLICY "Public read modules" ON modules FOR SELECT USING (true);
  CREATE POLICY "Public read published lessons" ON lessons FOR SELECT USING (is_published = true);
  CREATE POLICY "Public read bilingual lesson content" ON lesson_content FOR SELECT USING (true);
  CREATE POLICY "Public read roadmaps" ON roadmaps FOR SELECT USING (true);
  CREATE POLICY "Public read roadmap_courses" ON roadmap_courses FOR SELECT USING (true);
  CREATE POLICY "Public read certificates" ON certificates FOR SELECT USING (true);
  CREATE POLICY "Public read visible tests" ON test_cases FOR SELECT USING (NOT is_hidden);
EXCEPTION WHEN duplicate_object THEN null;
END $$;

