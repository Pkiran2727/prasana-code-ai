import re

with open('frontend/src/styles/globals.css', 'r') as f:
    css = f.read()

dark_vars = """
    --c-emerald-300: #6ee7b7;
    --c-emerald-400: #34d399;
    --c-emerald-500: #10b981;
    --c-teal-300: #5eead4;
    --c-teal-400: #2dd4bf;
    --c-teal-500: #14b8a6;
"""

light_vars = """
    --c-emerald-300: #047857; /* 700 */
    --c-emerald-400: #059669; /* 600 */
    --c-emerald-500: #10b981;
    --c-teal-300: #0f766e; /* 700 */
    --c-teal-400: #0d9488; /* 600 */
    --c-teal-500: #14b8a6;
"""

# Insert dark_vars before "/* Semantic backgrounds */" in Dark theme
css = css.replace("    /* Semantic backgrounds */", dark_vars + "\n    /* Semantic backgrounds */", 1)

# Insert light_vars before "/* Semantic backgrounds */" in Light theme
css = css.replace("    /* Semantic backgrounds */", light_vars + "\n    /* Semantic backgrounds */", 1)

# Also apply the same dark_vars to HC Dark, and light_vars to HC Light
css = css.replace("    --bg-app: #000000;", dark_vars + "\n    --bg-app: #000000;", 1)
css = css.replace("    --bg-app: #ffffff;", light_vars + "\n    --bg-app: #ffffff;", 1)

with open('frontend/src/styles/globals.css', 'w') as f:
    f.write(css)

