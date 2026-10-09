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
        "m01-first-steps": {"id": "py-m01", "title": "Module 1: First Steps with Python", "lessons": []},
        "m02-variables-types": {"id": "py-m02", "title": "Module 2: Variables & Data Types", "lessons": []},
        "m03-strings": {"id": "py-m03", "title": "Module 3: Working with Strings", "lessons": []}
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

                lesson_entry = {
                    "id": d["slug"],
                    "title": d["content"]["en"]["title"],
                    "title_te": d.get("content", {}).get("te", {}).get("title", ""),
                    "instructions": ch.get("instructions_md", ""),
                    "theory_en": d.get("content", {}).get("en", {}).get("body_md", ""),
                    "theory_te": d.get("content", {}).get("te", {}).get("body_md", ""),
                    "starterCode": ch.get("starter_code", ""),
                    "expectedOutput": test_cases[0]["expected"] if test_cases else "",
                    "testCases": test_cases,
                    "hint": ch.get("hints", ["Review the concept notes."])[0],
                    "hints": ch.get("hints", []),
                    "language": "python",
                    "xp": d.get("xp", 10),
                    "difficulty": d.get("difficulty", 1)
                }
                modules[mod_key]["lessons"].append(lesson_entry)
        except Exception as e:
            print(f"Error loading lesson file {f}: {e}")

    return [m for m in modules.values() if m["lessons"]]

# Load foundations dynamically or fallback
python_foundation_modules = _load_python_foundations()

