"""
Curriculum & Problem Bank Data for Prasana Code AI
Contains structured courses, modules, lessons, and practice problems with automated test verification.
"""

import os
import json
import glob

def _load_python_foundations():
    """Dynamically loads Python Foundations lessons from content JSON files."""
    possible_paths = [
        os.path.join(os.path.dirname(__file__), "../content/python/py-foundations"),
        os.path.join(os.getcwd(), "content/python/py-foundations"),
        "/app/content/python/py-foundations"
    ]
    base_dir = next((p for p in possible_paths if os.path.exists(p)), None)
    if not base_dir:
        return []

    modules = {
        "m01-first-steps": {"id": "py-m01", "title": "Module 1: First Steps with Python", "desc": "Master print statements, multiline formatting, and code comments.", "lessons": []},
        "m02-variables-types": {"id": "py-m02", "title": "Module 2: Variables & Data Types", "desc": "Declare variables, perform numeric calculations, and capture user inputs.", "lessons": []},
        "m03-strings": {"id": "py-m03", "title": "Module 3: Working with Strings", "desc": "Format string outputs, slice text substrings, and work with character indexing.", "lessons": []}
    }

    # Map slugs to helpful Telugu instructions fallback
    te_instruction_map = {
        "py-f-m01-l01-print": "`print()` ఫంక్షన్ ఉపయోగించి స్క్రీన్‌పై ఖచ్చితంగా `Namaste, Python!` అని ప్రింట్ చేయండి.",
        "py-f-m01-l02-multiline": "రెండు వేర్వేరు లైన్లలో వరుసగా `Line 1` మరియు `Line 2` అని ప్రింట్ చేయండి.",
        "py-f-m01-l03-comments": "కామెంట్స్ రాసి, కేవలం `Code with Comments` అనే టెక్స్ట్‌ని మాత్రమే ప్రింట్ చేయండి.",
        "py-f-m02-l01-variables": "`city` అనే వేరియబుల్‌లో `\"Hyderabad\"` ని స్టోర్ చేసి, ఆ వేరియబుల్‌ని `print(city)` ద్వారా ప్రింట్ చేయండి.",
        "py-f-m02-l02-numbers": "`a = 15`, `b = 25` తీసుకొని, వాటి మొత్తం `print(a + b)` ద్వారా `40` ని ప్రింట్ చేయండి.",
        "py-f-m02-l03-input": "`input()` ద్వారా యూజర్ పేరును తీసుకొని `Hello, <name>!` అని పలకరించండి.",
        "py-f-m03-l01-concat": "`+` ఆపరేటర్ వాడి రెండు స్ట్రింగ్స్‌ని కలిపి ప్రింట్ చేయండి.",
        "py-f-m03-l02-fstrings": "`f-string` ఫార్మాట్ వాడి వేరియబుల్స్ విలువలను అందంగా అమర్చి ప్రింట్ చేయండి.",
        "py-f-m03-l03-indexing": "స్ట్రింగ్ ఇండెక్సింగ్ `[0]` వాడి మొదటి అక్షరాన్ని ప్రింట్ చేయండి.",
        "py-f-m03-l04-slicing": "స్ట్రింగ్ స్లైసింగ్ `[start:end]` ద్వారా కావలసిన భాగాన్ని కట్ చేసి ప్రింట్ చేయండి."
    }

    for f in sorted(glob.glob(f"{base_dir}/*/*.json")):
        try:
            with open(f, "r", encoding="utf-8") as fp:
                d = json.load(fp)
            mod_key = d.get("module")
            if mod_key in modules:
                ch = d.get("challenge", {})
                test_cases = [
                    {"input": t.get("stdin", ""), "expected": t.get("expected", "")} 
                    for t in ch.get("tests", []) if not t.get("hidden")
                ]
                if not test_cases and ch.get("tests"):
                    test_cases = [{"input": ch["tests"][0].get("stdin", ""), "expected": ch["tests"][0].get("expected", "")}]

                slug = d["slug"]
                lesson_entry = {
                    "id": slug,
                    "title": d["content"]["en"]["title"],
                    "title_te": d.get("content", {}).get("te", {}).get("title", d["content"]["en"]["title"]),
                    "instructions": ch.get("instructions_md", ""),
                    "instructions_te": te_instruction_map.get(slug, ch.get("instructions_md", "")),
                    "theory_en": d.get("content", {}).get("en", {}).get("body_md", ""),
                    "theory_te": d.get("content", {}).get("te", {}).get("body_md", d.get("content", {}).get("en", {}).get("body_md", "")),
                    "starterCode": ch.get("starter_code", ""),
                    "solutionCode": ch.get("solution_code", ""),
                    "expectedOutput": test_cases[0]["expected"] if test_cases else "",
                    "testCases": test_cases,
                    "allTests": ch.get("tests", []),
                    "quiz": d.get("quiz", []),
                    "hint": ch.get("hints", ["Review the concept notes."])[0] if ch.get("hints") else "Review the notes.",
                    "hints": ch.get("hints", []),
                    "hints_te": ch.get("hints_te", ["కాన్సెప్ట్ సూచనలను పరిశీలించి కోడ్ రాయండి."]),
                    "language": "python",
                    "xp": d.get("xp", 10),
                    "difficulty": d.get("difficulty", 1)
                }
                modules[mod_key]["lessons"].append(lesson_entry)
        except Exception as e:
            print(f"Error loading lesson file {f}: {e}")

    return [m for m in modules.values() if m["lessons"]]

# Load foundations dynamically
python_foundation_modules = _load_python_foundations()

