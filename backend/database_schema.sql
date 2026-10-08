CREATE TYPE lesson_type AS ENUM ('lesson', 'challenge');
CREATE TYPE progress_status AS ENUM ('not_started', 'in_progress', 'completed');

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

-- Note: Ensure user_profiles has plan, plan_expires_at, total_xp 
-- ALTER TABLE user_profiles ADD COLUMN IF NOT EXISTS plan TEXT NOT NULL DEFAULT 'free';
-- ALTER TABLE user_profiles ADD COLUMN IF NOT EXISTS plan_expires_at TIMESTAMPTZ;
-- ALTER TABLE user_profiles ADD COLUMN IF NOT EXISTS total_xp INT NOT NULL DEFAULT 0;

CREATE INDEX IF NOT EXISTS idx_modules_course_order ON modules (course_id, sort_order);
CREATE INDEX IF NOT EXISTS idx_lessons_module_order ON lessons (module_id, sort_order);
CREATE INDEX IF NOT EXISTS idx_test_cases_lesson_order ON test_cases (lesson_id, sort_order);
CREATE INDEX IF NOT EXISTS idx_user_progress_status ON user_progress (user_id, status);
CREATE INDEX IF NOT EXISTS idx_submissions_user_lesson_time ON submissions (user_id, lesson_id, created_at DESC);