JOURNEYS_DATA = [
    {
        "id": "python-developer",
        "title": "Python Developer Journey",
        "category": "Python",
        "icon": "🐍",
        "badge": "Popular",
        "description": "Master Python from syntax fundamentals to Object-Oriented Programming, Data Analysis, and Automation.",
        "totalLessons": sum(len(m["lessons"]) for m in python_foundation_modules) if python_foundation_modules else 10,
        "estimatedHours": 12,
        "courses": python_foundation_modules if python_foundation_modules else [
            {
                "id": "py-m01",
                "title": "Module 1: First Steps with Python",
                "lessons": [
                    {
                        "id": "py-f-m01-l01-print",
                        "title": "Your First Python Code",
                        "title_te": "మీ మొదటి పైథాన్ కోడ్",
                        "instructions": "Use the `print()` function to display exactly `Namaste, Python!` on the screen.",
                        "theory_en": "Programming is giving instructions to a computer. In Python, `print()` outputs text to the screen.",
                        "theory_te": "ప్రోగ్రామింగ్ అంటే కంప్యూటర్‌కు సూచనలు ఇవ్వడం. Python లో `print()` టెక్స్ట్‌ను స్క్రీన్‌పై చూపిస్తుంది.",
                        "starterCode": "# Task: Print Namaste, Python!\n",
                        "expectedOutput": "Namaste, Python!",
                        "testCases": [{"input": "", "expected": "Namaste, Python!"}],
                        "hint": "Use print(\"Namaste, Python!\") to display the text.",
                        "language": "python",
                        "xp": 10
                    }
                ]
            }
        ]
    },
    {
        "id": "web-development",
        "title": "Full-Stack Web Development Journey",
        "category": "Web Dev",
        "icon": "🌐",
        "badge": "Hot",
        "description": "Build modern responsive websites and interactive web apps using HTML, CSS, JavaScript, React, and Node.js.",
        "totalLessons": 20,
        "estimatedHours": 18,
        "courses": [
            {
                "id": "js-101",
                "title": "JavaScript Fundamentals & ES6",
                "lessons": [
                    {
                        "id": "js-l1",
                        "title": "Functions & Arrow Syntax",
                        "instructions": "Create a JavaScript function `greetUser(name)` that returns `'Welcome to Prasana Code AI, ' + name`.",
                        "starterCode": "// Task: Create greetUser function\nconst greetUser = (name) => {\n  // Your code here\n};\n\nconsole.log(greetUser('Prasana'));\n",
                        "expectedOutput": "Welcome to Prasana Code AI, Prasana",
                        "testCases": [
                            {"input": "", "expected": "Welcome to Prasana Code AI, Prasana"}
                        ],
                        "hint": "Use template literals: `return `Welcome to Prasana Code AI, ${name}`;`",
                        "language": "javascript",
                        "xp": 10
                    },
                    {
                        "id": "js-l2",
                        "title": "Array Filtering & Mapping",
                        "instructions": "Write code to filter an array of numbers `[1, 2, 3, 4, 5, 6]` to keep only even numbers, then print the result.",
                        "starterCode": "const nums = [1, 2, 3, 4, 5, 6];\n// Task: filter even numbers and print\n",
                        "expectedOutput": "[ 2, 4, 6 ]",
                        "testCases": [
                            {"input": "", "expected": "[ 2, 4, 6 ]"}
                        ],
                        "hint": "Use nums.filter(n => n % 2 === 0)",
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
        "description": "Crack technical interviews with comprehensive coverage of Arrays, Two Pointers, Trees, Graphs, and Dynamic Programming.",
        "totalLessons": 25,
        "estimatedHours": 20,
        "courses": [
            {
                "id": "dsa-101",
                "title": "Arrays & Hashing",
                "lessons": [
                    {
                        "id": "dsa-l1",
                        "title": "Two Sum Problem",
                        "instructions": "Given an array of numbers `nums` and a target integer `target`, return the two indices that sum up to `target`.",
                        "starterCode": "def two_sum(nums, target):\n    # Task: Write efficient hash map logic here\n    pass\n\nprint(two_sum([2, 7, 11, 15], 9))\n",
                        "expectedOutput": "[0, 1]",
                        "testCases": [
                            {"input": "", "expected": "[0, 1]"}
                        ],
                        "hint": "Use a dictionary to store element indices as you iterate through the list.",
                        "language": "python",
                        "xp": 20
                    },
                    {
                        "id": "dsa-l2",
                        "title": "Valid Parentheses",
                        "instructions": "Given a string `s` containing just characters '(', ')', '{', '}', '[' and ']', return True if the input string is valid.",
                        "starterCode": "def is_valid(s):\n    # Task: Use a stack to check balanced brackets\n    pass\n\nprint(is_valid(\"()[]{}\"))\n",
                        "expectedOutput": "True",
                        "testCases": [
                            {"input": "", "expected": "True"}
                        ],
                        "hint": "Use a stack list and a dictionary mapping closing brackets to opening brackets.",
                        "language": "python",
                        "xp": 20
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
        "badge": "High Performance",
        "description": "Master low-level programming, memory management, pointers, and high-performance Standard Template Library (STL).",
        "totalLessons": 18,
        "estimatedHours": 16,
        "courses": [
            {
                "id": "cpp-101",
                "title": "C++ Syntax & Fundamentals",
                "lessons": [
                    {
                        "id": "cpp-l1",
                        "title": "Hello World in C++",
                        "instructions": "Print `'Prasana Code AI C++ Sandbox'` using `std::cout`.",
                        "starterCode": "#include <iostream>\n\nint main() {\n    // Task: Print message here\n    \n    return 0;\n}\n",
                        "expectedOutput": "Prasana Code AI C++ Sandbox",
                        "testCases": [
                            {"input": "", "expected": "Prasana Code AI C++ Sandbox"}
                        ],
                        "hint": "Use std::cout << \"Prasana Code AI C++ Sandbox\" << std::endl;",
                        "language": "cpp",
                        "xp": 10
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
        "badge": "New",
        "description": "Learn to integrate OpenAI/Gemini LLMs, construct AI autonomous agents, fine-tune prompts, and build AI SaaS apps.",
        "totalLessons": 15,
        "estimatedHours": 12,
        "courses": [
            {
                "id": "ai-101",
                "title": "Prompt Engineering Essentials",
                "lessons": [
                    {
                        "id": "ai-l1",
                        "title": "Structured JSON Prompting",
                        "instructions": "Write a Python script that formats a prompt dictionary into a clean JSON string ready for LLM API calls.",
                        "starterCode": "import json\n\nprompt_data = {\n    \"role\": \"system\",\n    \"content\": \"You are Prasana AI Tutor.\"\n}\n\n# Task: Convert prompt_data to json string\njson_str = \"\"\nprint(json_str)\n",
                        "expectedOutput": "{\"role\": \"system\", \"content\": \"You are Prasana AI Tutor.\"}",
                        "testCases": [
                            {"input": "", "expected": "{\"role\": \"system\", \"content\": \"You are Prasana AI Tutor.\"}"}
                        ],
                        "hint": "Use `json.dumps(prompt_data)` to serialize the dictionary.",
                        "language": "python",
                        "xp": 15
                    }
                ]
            }
        ]
    }
]

PRACTICE_PROBLEMS = [
    {
        "id": "prob-1",
        "title": "Reverse String",
        "difficulty": "Easy",
        "category": "Strings",
        "language": "python",
        "description": "Write a function `reverse_string(s)` that takes a string `s` and returns it reversed.",
        "starterCode": "def reverse_string(s):\n    # Task: Write your solution here\n    pass\n\nprint(reverse_string(\"prasana\"))\n",
        "testCases": [
            {"input": "", "expected": "anasarp"},
            {"input": "", "expected": "nohtyp"},
            {"input": "", "expected": "olleh"}
        ],
        "hint": "Use Python string slicing `s[::-1]` or iterate backwards."
    },
    {
        "id": "prob-2",
        "title": "FizzBuzz Challenge",
        "difficulty": "Easy",
        "category": "Algorithms",
        "language": "python",
        "description": "Print numbers 1 to N. For multiples of 3 print 'Fizz', for multiples of 5 print 'Buzz', and for multiples of both print 'FizzBuzz'.",
        "starterCode": "def fizz_buzz(n):\n    # Task: Your logic here\n    pass\n\nfizz_buzz(15)\n",
        "testCases": [
            {"input": "", "expected": "1\n2\nFizz\n4\nBuzz\nFizz\n7\n8\nFizz\nBuzz\n11\nFizz\n13\n14\nFizzBuzz"},
            {"input": "", "expected": "1\n2\nFizz"}
        ],
        "hint": "Check `i % 15 == 0` first, then `i % 3 == 0`, then `i % 5 == 0`."
    },
    {
        "id": "prob-3",
        "title": "Palindrome Checker",
        "difficulty": "Easy",
        "category": "Strings",
        "language": "python",
        "description": "Write a function `is_palindrome(s)` that checks if a given string reads the same forwards and backwards. Return True or False.",
        "starterCode": "def is_palindrome(s):\n    # Task: Check if s is equal to its reverse\n    pass\n\nprint(is_palindrome(\"racecar\"))\n",
        "testCases": [
            {"input": "", "expected": "True"}
        ],
        "hint": "Compare s.lower() with s.lower()[::-1]"
    },
    {
        "id": "prob-4",
        "title": "Find Maximum in Array",
        "difficulty": "Easy",
        "category": "Arrays",
        "language": "python",
        "description": "Write a function `find_max(nums)` that finds and returns the largest number in a list without using `max()`.",
        "starterCode": "def find_max(nums):\n    # Task: Find maximum element\n    pass\n\nprint(find_max([3, 14, 7, 25, 9]))\n",
        "testCases": [
            {"input": "", "expected": "25"}
        ],
        "hint": "Keep a variable `highest = nums[0]` and iterate through the list updating it."
    },
    {
        "id": "prob-5",
        "title": "Sum of Even Numbers",
        "difficulty": "Easy",
        "category": "Math",
        "language": "python",
        "description": "Write a function `sum_of_evens(n)` that returns the sum of all positive even numbers up to and including `n`.",
        "starterCode": "def sum_of_evens(n):\n    # Task: Calculate sum of evens\n    pass\n\nprint(sum_of_evens(10))\n",
        "testCases": [
            {"input": "", "expected": "30"}
        ],
        "hint": "Even numbers up to 10 are 2, 4, 6, 8, 10. Their sum is 30."
    },
    {
        "id": "prob-6",
        "title": "Count Vowels in String",
        "difficulty": "Easy",
        "category": "Strings",
        "language": "python",
        "description": "Write a function `count_vowels(s)` that counts how many vowels (a, e, i, o, u) appear in the input string (case-insensitive).",
        "starterCode": "def count_vowels(s):\n    # Task: Count vowels\n    pass\n\nprint(count_vowels(\"Prasana Code AI\"))\n",
        "testCases": [
            {"input": "", "expected": "7"}
        ],
        "hint": "Check each character: `if char.lower() in 'aeiou': count += 1`"
    },
    {
        "id": "prob-7",
        "title": "Factorial Calculator",
        "difficulty": "Medium",
        "category": "Recursion",
        "language": "python",
        "description": "Write a function `factorial(n)` that returns the factorial of integer `n` (n!).",
        "starterCode": "def factorial(n):\n    # Task: Return n!\n    pass\n\nprint(factorial(5))\n",
        "testCases": [
            {"input": "", "expected": "120"}
        ],
        "hint": "Base case: if n <= 1 return 1, otherwise return n * factorial(n - 1)."
    },
    {
        "id": "prob-8",
        "title": "Two Sum (DSA)",
        "difficulty": "Medium",
        "category": "Arrays",
        "language": "python",
        "description": "Given a list `nums` and a `target`, return the two indices whose values add up to `target`.",
        "starterCode": "def two_sum(nums, target):\n    # Task: Return [index1, index2]\n    pass\n\nprint(two_sum([2, 7, 11, 15], 9))\n",
        "testCases": [
            {"input": "", "expected": "[0, 1]"}
        ],
        "hint": "Use a dictionary `seen = {}` mapping number to its index."
    }
]