# Append Module 4: OOP and Exception Handling to Python Track (idempotent)
if not any(m.get("id") == "py-m04" for m in python_foundation_modules):
    python_foundation_modules.append({
        "id": "py-m04",
        "title": "Module 4: Object-Oriented Programming (OOP) & Exceptions",
        "desc": "Master class definitions, __init__ constructors, object methods, and safe exception handling.",
    "lessons": [
        {
            "id": "py-f-m04-l01-classes",
            "title": "Classes & Objects in Python",
            "title_te": "పైథాన్ క్లాసులు & ఆబ్జెక్టులు (OOP)",
            "instructions": "Create a class `Coder` with an `__init__` constructor accepting `name` and `language`, and a method `info()` returning `'<name> codes in <language>'`. Instantiate `dev = Coder('Prasana', 'Python')` and print `dev.info()`.",
            "instructions_te": "`name` మరియు `language` తీసుకునే `Coder` క్లాస్ రాసి, `Coder('Prasana', 'Python')` ఆబ్జెక్ట్ నుండి `info()` ని ప్రింట్ చేయండి.",
            "theory_en": "Object-Oriented Programming (OOP) models real-world entities through classes and objects.\n\n```python\nclass Coder:\n    def __init__(self, name, lang):\n        self.name = name\n        self.lang = lang\n    def info(self):\n        return f'{self.name} codes in {self.lang}'\n\ndev = Coder('Prasana', 'Python')\nprint(dev.info())\n```",
            "theory_te": "క్లాసులు ఆబ్జెక్టులను సృష్టించే బ్లూప్రింట్లు. `__init__` మెథడ్ కన్‌స్ట్రక్టర్ లా పనిచేస్తుంది.",
            "starterCode": "class Coder:\n    def __init__(self, name, language):\n        self.name = name\n        self.language = language\n    def info(self):\n        return f\"{self.name} codes in {self.language}\"\n\ndev = Coder(\"Prasana\", \"Python\")\nprint(dev.info())\n",
            "expectedOutput": "Prasana codes in Python",
            "testCases": [{"input": "", "expected": "Prasana codes in Python"}],
            "hint": "Define class Coder with __init__(self, name, language) and info(self).",
            "hints_te": ["`def __init__(self, name, language):` అని రాయండి."],
            "language": "python",
            "xp": 20
        },
        {
            "id": "py-f-m04-l02-exceptions",
            "title": "Exception Handling with try-except",
            "title_te": "ఎర్రర్ హ్యాండ్లింగ్ (try & except)",
            "instructions": "Write a function `safe_divide(a, b)` that catches `ZeroDivisionError` and returns `'Division by zero error'`, or returns `a // b`. Print `safe_divide(10, 0)`.",
            "instructions_te": "`ZeroDivisionError` వచ్చినప్పుడు `'Division by zero error'` ని రిటర్న్ చేసే `safe_divide(a, b)` ఫంక్షన్ రాసి, `safe_divide(10, 0)` ని ప్రింట్ చేయండి.",
            "theory_en": "`try-except` blocks prevent Python programs from terminating unexpectedly when an exception arises at runtime.",
            "theory_te": "రన్‌టైమ్ ఎర్రర్స్ వచ్చినప్పుడు ప్రోగ్రామ్ ఆగిపోకుండా `try-except` బ్లాక్స్ వాడతాము.",
            "starterCode": "def safe_divide(a, b):\n    try:\n        return a // b\n    except ZeroDivisionError:\n        return 'Division by zero error'\n\nprint(safe_divide(10, 0))\n",
            "expectedOutput": "Division by zero error",
            "testCases": [{"input": "", "expected": "Division by zero error"}],
            "hint": "Use try: return a // b except ZeroDivisionError: return 'Division by zero error'",
            "hints_te": ["`try:` మరియు `except ZeroDivisionError:` వాడండి."],
            "language": "python",
            "xp": 20
        }
    ]
})

