"""
Curriculum & Problem Bank Data for Prasana Code AI
Contains prefilled structured courses, lessons, and practice problems with test cases.
"""

JOURNEYS_DATA = [
    {
        "id": "python-developer",
        "title": "Python Developer Journey",
        "category": "Python",
        "icon": "🐍",
        "badge": "Popular",
        "description": "Master Python from syntax fundamentals to Object-Oriented Programming, Data Analysis, and Automation.",
        "totalLessons": 24,
        "estimatedHours": 15,
        "courses": [
            {
                "id": "py-101",
                "title": "Python Essentials & Data Types",
                "lessons": [
                    {
                        "id": "py-l1",
                        "title": "Your First Python Code & Variables",
                        "instructions": "Welcome to Python! In Python, you can print text using `print()`. Your task is to declare a variable `user_name` with value `'Prasana'` and print `'Hello, Prasana!'`.",
                        "starterCode": "# Write your code below\nuser_name = \"Prasana\"\n# Print 'Hello, Prasana!' using user_name\n",
                        "expectedOutput": "Hello, Prasana!\n",
                        "hint": "Use print(f'Hello, {user_name}!') or print('Hello, ' + user_name + '!')"
                    },
                    {
                        "id": "py-l2",
                        "title": "Conditionals & If-Else Statements",
                        "instructions": "Write a Python script that checks if a variable `score` is greater than or equal to 50. If true, print `'PASS'`, otherwise print `'FAIL'`.",
                        "starterCode": "score = 75\n# Add if-else logic here\n",
                        "expectedOutput": "PASS\n",
                        "hint": "Check with `if score >= 50:` then `print('PASS')` else `print('FAIL')`"
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
        "totalLessons": 30,
        "estimatedHours": 20,
        "courses": [
            {
                "id": "js-101",
                "title": "JavaScript Fundamentals & ES6",
                "lessons": [
                    {
                        "id": "js-l1",
                        "title": "Functions & Arrow Syntax",
                        "instructions": "Create a JavaScript function `greetUser(name)` that returns `'Welcome to Prasana Code AI, ' + name`.",
                        "starterCode": "// Create greetUser function\nconst greetUser = (name) => {\n  // Your code here\n};\n\nconsole.log(greetUser('Prasana'));\n",
                        "expectedOutput": "Welcome to Prasana Code AI, Prasana\n",
                        "hint": "Use template literals: `return \\`Welcome to Prasana Code AI, ${name}\\`;`"
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
        "totalLessons": 40,
        "estimatedHours": 25,
        "courses": [
            {
                "id": "dsa-101",
                "title": "Arrays & Hashing",
                "lessons": [
                    {
                        "id": "dsa-l1",
                        "title": "Two Sum Problem",
                        "instructions": "Given an array of numbers `nums` and a target integer `target`, return the two numbers that sum up to `target`.",
                        "starterCode": "def two_sum(nums, target):\n    # Write efficient hash map logic here\n    seen = {}\n    for i, num in enumerate(nums):\n        diff = target - num\n        if diff in seen:\n            return [seen[diff], i]\n        seen[num] = i\n    return []\n\nprint(two_sum([2, 7, 11, 15], 9))\n",
                        "expectedOutput": "[0, 1]\n",
                        "hint": "Use a dictionary to store element indices as you iterate through the list."
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
        "totalLessons": 20,
        "estimatedHours": 18,
        "courses": [
            {
                "id": "cpp-101",
                "title": "C++ Syntax & Pointers",
                "lessons": [
                    {
                        "id": "cpp-l1",
                        "title": "Hello World in C++",
                        "instructions": "Print `'Prasana Code AI C++ Sandbox'` using `std::cout`.",
                        "starterCode": "#include <iostream>\n\nint main() {\n    // Print message here\n    std::cout << \"Prasana Code AI C++ Sandbox\" << std::endl;\n    return 0;\n}\n",
                        "expectedOutput": "Prasana Code AI C++ Sandbox\n",
                        "hint": "Use std::cout << \"text\" << std::endl;"
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
        "totalLessons": 18,
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
                        "starterCode": "import json\n\nprompt_data = {\n    \"role\": \"system\",\n    \"content\": \"You are Prasana AI Tutor.\"\n}\n\n# Convert prompt_data to json string\njson_str = json.dumps(prompt_data)\nprint(json_str)\n",
                        "expectedOutput": "{\"role\": \"system\", \"content\": \"You are Prasana AI Tutor.\"}\n",
                        "hint": "Use `json.dumps(prompt_data)` to serialize the dictionary."
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
        "starterCode": "def reverse_string(s):\n    # Write your solution here\n    return s[::-1]\n\nprint(reverse_string(\"prasana\"))\n",
        "testCases": [
            {"input": "prasana", "expected": "anasarp\n"},
            {"input": "python", "expected": "nohtyp\n"}
        ]
    },
    {
        "id": "prob-2",
        "title": "FizzBuzz Challenge",
        "difficulty": "Easy",
        "category": "Algorithms",
        "language": "python",
        "description": "Print numbers 1 to N. For multiples of 3 print 'Fizz', for multiples of 5 print 'Buzz', and for multiples of both print 'FizzBuzz'.",
        "starterCode": "def fizz_buzz(n):\n    for i in range(1, n + 1):\n        if i % 3 == 0 and i % 5 == 0:\n            print(\"FizzBuzz\")\n        elif i % 3 == 0:\n            print(\"Fizz\")\n        elif i % 5 == 0:\n            print(\"Buzz\")\n        else:\n            print(i)\n\nfizz_buzz(15)\n",
        "testCases": [
            {"input": "15", "expected": "1\n2\nFizz\n4\nBuzz\nFizz\n7\n8\nFizz\nBuzz\n11\nFizz\n13\n14\nFizzBuzz\n"}
        ]
    }
]