JOURNEYS_DATA = [
    {
        "id": "python-developer",
        "title": "Python Developer Journey",
        "category": "Python",
        "icon": "🐍",
        "badge": "Comprehensive",
        "description": "Master Python from syntax fundamentals to Object-Oriented Programming, Data Analysis, and Automation with Telugu & English lessons.",
        "estimatedHours": 14,
        "courses": python_foundation_modules
    },
    {
        "id": "web-development",
        "title": "Full-Stack Web Development Journey",
        "category": "Web Dev",
        "icon": "🌐",
        "badge": "Popular",
        "description": "Build modern interactive web apps with JavaScript, ES6, Async/Await, and modern DOM principles with bilingual explanations.",
        "estimatedHours": 20,
        "courses": [
            {
                "id": "js-m01",
                "title": "Module 1: JavaScript Fundamentals & ES6",
                "desc": "Master variable declaration, scopes, arrow functions, and modern string templates.",
                "lessons": [
                    {
                        "id": "js-m01-l01-variables",
                        "title": "Modern Variables (let vs const)",
                        "title_te": "జావాస్క్రిప్ట్ వేరియబుల్స్ (let & const)",
                        "instructions": "Declare a constant named `appName` with value `'Prasana Code AI'`, and a variable `userCount` with value `100`. Print both using `console.log()` separated by a space.",
                        "instructions_te": "`appName` అనే కాన్స్టెంట్‌ని `'Prasana Code AI'` విలువతో, `userCount` వేరియబుల్‌ని `100` తో డిక్లేర్ చేసి `console.log(appName, userCount)` ద్వారా ప్రింట్ చేయండి.",
                        "theory_en": "In modern JavaScript (ES6+), we use `const` for values that do not change and `let` for variables that will be reassigned. Avoid legacy `var` to prevent scope pollution.\n\n```javascript\nconst name = 'Prasana';\nlet score = 50;\nconsole.log(name, score);\n```",
                        "theory_te": "జావాస్క్రిప్ట్‌లో విలువ మారకుండా ఉండే వాటికి `const`, విలువ మారే వాటికి `let` వాడతాము. పాత `var` ని వాడటం వల్ల గ్లోబల్ స్కోప్ సమస్యలు రావచ్చు.\n\n```javascript\nconst name = 'Prasana';\nlet score = 50;\nconsole.log(name, score);\n```",
                        "starterCode": "// Task: Declare appName (const) and userCount (let)\n// Task: Print both using console.log\n",
                        "expectedOutput": "Prasana Code AI 100",
                        "testCases": [{"input": "", "expected": "Prasana Code AI 100"}],
                        "hint": "Use: const appName = 'Prasana Code AI'; let userCount = 100; console.log(appName, userCount);",
                        "hints_te": ["`const appName = 'Prasana Code AI';` రాయండి.", "`let userCount = 100;` రాయండి.", "`console.log(appName, userCount);` ద్వారా అవుట్‌పుట్ పొందండి."],
                        "language": "javascript",
                        "xp": 10
                    },
                    {
                        "id": "js-m01-l02-functions",
                        "title": "Arrow Functions & Syntax",
                        "title_te": "ఆరో ఫంక్షన్స్ (Arrow Functions)",
                        "instructions": "Write an arrow function `multiply(a, b)` that returns the product of `a` and `b`. Then print `multiply(6, 7)`.",
                        "instructions_te": "`a` మరియు `b` ని గుణించి ఇచ్చే `multiply(a, b)` ఆరో ఫంక్షన్‌ని రాసి, `multiply(6, 7)` అవుట్‌పుట్‌ని `console.log` ద్వారా ప్రింట్ చేయండి.",
                        "theory_en": "Arrow functions provide a clean, concise syntax for writing functions in JavaScript.\n\n```javascript\nconst add = (a, b) => a + b;\nconsole.log(add(5, 3)); // 8\n```",
                        "theory_te": "ఆరో ఫంక్షన్స్ (`=>`) జావాస్క్రిప్ట్‌లో ఫంక్షన్స్ రాయడానికి చాలా సులభమైన ఆధునిక పద్ధతి.\n\n```javascript\nconst add = (a, b) => a + b;\nconsole.log(add(5, 3));\n```",
                        "starterCode": "// Task: Create multiply arrow function\nconst multiply = (a, b) => {\n  // Your code here\n};\n\nconsole.log(multiply(6, 7));\n",
                        "expectedOutput": "42",
                        "testCases": [{"input": "", "expected": "42"}],
                        "hint": "Return a * b inside the function: `const multiply = (a, b) => a * b;`",
                        "hints_te": ["ఫంక్షన్ లోపల `return a * b;` రాయండి."],
                        "language": "javascript",
                        "xp": 15
                    }
                ]
            },
            {
                "id": "js-m02",
                "title": "Module 2: Array Filtering & Mapping",
                "desc": "Process collections using functional array methods: filter, map, and reduce.",
                "lessons": [
                    {
                        "id": "js-m02-l01-arrays",
                        "title": "Filtering Even Numbers",
                        "title_te": "అరే ఫిల్టరింగ్ (Array Filter)",
                        "instructions": "Given the array `[10, 15, 20, 25, 30]`, use `.filter()` to keep only even numbers, then print the resulting array with `console.log()`.",
                        "instructions_te": "`[10, 15, 20, 25, 30]` అరే లోని సరి సంఖ్యలను (Even Numbers) `.filter()` ద్వారా సేకరించి ప్రింట్ చేయండి.",
                        "theory_en": "The `.filter()` method creates a shallow copy of a portion of a given array, filtered down to just the elements that pass the test implemented by the provided function.\n\n```javascript\nconst numbers = [1, 2, 3, 4];\nconst evens = numbers.filter(n => n % 2 === 0);\nconsole.log(evens); // [2, 4]\n```",
                        "theory_te": "`.filter()` మెథడ్ ఒక అరే లోని ఎలిమెంట్స్ లో మన షరతుకు సరిపోయే వాటిని మాత్రమే కొత్త అరే లోకి తీసుకుంటుంది.\n\n```javascript\nconst evens = numbers.filter(n => n % 2 === 0);\n```",
                        "starterCode": "const nums = [10, 15, 20, 25, 30];\n// Task: Filter even numbers and console.log\n",
                        "expectedOutput": "[ 10, 20, 30 ]",
                        "testCases": [{"input": "", "expected": "[ 10, 20, 30 ]"}],
                        "hint": "Use: const evens = nums.filter(n => n % 2 === 0); console.log(evens);",
                        "hints_te": ["`n % 2 === 0` అయితే అది సరి సంఖ్య.", "`console.log(nums.filter(n => n % 2 === 0));` రాయండి."],
                        "language": "javascript",
                        "xp": 15
                    }
                ]
            },
            {
                "id": "js-m03",
                "title": "Module 3: Asynchronous JavaScript",
                "desc": "Handle asynchronous operations smoothly using Promises and Async/Await.",
                "lessons": [
                    {
                        "id": "js-m03-l01-async",
                        "title": "Async Functions & Await",
                        "title_te": "అసింక్ & అవేట్ (Async & Await)",
                        "instructions": "Write an async function `fetchStatus()` that resolves with `'Service Ready'` and print the resolved result.",
                        "instructions_te": "`'Service Ready'` ని రిజాల్వ్ చేసే `fetchStatus()` అసింక్ ఫంక్షన్ రాసి, దాని రిజల్ట్‌ని ప్రింట్ చేయండి.",
                        "theory_en": "`async` functions always return a Promise. The `await` keyword pauses execution until the Promise settles.\n\n```javascript\nasync function getData() {\n  return 'Success';\n}\ngetData().then(console.log);\n```",
                        "theory_te": "`async` ఫంక్షన్స్ ఎప్పుడూ ఒక Promise ని రిటర్న్ చేస్తాయి. డేటా లోడ్ అయ్యే వరకు వేచి చూడటానికి `await` వాడతాము.",
                        "starterCode": "async function fetchStatus() {\n  return 'Service Ready';\n}\n\nfetchStatus().then(res => console.log(res));\n",
                        "expectedOutput": "Service Ready",
                        "testCases": [{"input": "", "expected": "Service Ready"}],
                        "hint": "Call fetchStatus().then(console.log);",
                        "hints_te": ["`fetchStatus().then(console.log);` అని కాల్ చేయండి."],
                        "language": "javascript",
                        "xp": 20
                    }
                ]
            },
            {
                "id": "js-m04",
                "title": "Module 4: JSON Parsing & Data APIs",
                "desc": "Work with JSON payloads, object serialization, and HTTP API handling.",
                "lessons": [
                    {
                        "id": "js-m04-l01-json",
                        "title": "JSON Parsing & Serialization",
                        "title_te": "జావాస్క్రిప్ట్‌లో JSON హ్యాండ్లింగ్",
                        "instructions": "Given a JSON string `raw = '{\"name\":\"Mitra\",\"role\":\"AI Tutor\"}'`, parse it using `JSON.parse()` and print `parsed.name` and `parsed.role` separated by a space using `console.log()`.",
                        "instructions_te": "`JSON.parse()` వాడి JSON స్ట్రింగ్‌ని ఆబ్జెక్ట్‌గా మార్చి `name` మరియు `role` ని ప్రింట్ చేయండి.",
                        "theory_en": "`JSON.parse()` converts a formatted JSON string into a structured JavaScript object.",
                        "theory_te": "సర్వర్ నుండి వచ్చే JSON డేటాను జావాస్క్రిప్ట్ ఆబ్జెక్ట్‌గా మార్చడానికి `JSON.parse()` వాడతాము.",
                        "starterCode": "const raw = '{\"name\":\"Mitra\",\"role\":\"AI Tutor\"}';\nconst parsed = JSON.parse(raw);\nconsole.log(parsed.name, parsed.role);\n",
                        "expectedOutput": "Mitra AI Tutor",
                        "testCases": [{"input": "", "expected": "Mitra AI Tutor"}],
                        "hint": "const parsed = JSON.parse(raw); console.log(parsed.name, parsed.role);",
                        "hints_te": ["`const parsed = JSON.parse(raw);` తర్వాత `console.log(parsed.name, parsed.role);` రాయండి."],
                        "language": "javascript",
                        "xp": 15
                    }
                ]
            }
        ]
    },
    {
        "id": "dsa-mastery",
        "title": "Data Structures & Algorithms (DSA)",
        "category": "DSA",
        "icon": "⚡",
        "badge": "Interview Prep",
        "description": "Crack technical coding interviews with core algorithms, Two Pointers, Stacks, Trees, and Dynamic Programming.",
        "estimatedHours": 22,
        "courses": [
            {
                "id": "dsa-m01",
                "title": "Module 1: Arrays & Two Pointers",
                "desc": "Solve linear search, frequency counting, and two-pointer traversal problems.",
                "lessons": [
                    {
                        "id": "dsa-m01-l01-twosum",
                        "title": "Two Sum (Hash Map Approach)",
                        "title_te": "టూ సమ్ ప్రాబ్లమ్ (Two Sum)",
                        "instructions": "Given an array `nums` and integer `target`, return the two indices that add up to `target`. Print the result list.",
                        "instructions_te": "`nums = [2, 7, 11, 15]` మరియు `target = 9` ఇచ్చినప్పుడు, మొత్తం 9 వచ్చే రెండు సంఖ్యల ఇండెక్స్‌లు `[0, 1]` ని రిటర్న్ చేసి ప్రింట్ చేయండి.",
                        "theory_en": "Instead of a brute-force O(n²) double loop, a hash map lets you lookup the required complement `target - num` in O(1) time, bringing overall complexity to O(n).\n\n```python\nseen = {}\nfor i, num in enumerate(nums):\n    diff = target - num\n    if diff in seen:\n        return [seen[diff], i]\n    seen[num] = i\n```",
                        "theory_te": "రెండు లూప్‌లు వాడి O(n²) సమయం వేస్ట్ చేయకుండా, Hash Map (Dictionary) ద్వారా కావాల్సిన సంఖ్యను O(1) సమయంలో కనుగొనవచ్చు.",
                        "starterCode": "def two_sum(nums, target):\n    seen = {}\n    for i, num in enumerate(nums):\n        diff = target - num\n        if diff in seen:\n            return [seen[diff], i]\n        seen[num] = i\n    return []\n\nprint(two_sum([2, 7, 11, 15], 9))\n",
                        "expectedOutput": "[0, 1]",
                        "testCases": [{"input": "", "expected": "[0, 1]"}],
                        "hint": "Check `if target - num in seen:` before adding to dictionary.",
                        "hints_te": ["డిక్షనరీలో `target - num` ఉందో లేదో సరిచూడండి."],
                        "language": "python",
                        "xp": 25
                    },
                    {
                        "id": "dsa-m01-l02-reverse",
                        "title": "Reverse String In-Place",
                        "title_te": "స్ట్రింగ్ రివర్స్ చేయడం (Two Pointers)",
                        "instructions": "Reverse the list of characters `['h', 'e', 'l', 'l', 'o']` in-place using two pointers and print the result.",
                        "instructions_te": "`left` మరియు `right` పాయింటర్స్ వాడి లిస్ట్‌ని రివర్స్ చేసి `print(chars)` చేయండి.",
                        "theory_en": "Use `left = 0` and `right = len(arr) - 1`. Swap elements and move inward until they cross.\n\n```python\nwhile left < right:\n    arr[left], arr[right] = arr[right], arr[left]\n    left += 1\n    right -= 1\n```",
                        "theory_te": "మొదటి మరియు చివరి ఎలిమెంట్స్ ను పరస్పరం మార్చుకుంటూ (Swap) మధ్యలోకి రావడం టూ పాయింటర్స్ టెక్నిక్.",
                        "starterCode": "chars = ['h', 'e', 'l', 'l', 'o']\nleft, right = 0, len(chars) - 1\nwhile left < right:\n    chars[left], chars[right] = chars[right], chars[left]\n    left += 1\n    right -= 1\n\nprint(chars)\n",
                        "expectedOutput": "['o', 'l', 'l', 'e', 'h']",
                        "testCases": [{"input": "", "expected": "['o', 'l', 'l', 'e', 'h']"}],
                        "hint": "Swap using Python syntax: a, b = b, a",
                        "hints_te": ["`chars[left], chars[right] = chars[right], chars[left]` ద్వారా స్వాప్ చేయండి."],
                        "language": "python",
                        "xp": 20
                    }
                ]
            },
            {
                "id": "dsa-m02",
                "title": "Module 2: Stacks & Balanced Brackets",
                "desc": "Master LIFO stack applications for expression validation and parsing.",
                "lessons": [
                    {
                        "id": "dsa-m02-l01-parentheses",
                        "title": "Valid Parentheses Checker",
                        "title_te": "బ్రాకెట్స్ సరిచూడటం (Stack LIFO)",
                        "instructions": "Determine if the bracket string `'()[]{}'` is valid. Return and print `True` if all open brackets are correctly closed.",
                        "instructions_te": "`'()[]{}'` లోని ప్రతి బ్రాకెట్ సరిగ్గా మూయబడిందో లేదో స్టాక్ వాడి నిర్ధారించి `True` అని ప్రింట్ చేయండి.",
                        "theory_en": "A stack allows checking nested matching pairs in LIFO order (Last In, First Out). Push opening brackets; pop and compare upon encountering closing brackets.",
                        "theory_te": "ఓపెనింగ్ బ్రాకెట్స్ వచ్చినప్పుడు స్టాక్ లోకి వేసి, క్లోజింగ్ బ్రాకెట్స్ వచ్చినప్పుడు చివరగా వచ్చినది సరిపోతుందో లేదో చూడాలి.",
                        "starterCode": "def is_valid(s):\n    stack = []\n    mapping = {')': '(', '}': '{', ']': '['}\n    for char in s:\n        if char in mapping:\n            top = stack.pop() if stack else '#'\n            if mapping[char] != top:\n                return False\n        else:\n            stack.append(char)\n    return not stack\n\nprint(is_valid('()[]{}'))\n",
                        "expectedOutput": "True",
                        "testCases": [{"input": "", "expected": "True"}],
                        "hint": "Ensure stack is empty at the end: `return not stack`",
                        "hints_te": ["స్టాక్ చివర్లో ఖాళీగా ఉంటేనే బ్రాకెట్స్ అన్నీ సరిగ్గా మూయబడినట్లు."],
                        "language": "python",
                        "xp": 25
                    }
                ]
            },
            {
                "id": "dsa-m03",
                "title": "Module 3: Searching & Sorting Algorithms",
                "desc": "Master Divide and Conquer algorithmic patterns and logarithmic search.",
                "lessons": [
                    {
                        "id": "dsa-m03-l01-binarysearch",
                        "title": "Binary Search in O(log n)",
                        "title_te": "బైనరీ సెర్చ్ (Binary Search)",
                        "instructions": "Implement binary search to find target `16` in sorted list `[2, 5, 8, 12, 16, 23, 38]`. Print the found index `4`.",
                        "instructions_te": "క్రమబద్ధీకరించిన లిస్ట్‌లో బైనరీ సెర్చ్ ద్వారా `16` ఉన్న ఇండెక్స్ `4` ని కనుగొని ప్రింట్ చేయండి.",
                        "theory_en": "Binary search repeatedly divides the search interval in half to locate an element in O(log n) time.",
                        "theory_te": "సార్ట్ చేయబడిన లిస్ట్‌లో మధ్య ఎలిమెంట్‌తో పోల్చుకుంటూ O(log n) సమయంలో సెర్చ్ చేయవచ్చు.",
                        "starterCode": "def binary_search(arr, target):\n    low, high = 0, len(arr) - 1\n    while low <= high:\n        mid = (low + high) // 2\n        if arr[mid] == target:\n            return mid\n        elif arr[mid] < target:\n            low = mid + 1\n        else:\n            high = mid - 1\n    return -1\n\nprint(binary_search([2, 5, 8, 12, 16, 23, 38], 16))\n",
                        "expectedOutput": "4",
                        "testCases": [{"input": "", "expected": "4"}],
                        "hint": "Use low, high pointers and calculate mid = (low + high) // 2.",
                        "hints_te": ["`low, high` పాయింటర్స్ వాడి ప్రతి రౌండ్‌లోనూ `mid = (low + high) // 2` లెక్కించండి."],
                        "language": "python",
                        "xp": 25
                    }
                ]
            }
        ]
    },
    {
        "id": "cpp-mastery",
        "title": "C++ & Systems Programming",
        "category": "C++",
        "icon": "⚙️",
        "badge": "Performance",
        "description": "Master low-level control, pointers, references, memory allocation, and STL containers.",
        "estimatedHours": 18,
        "courses": [
            {
                "id": "cpp-m01",
                "title": "Module 1: C++ Fundamentals & Standard I/O",
                "desc": "Understand compiled execution, main function entry, namespaces, and streams.",
                "lessons": [
                    {
                        "id": "cpp-m01-l01-io",
                        "title": "Hello World with std::cout",
                        "title_te": "C++ లో మొదటి ప్రోగ్రామ్",
                        "instructions": "Write a C++ program that prints `Namaste, C++!` to standard output using `std::cout`.",
                        "instructions_te": "`std::cout` ఉపయోగించి `Namaste, C++!` ని స్క్రీన్‌పై ప్రింట్ చేసే C++ ప్రోగ్రామ్ రాయండి.",
                        "theory_en": "In C++, the `<iostream>` header provides input and output streams. The `std::cout` stream combined with the stream insertion operator `<<` sends data to standard output.\n\n```cpp\n#include <iostream>\nint main() {\n    std::cout << \"Hello!\" << std::endl;\n    return 0;\n}\n```",
                        "theory_te": "C++ లో అవుట్‌పుట్ చూపించడానికి `<iostream>` లోని `std::cout <<` ఆపరేటర్ వాడతాము. ప్రతి ప్రోగ్రామ్ `main()` ఫంక్షన్ తో ప్రారంభమవుతుంది.",
                        "starterCode": "#include <iostream>\n\nint main() {\n    // Task: Print Namaste, C++!\n    std::cout << \"Namaste, C++!\" << std::endl;\n    return 0;\n}\n",
                        "expectedOutput": "Namaste, C++!",
                        "testCases": [{"input": "", "expected": "Namaste, C++!"}],
                        "hint": "Use std::cout << \"Namaste, C++!\" << std::endl;",
                        "hints_te": ["`std::cout << \"Namaste, C++!\" << std::endl;` రాయండి."],
                        "language": "cpp",
                        "xp": 15
                    },
                    {
                        "id": "cpp-m01-l02-functions",
                        "title": "Functions & Pass-by-Reference",
                        "title_te": "C++ ఫంక్షన్స్ & రిఫరెన్స్ (&)",
                        "instructions": "Create a function `square(int n)` that returns `n * n`. In `main()`, print `square(7)`.",
                        "instructions_te": "`n * n` ని ఇచ్చే `square(int n)` ఫంక్షన్ రాసి, `square(7)` విలువ `49` ని ప్రింట్ చేయండి.",
                        "theory_en": "C++ functions require explicit return types and parameter types.\n\n```cpp\nint square(int n) {\n    return n * n;\n}\n```",
                        "theory_te": "C++ లో ఫంక్షన్స్ కి ఖచ్చితమైన డేటా టైప్స్ (`int`, `float`, `void`) ముందే డిక్లేర్ చేయాలి.",
                        "starterCode": "#include <iostream>\n\nint square(int n) {\n    return n * n;\n}\n\nint main() {\n    std::cout << square(7) << std::endl;\n    return 0;\n}\n",
                        "expectedOutput": "49",
                        "testCases": [{"input": "", "expected": "49"}],
                        "hint": "Return n * n and print via std::cout.",
                        "hints_te": ["`std::cout << square(7) << std::endl;` ని ప్రింట్ చేయండి."],
                        "language": "cpp",
                        "xp": 20
                    }
                ]
            },
            {
                "id": "cpp-m02",
                "title": "Module 2: Pointers & Memory Management",
                "desc": "Master direct memory addressing, pointer dereferencing, and references.",
                "lessons": [
                    {
                        "id": "cpp-m02-l01-pointers",
                        "title": "Pointers & Address-Of Operator",
                        "title_te": "C++ పాయింటర్స్ & మెమరీ అడ్రస్ (* &)",
                        "instructions": "Declare an integer `val = 42`, create a pointer `ptr = &val`, and print the dereferenced value `*ptr` using `std::cout`.",
                        "instructions_te": "`val = 42` యొక్క అడ్రస్‌ను `int* ptr = &val` లో ఉంచి, `*ptr` ద్వారా దాని విలువ `42` ని ప్రింట్ చేయండి.",
                        "theory_en": "A pointer holds the memory address of another variable. The `&` operator retrieves an address, and the `*` operator dereferences a pointer to access the stored value.\n\n```cpp\nint x = 10;\nint* p = &x;\nstd::cout << *p << std::endl; // 10\n```",
                        "theory_te": "పాయింటర్ అంటే వేరొక వేరియబుల్ యొక్క మెమరీ అడ్రస్‌ను స్టోర్ చేసే వేరియబుల్. `&` అడ్రస్‌ని ఇస్తే, `*` ఆ అడ్రస్‌లోని విలువని ఇస్తుంది.",
                        "starterCode": "#include <iostream>\n\nint main() {\n    int val = 42;\n    int* ptr = &val;\n    std::cout << *ptr << std::endl;\n    return 0;\n}\n",
                        "expectedOutput": "42",
                        "testCases": [{"input": "", "expected": "42"}],
                        "hint": "Dereference using *ptr and print with std::cout << *ptr << std::endl;",
                        "hints_te": ["`std::cout << *ptr << std::endl;` ద్వారా ప్రింట్ చేయండి."],
                        "language": "cpp",
                        "xp": 25
                    }
                ]
            }
        ]
    },
    {
        "id": "ai-engineering",
        "title": "Artificial Intelligence & Prompt Engineering",
        "category": "AI",
        "icon": "🤖",
        "badge": "Emerging",
        "description": "Learn LLM architectures, system prompt design, JSON outputs, and agentic tool-calling workflows.",
        "estimatedHours": 16,
        "courses": [
            {
                "id": "ai-m01",
                "title": "Module 1: Prompt Engineering & Structured Outputs",
                "desc": "Format LLM prompts for deterministic JSON schemas and system instruction boundaries.",
                "lessons": [
                    {
                        "id": "ai-m01-l01-json",
                        "title": "Structured JSON Prompt Formatting",
                        "title_te": "LLM కోసం JSON ఫార్మాటింగ్",
                        "instructions": "Construct a Python dictionary representing an AI message with keys `'role'` set to `'user'` and `'content'` set to `'Teach me Python'`, convert it to a JSON string using `json.dumps()`, and print it.",
                        "instructions_te": "`'role': 'user'` మరియు `'content': 'Teach me Python'` ఉన్న డిక్షనరీని JSON స్ట్రింగ్‌గా మార్చి ప్రింట్ చేయండి.",
                        "theory_en": "Modern AI APIs (OpenAI, Gemini, Anthropic) accept structured message arrays. Using `json.dumps()` ensures deterministic serialization without escape bugs.\n\n```python\nimport json\nmsg = {'role': 'user', 'content': 'Hello'}\nprint(json.dumps(msg))\n```",
                        "theory_te": "LLM API లతో పని చేసేటప్పుడు మెసేజ్‌లను JSON ఫార్మాట్‌లో పంపడం సర్వసాధారణం. పైథాన్‌లో `json.dumps()` దీని కోసం వాడతాము.",
                        "starterCode": "import json\n\nmessage = {\n    'role': 'user',\n    'content': 'Teach me Python'\n}\n\nprint(json.dumps(message))\n",
                        "expectedOutput": "{\"role\": \"user\", \"content\": \"Teach me Python\"}",
                        "testCases": [{"input": "", "expected": "{\"role\": \"user\", \"content\": \"Teach me Python\"}"}],
                        "hint": "Use json.dumps(message) to output the string.",
                        "hints_te": ["`json.dumps(message)` ని ప్రింట్ చేయండి."],
                        "language": "python",
                        "xp": 20
                    }
                ]
            },
            {
                "id": "ai-m02",
                "title": "Module 2: Agentic Tool Calling & Function Schemas",
                "desc": "Format external tools and runtime functions into LLM-compatible JSON schemas.",
                "lessons": [
                    {
                        "id": "ai-m02-l01-tools",
                        "title": "LLM Function Calling Schema",
                        "title_te": "AI ఏజెంట్ టూల్ కాలింగ్ స్కీమా",
                        "instructions": "Define a tool calling dictionary with function name `'run_code'`, serialize its name attribute to JSON using `json.dumps()`, and print it.",
                        "instructions_te": "`'run_code'` ఫంక్షన్ పేరుతో టూల్ స్కీమా రాసి, దాని పేరును JSON ద్వారా ప్రింట్ చేయండి.",
                        "theory_en": "Modern agentic systems expose APIs as structured JSON schemas to let LLMs invoke external execution environments.",
                        "theory_te": "LLM ఏజెంట్లు కోడ్ ఎగ్జిక్యూషన్ మరియు డేటాబేస్ టూల్స్‌ని పిలవడానికి JSON స్కీమా ఫార్మాట్ వాడతాయి.",
                        "starterCode": "import json\n\ntool = {\n    'name': 'run_code',\n    'description': 'Executes code in isolated sandbox'\n}\n\nprint(json.dumps(tool['name']))\n",
                        "expectedOutput": "\"run_code\"",
                        "testCases": [{"input": "", "expected": "\"run_code\""}],
                        "hint": "Print json.dumps(tool['name'])",
                        "hints_te": ["`print(json.dumps(tool['name']))` రాయండి."],
                        "language": "python",
                        "xp": 25
                    }
                ]
            }
        ]
    }
]

# Guarantee totalLessons perfectly matches the actual number of lessons in every track
for _j in JOURNEYS_DATA:
    _j["totalLessons"] = sum(len(_c.get("lessons", [])) for _c in _j.get("courses", []))


PRACTICE_PROBLEMS = [
    {
        "id": "prob-1",
        "title": "Reverse String",
        "title_te": "స్ట్రింగ్ రివర్స్ చేయండి (Reverse String)",
        "difficulty": "Easy",
        "category": "Strings",
        "language": "python",
        "description": "Write a function `reverse_string(s)` that takes a string `s` and returns it reversed.",
        "description_te": "ఒక స్ట్రింగ్ `s` ను తీసుకొని, దాన్ని తిరగరాసి (reversed) ఇచ్చే ఫంక్షన్ `reverse_string(s)` ను రాయండి.",
        "starterCode": "def reverse_string(s):\n    # Task: Write your solution here\n    pass\n\nprint(reverse_string(\"prasana\"))\n",
        "testCases": [
            {"input": "", "expected": "anasarp"},
            {"input": "", "expected": "nohtyp"},
            {"input": "", "expected": "olleh"}
        ],
        "hint": "Use Python string slicing `s[::-1]` or iterate backwards.",
        "hints_te": ["పైథాన్‌లో స్ట్రింగ్ స్లైసింగ్ `s[::-1]` ఉపయోగించవచ్చు లేదా లూప్ ద్వారా రివర్స్ చేయవచ్చు."]
    },
    {
        "id": "prob-2",
        "title": "FizzBuzz Challenge",
        "title_te": "ఫిజ్ బజ్ ఛాలెంజ్ (FizzBuzz Challenge)",
        "difficulty": "Easy",
        "category": "Algorithms",
        "language": "python",
        "description": "Print numbers 1 to N. For multiples of 3 print 'Fizz', for multiples of 5 print 'Buzz', and for multiples of both print 'FizzBuzz'.",
        "description_te": "1 నుండి N వరకు సంఖ్యలను ప్రింట్ చేయండి. 3 తో భాగించబడితే 'Fizz', 5 తో భాగించబడితే 'Buzz', మరియు రెండింటితో భాగించబడితే 'FizzBuzz' ప్రింట్ చేయండి.",
        "starterCode": "def fizz_buzz(n):\n    # Task: Your logic here\n    pass\n\nfizz_buzz(15)\n",
        "testCases": [
            {"input": "", "expected": "1\n2\nFizz\n4\nBuzz\nFizz\n7\n8\nFizz\nBuzz\n11\nFizz\n13\n14\nFizzBuzz"},
            {"input": "", "expected": "1\n2\nFizz"}
        ],
        "hint": "Check `i % 15 == 0` first, then `i % 3 == 0`, then `i % 5 == 0`.",
        "hints_te": ["మొదట `i % 15 == 0` కండిషన్ చెక్ చేయండి, ఆ తర్వాత `i % 3 == 0`, తర్వాత `i % 5 == 0` చెక్ చేయండి."]
    },
    {
        "id": "prob-3",
        "title": "Palindrome Checker",
        "title_te": "పాలిండ్రోమ్ నిర్ధారణ (Palindrome Checker)",
        "difficulty": "Easy",
        "category": "Strings",
        "language": "python",
        "description": "Write a function `is_palindrome(s)` that checks if a given string reads the same forwards and backwards. Return True or False.",
        "description_te": "ఇచ్చిన స్ట్రింగ్ ముందు నుండి వెనుకకు ఒకే విధంగా ఉందో లేదో (పాలిండ్రోమ్) చెక్ చేసి True లేదా False ఇచ్చే `is_palindrome(s)` రాయండి.",
        "starterCode": "def is_palindrome(s):\n    # Task: Check if s is equal to its reverse\n    pass\n\nprint(is_palindrome(\"racecar\"))\n",
        "testCases": [
            {"input": "", "expected": "True"}
        ],
        "hint": "Compare s.lower() with s.lower()[::-1]",
        "hints_te": ["`s.lower()` ని `s.lower()[::-1]` తో పోల్చి సమానమైతే True రిటర్న్ చేయండి."]
    },
    {
        "id": "prob-4",
        "title": "Find Maximum in Array",
        "title_te": "అర్రేలో గరిష్ట విలువ (Find Maximum in Array)",
        "difficulty": "Easy",
        "category": "Arrays",
        "language": "python",
        "description": "Write a function `find_max(nums)` that finds and returns the largest number in a list without using `max()`.",
        "description_te": "బిల్ట్-ఇన్ `max()` వాడకుండా ఒక లిస్ట్‌లో అతి పెద్ద సంఖ్యను కనుగొనే ఫంక్షన్ `find_max(nums)` రాయండి.",
        "starterCode": "def find_max(nums):\n    # Task: Find maximum element\n    pass\n\nprint(find_max([3, 14, 7, 25, 9]))\n",
        "testCases": [
            {"input": "", "expected": "25"}
        ],
        "hint": "Keep a variable `highest = nums[0]` and iterate through the list updating it.",
        "hints_te": ["`highest = nums[0]` గా తీసుకొని, లిస్ట్ గుండా లూప్ చేస్తూ పెద్ద విలువ వస్తే అప్‌డేట్ చేయండి."]
    },
    {
        "id": "prob-5",
        "title": "Sum of Even Numbers",
        "title_te": "సరి సంఖ్యల మొత్తం (Sum of Even Numbers)",
        "difficulty": "Easy",
        "category": "Math",
        "language": "python",
        "description": "Write a function `sum_of_evens(n)` that returns the sum of all positive even numbers up to and including `n`.",
        "description_te": "1 నుండి `n` వరకు గల అన్ని సరి సంఖ్యల (even numbers) మొత్తాన్ని లెక్కించే ఫంక్షన్ `sum_of_evens(n)` రాయండి.",
        "starterCode": "def sum_of_evens(n):\n    # Task: Calculate sum of evens\n    pass\n\nprint(sum_of_evens(10))\n",
        "testCases": [
            {"input": "", "expected": "30"}
        ],
        "hint": "Even numbers up to 10 are 2, 4, 6, 8, 10. Their sum is 30.",
        "hints_te": ["10 వరకు సరి సంఖ్యలు 2, 4, 6, 8, 10. వీటి మొత్తం 30 అవుతుంది. `range(2, n + 1, 2)` వాడవచ్చు."]
    },
    {
        "id": "prob-6",
        "title": "Count Vowels in String",
        "title_te": "అచ్చుల లెక్కింపు (Count Vowels in String)",
        "difficulty": "Easy",
        "category": "Strings",
        "language": "python",
        "description": "Write a function `count_vowels(s)` that counts how many vowels (a, e, i, o, u) appear in the input string (case-insensitive).",
        "description_te": "ఇచ్చిన స్ట్రింగ్‌లో ఎన్ని అచ్చులు (a, e, i, o, u) ఉన్నాయో లెక్కించే ఫంక్షన్ `count_vowels(s)` రాయండి.",
        "starterCode": "def count_vowels(s):\n    # Task: Count vowels\n    pass\n\nprint(count_vowels(\"Prasana Code AI\"))\n",
        "testCases": [
            {"input": "", "expected": "7"}
        ],
        "hint": "Check each character: `if char.lower() in 'aeiou': count += 1`",
        "hints_te": ["ప్రతి అక్షరాన్ని చెక్ చేయండి: `if char.lower() in 'aeiou': count += 1`"]
    },
    {
        "id": "prob-7",
        "title": "Factorial Calculator",
        "title_te": "ఫ్యాక్టోరియల్ లెక్కింపు (Factorial Calculator)",
        "difficulty": "Medium",
        "category": "Recursion",
        "language": "python",
        "description": "Write a function `factorial(n)` that returns the factorial of integer `n` (n!).",
        "description_te": "ఇచ్చిన పూర్ణాంకం `n` కు ఫ్యాక్టోరియల్ (n!) ను లెక్కించే ఫంక్షన్ `factorial(n)` రాయండి.",
        "starterCode": "def factorial(n):\n    # Task: Return n!\n    pass\n\nprint(factorial(5))\n",
        "testCases": [
            {"input": "", "expected": "120"}
        ],
        "hint": "Base case: if n <= 1 return 1, otherwise return n * factorial(n - 1).",
        "hints_te": ["బేస్ కేస్: `n <= 1` అయితే 1 రిటర్న్ చేయండి, లేకపోతే `n * factorial(n - 1)` రిటర్న్ చేయండి."]
    },
    {
        "id": "prob-8",
        "title": "Two Sum (DSA)",
        "title_te": "టూ సమ్ అల్గారిథమ్ (Two Sum DSA)",
        "difficulty": "Medium",
        "category": "Arrays",
        "language": "python",
        "description": "Given a list `nums` and a `target`, return the two indices whose values add up to `target`.",
        "description_te": "ఒక సంఖ్యల జాబితా `nums` మరియు `target` ఇచ్చినప్పుడు, వాటి మొత్తం target అయ్యే రెండు సూచికలను (indices) రిటర్న్ చేయండి.",
        "starterCode": "def two_sum(nums, target):\n    # Task: Return [index1, index2]\n    pass\n\nprint(two_sum([2, 7, 11, 15], 9))\n",
        "testCases": [
            {"input": "", "expected": "[0, 1]"}
        ],
        "hint": "Use a dictionary `seen = {}` mapping number to its index.",
        "hints_te": ["ఒక డిక్షనరీ `seen = {}` ఉపయోగించి, చూసిన నంబర్ మరియు దాని ఇండెక్స్‌ను స్టోర్ చేసుకుని O(n) లో పరిష్కరించవచ్చు."]
    },
    {
        "id": "prob-9",
        "title": "Array Filtering & Mapping",
        "title_te": "అర్రే ఫిల్టరింగ్ & మ్యాపింగ్ (Array Filter JS)",
        "difficulty": "Easy",
        "category": "Web Dev",
        "language": "javascript",
        "description": "Write a JavaScript function `doubleEvens(arr)` that filters even numbers and doubles them.",
        "description_te": "జావాస్క్రిప్ట్‌లో సరి సంఖ్యలను ఫిల్టర్ చేసి వాటిని రెట్టింపు చేసే ఫంక్షన్ `doubleEvens(arr)` రాయండి.",
        "starterCode": "function doubleEvens(arr) {\n    // Task: filter evens and multiply by 2\n    return arr.filter(x => x % 2 === 0).map(x => x * 2);\n}\n\nconsole.log(JSON.stringify(doubleEvens([1, 2, 3, 4, 5, 6])));\n",
        "testCases": [
            {"input": "", "expected": "[4,8,12]"}
        ],
        "hint": "Use `arr.filter(n => n % 2 === 0).map(n => n * 2)`.",
        "hints_te": ["జావాస్క్రిప్ట్ మెథడ్స్ `.filter()` మరియు `.map()` ఉపయోగించండి."]
    },
    {
        "id": "prob-10",
        "title": "Vector Elements Sum (C++)",
        "title_te": "వెక్టర్ ఎలిమెంట్స్ మొత్తం (Vector Sum C++)",
        "difficulty": "Medium",
        "category": "Systems",
        "language": "cpp",
        "description": "Write a C++ program that calculates and prints the sum of integers in a vector.",
        "description_te": "ఒక std::vector లోని సంఖ్యల మొత్తాన్ని లెక్కించి ప్రింట్ చేసే C++ ప్రోగ్రామ్ రాయండి.",
        "starterCode": "#include <iostream>\n#include <vector>\n#include <numeric>\n\nint main() {\n    std::vector<int> nums = {10, 20, 30, 40};\n    int sum = 0;\n    for (int n : nums) sum += n;\n    std::cout << sum << std::endl;\n    return 0;\n}\n",
        "testCases": [
            {"input": "", "expected": "100"}
        ],
        "hint": "Iterate with a range-based for loop `for (int n : nums) sum += n;`.",
        "hints_te": ["రేంజ్ బేస్డ్ ఫర్ లూప్ `for (int n : nums)` ఉపయోగించి సంకలనం చేయండి."]
    }
]
