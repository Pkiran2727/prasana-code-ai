import glob
import json
import os
import re
import sys

sys.path.insert(0, "tests")
import strict_validator


def words_outside_code(md):
    md = re.sub(r"```.*?```", " ", md, flags=re.S)
    md = "\n".join(l for l in md.splitlines() if not l.strip().startswith("|"))
    return len(re.findall(r"[A-Za-z0-9'`\-\.]+", md))


UPDATES = {
    "py-f-m01-l01-print.json": {
        "fixed_output": True,
        "en_body": (
            "Programming is fundamentally about giving clear, precise instructions to a digital computer to solve real-world problems. "
            "In Python, the first and most essential instruction you learn is the built-in `print()` function. It instructs the Python interpreter "
            "to display whatever data you pass directly onto your terminal screen or console window.\n\n"
            "Think of calling `print()` as writing an announcement on a clean whiteboard where every student in the room can see it clearly.\n\n"
            "```python\nprint(\"Hello, World!\")\n```\n\n"
            "When Python executes this line, the message appears instantly in your output area. Notice carefully that any text or string characters "
            "you wish to print must be wrapped inside matching quotation marks, using either double quotes or single quotes. If you omit the quotes, "
            "Python assumes the words are variable identifiers and will raise a syntax error. Practice running greetings to build confidence right now. "
            "Every software engineer starts their programming journey by printing helpful status messages to understand application flow."
        ),
        "hints_te": [
            "స్క్రీన్‌పై టెక్స్ట్‌ని చూపించడానికి print() ఫంక్షన్‌ని ఉపయోగించండి.",
            "print() లోపల ఉన్న టెక్స్ట్ తప్పనిసరిగా డబుల్ కోట్స్ లో ఉండాలి.",
            "ప్లాన్: print(\"Namaste, Python!\") అని మీ కోడ్‌లో రాయండి."
        ],
        "quiz_patch": {
            1: {
                "qtype": "predict_output",
                "prompt_md": "What prints?\n```python\nprint(\"123\")\n```",
                "code": "print(\"123\")",
                "answer": "123",
                "explanation_md": "Whatever is inside `print()` will be displayed on the screen."
            }
        }
    },
    "py-f-m01-l02-multiline.json": {
        "fixed_output": True,
        "en_body": (
            "In Python, you are never restricted to printing a single line of text. You can execute multiple `print()` statements in sequence, "
            "and Python will process each one in exact top-to-bottom order. By default, every call to `print()` automatically appends an invisible "
            "newline character at the end of its output, meaning the next statement prints on a fresh line below it.\n\n"
            "Imagine flipping to a brand-new page in a notebook every single time you jot down another thought or sentence.\n\n"
            "```python\nprint(\"Line 1\")\nprint(\"Line 2\")\n```\n\n"
            "When run, this produces two separate lines of text cleanly aligned in the terminal console. You can print multiple sentences, "
            "numbered lists, recipes, ASCII art shapes, or tabular figures simply by placing consecutive `print()` calls inside your Python source file. "
            "Mastering multiline output allows you to structure readable and informative reports for your users effortlessly. "
            "This structured presentation forms the core user experience of modern command-line developer tools and interactive terminal interfaces."
        ),
        "hints_te": [
            "రెండు వేర్వేరు లైన్లలో ప్రింట్ చేయడానికి రెండు print() స్టేట్‌మెంట్లు వాడండి.",
            "మొదటి print() లో Apple మరియు రెండవ print() లో Banana రాయండి.",
            "ప్లాన్: print(\"Apple\") తర్వాత print(\"Banana\") అని రాయండి."
        ],
        "quiz_patch": {
            0: {
                "qtype": "predict_output",
                "prompt_md": "What prints?\n```python\nprint(\"A\")\nprint(\"B\")\n```",
                "code": "print(\"A\")\nprint(\"B\")",
                "answer": "A\nB",
                "explanation_md": "Each print() prints on a new line."
            }
        }
    },
    "py-f-m01-l03-comments.json": {
        "fixed_output": True,
        "en_body": (
            "As your computer programs grow in complexity, writing notes to explain your thought process becomes incredibly valuable for yourself "
            "and your teammates. In Python, you can leave helpful human-readable notes called comments by prefixing any line with the hash character `#`. "
            "Whenever the Python interpreter encounters a `#` symbol, it completely disregards every single character on that line following it.\n\n"
            "Think of comments like handy yellow sticky notes attached to a formal legal contract; human readers find them illuminating, but the official legal logic ignores them entirely.\n\n"
            "```python\n# This is a helpful comment. Python ignores it.\nprint(\"Hello\") # Prints Hello\n```\n\n"
            "Comments are widely used in professional software engineering to document tricky algorithms, leave reminders, temporarily disable pieces of code during debugging sessions, "
            "and explain why specific implementation decisions were made in the codebase. Clear documentation ensures long-term software maintainability, "
            "allowing future contributors to comprehend legacy business requirements swiftly without tedious guesswork or accidental regression bugs."
        ),
        "hints_te": [
            "పైథాన్‌లో కామెంట్స్ ఎల్లప్పుడూ # గుర్తుతో మొదలవుతాయి.",
            "మొదటి లైన్‌లో # My first comment అని రాయండి.",
            "తర్వాత లైన్‌లో print(\"Python is fun!\") అని రాయండి."
        ],
        "quiz_patch": {
            1: {
                "qtype": "predict_output",
                "prompt_md": "What prints?\n```python\n# print(\"Hi\")\nprint(\"Bye\")\n```",
                "code": "# print(\"Hi\")\nprint(\"Bye\")",
                "answer": "Bye",
                "explanation_md": "The first line is commented out, so only Bye prints."
            }
        }
    },
    "py-f-m02-l01-variables.json": {
        "fixed_output": True,
        "en_body": (
            "In computer science and software development, a variable acts like a durable labeled storage container that holds data inside the computer's memory. "
            "To assign information to a variable in Python, you use the single equals sign `=`, which is known as the assignment operator. "
            "The descriptive variable name is always written on the left side, while the actual data value you want to store belongs on the right side.\n\n"
            "Think of sticking a neat printed label saying 'age' onto a cardboard storage box and placing the number twenty safely inside it.\n\n"
            "```python\nage = 20\nname = \"Prasana\"\nprint(age)\nprint(name)\n```\n\n"
            "Once a variable has been defined, you can reference it anywhere in your code, pass it to functions like `print()`, or update its stored value "
            "as your program executes its business logic. Descriptive variable names make your code expressive and maintainable. "
            "Choosing intuitive identifiers helps other programmers immediately recognize what kind of information each container holds during runtime execution."
        ),
        "hints_te": [
            "వేరియబుల్ పేరు ఎడమ వైపున, దాని విలువ కుడి వైపున రాయండి.",
            "సిటీ కోసం: city = \"Hyderabad\" అని డిక్లేర్ చేయండి.",
            "చివరగా ఆ వేరియబుల్‌ని print(city) ద్వారా ప్రింట్ చేయండి."
        ],
        "quiz_patch": {
            1: {
                "qtype": "predict_output",
                "prompt_md": "What prints?\n```python\nx = \"Apple\"\nprint(\"x\")\n```",
                "code": "x = \"Apple\"\nprint(\"x\")",
                "answer": "x",
                "explanation_md": "Because \"x\" is inside quotes, the letter x prints, not Apple."
            }
        }
    },
    "py-f-m02-l02-numbers.json": {
        "fixed_output": True,
        "en_body": (
            "Python is widely admired for its exceptional mathematical computation capabilities and clean numeric syntax. "
            "At its core, Python categorizes numbers into two primary data types: integers `int` and floating-point numbers `float`. "
            "Integers represent whole numbers with zero fractional part, such as ten, negative five, or zero. In contrast, floats represent decimal numbers like three point one four.\n\n"
            "You can execute standard arithmetic operations seamlessly using familiar mathematical operator symbols: addition `+`, subtraction `-`, multiplication `*`, and division `/`.\n\n"
            "```python\nx = 10\ny = 3\nprint(x + y) # 13\nprint(x / y) # 3.3333333333333335\n```\n\n"
            "Notice that dividing two integers using `/` in Python always produces a floating-point result, preserving exact mathematical precision. "
            "You can combine multiple mathematical operations in complex expressions, adhering to standard algebraic operator precedence rules. "
            "These fundamental numeric types empower engineers to perform financial accounting, game physics, scientific analytics, and high-frequency algorithms accurately."
        ),
        "hints_te": [
            "రెండు సంఖ్యలను గుణించడానికి * గుర్తును ఉపయోగించండి.",
            "మల్టిప్లికేషన్ కోసం: result = a * b అని రాయండి.",
            "ప్లాన్: print(result) అని రాసి రన్ చేయండి."
        ],
        "quiz_patch": {
            1: {
                "qtype": "predict_output",
                "prompt_md": "What prints?\n```python\nprint(5 * 2)\n```",
                "code": "print(5 * 2)",
                "answer": "10",
                "explanation_md": "5 multiplied by 2 equals 10."
            }
        }
    },
    "py-f-m02-l03-input.json": {
        "fixed_output": False,
        "en_body": (
            "Real-world computer applications are inherently interactive; they respond dynamically to information provided by real human users. "
            "In Python, you prompt and accept user data from the terminal console using the built-in `input()` function. "
            "Whenever Python encounters `input()`, it temporarily pauses script execution, waits patiently for the user to type on their keyboard, "
            "and resumes once they press the Enter key.\n\n"
            "Think of `input()` as handing a microphone to someone in the audience and waiting for them to say their answer.\n\n"
            "```python\nname = input()\nprint(\"Hello\")\nprint(name)\n```\n\n"
            "A critical concept to remember is that `input()` always captures and returns the user's typed data as a string data type, "
            "even if the person typed numeric digits like forty-two. You can store this incoming text directly into variables and process it throughout your application. "
            "By capturing user intent through input streams, your applications can deliver personalized feedback, process online orders, and build interactive dialogs."
        ),
        "hints_te": [
            "యూజర్ నుంచి ఇన్‌పుట్ తీసుకోవడానికి input() ఫంక్షన్ వాడండి.",
            "కలర్ కోసం: color = input() అని అసైన్ చేయండి.",
            "చివరగా స్క్రీన్‌పై చూపించడానికి print(color) అని రాయండి."
        ],
        "quiz_patch": {
            1: {
                "qtype": "predict_output",
                "prompt_md": "If user types `5`, what prints?\n```python\nx = input()\nprint(x)\n```",
                "code": "x = input()\nprint(x)",
                "stdin": "5\n",
                "answer": "5",
                "explanation_md": "input() captures what user typed, and print(x) prints 5."
            }
        }
    },
    "py-f-m03-l01-concat.json": {
        "fixed_output": False,
        "en_body": (
            "In computer programming, combining multiple separate pieces of text into a cohesive sentence is one of the most frequent operations you will perform. "
            "In Python, joining two or more strings together end-to-end is formally known as string concatenation, and it is accomplished using the plus operator `+`.\n\n"
            "Think of string concatenation as taking two separate strips of paper and gluing their ends together securely into one continuous paper strip.\n\n"
            "```python\nword1 = \"Hello\"\nword2 = \"World\"\nprint(word1 + word2)       # HelloWorld\nprint(word1 + \" \" + word2) # Hello World\n```\n\n"
            "Notice that concatenation does not automatically insert spaces between words for you; you must explicitly provide any necessary space characters "
            "inside your string literals. Concatenation is strictly designed for strings; combining a string directly with a raw integer number requires type conversion. "
            "Mastering concatenation gives you full creative freedom to assemble customized greetings, build dynamic database queries, and display formatted messages."
        ),
        "hints_te": [
            "మూడు స్ట్రింగ్స్‌ని కలపడానికి + ఆపరేటర్ వాడండి.",
            "స్పేస్ మిస్ అవ్వకుండా \"Namaste, \" అని రాయండి.",
            "ప్లాన్: print(\"Namaste, \" + name + \"!\") అని రాయండి."
        ],
        "quiz_patch": {
            0: {
                "qtype": "predict_output",
                "prompt_md": "What prints?\n```python\nprint(\"A\" + \"B\")\n```",
                "code": "print(\"A\" + \"B\")",
                "answer": "AB",
                "explanation_md": "String concatenation merges A and B together into AB."
            },
            1: {
                "qtype": "predict_output",
                "prompt_md": "If user types `5`, what prints?\n```python\nx = input()\nprint(x + x)\n```",
                "code": "x = input()\nprint(x + x)",
                "stdin": "5\n",
                "answer": "55",
                "explanation_md": "input() returns a string, so '5' + '5' concatenates into '55'."
            }
        }
    },
    "py-f-m03-l02-fstrings.json": {
        "fixed_output": False,
        "en_body": (
            "While the plus operator works for simple concatenation, assembling complex sentences with numerous variables and numbers quickly becomes messy and error-prone. "
            "To solve this problem elegantly, modern Python introduced formatted string literals, affectionately known as f-strings. "
            "To construct an f-string, you simply place the letter `f` immediately before the opening quotation mark of your string literal.\n\n"
            "Inside an f-string, any variable name or Python expression wrapped in curly braces `{}` is automatically evaluated and converted to readable text.\n\n"
            "```python\nname = \"Prasana\"\nage = 20\n# Clean f-string:\nprint(f\"My name is {name} and I am {age}\")\n```\n\n"
            "F-strings are significantly faster, vastly more readable, and reduce punctuation clutter. Professional Python developers rely heavily on f-strings "
            "for creating logs, formatted output tables, and user notifications throughout production applications. "
            "Adopting f-strings elevates code readability and adheres to clean programming practices advocated across modern Python development teams worldwide."
        ),
        "hints_te": [
            "కొటేషన్ల ముందు చిన్న అక్షరం f ని ఉంచండి.",
            "వేరియబుల్స్ ని కర్లీ బ్రేసెస్ {} లోపల రాయాలి.",
            "ప్లాన్: f\"The weather in {city} is {weather}.\" అని రాయండి."
        ],
        "quiz_patch": {
            1: {
                "qtype": "predict_output",
                "prompt_md": "What prints?\n```python\nitem = \"Car\"\nprint(\"I bought a {item}\")\n```",
                "code": "item = \"Car\"\nprint(\"I bought a {item}\")",
                "answer": "I bought a {item}",
                "explanation_md": "Without the 'f' prefix, {item} is treated literally."
            }
        }
    },
    "py-f-m03-l03-indexing.json": {
        "fixed_output": False,
        "en_body": (
            "Strings in Python are ordered sequences of individual characters. Every character in a string occupies a specific numerical slot known as its index. "
            "In Python, as in most contemporary programming languages, indexing starts at zero rather than one. "
            "Therefore, the very first character of any string is located at index zero, the second character sits at index one, and so on.\n\n"
            "You extract an individual character from a string by appending square brackets `[]` containing the desired index number to your variable name.\n\n"
            "```python\nword = \"PYTHON\"\nprint(word[0]) # Prints P\nprint(word[2]) # Prints T\n```\n\n"
            "Python also supports negative indexing, allowing you to access characters from the end of the string backward, where negative one refers to the final character. "
            "Understanding zero-based indexing is foundational for traversing strings, lists, arrays, and complex data structures. "
            "By targeting precise positions within strings, you can parse encoded file formats, extract initials, and inspect specific symbols effortlessly."
        ),
        "hints_te": [
            "పైథాన్‌లో ఇండెక్సింగ్ ఎల్లప్పుడూ 0 తో ప్రారంభమవుతుంది.",
            "రెండవ అక్షరం కోసం ఇండెక్స్ 1 ని వాడాలి.",
            "ప్లాన్: word[1] ని print() లోపల ఉంచి ప్రింట్ చేయండి."
        ],
        "quiz_patch": {
            0: {
                "qtype": "predict_output",
                "prompt_md": "What prints?\n```python\nword = \"CODE\"\nprint(word[3])\n```",
                "code": "word = \"CODE\"\nprint(word[3])",
                "answer": "E",
                "explanation_md": "C is at 0, O is at 1, D is at 2, and E is at index 3."
            }
        }
    },
    "py-f-m03-l04-slicing.json": {
        "fixed_output": False,
        "en_body": (
            "While indexing allows you to pick a single character from a string, you often need to extract a whole portion or substring. "
            "In Python, this versatile technique is called string slicing. Slicing uses the syntax `string[start:end]`, where Python extracts all characters "
            "beginning at the `start` index and continues up to, but crucially not including, the `end` index position.\n\n"
            "Think of using a kitchen knife to cut a precise slice out of a loaf of sandwich bread between two measurement marks.\n\n"
            "```python\nword = \"PYTHON\"\nprint(word[0:2]) # PY\nprint(word[2:5]) # THO\n```\n\n"
            "Because the end index is exclusive, `[0:3]` gives you exactly three characters: positions zero, one, and two. "
            "If you omit the start index, Python defaults to the beginning of the string; if you omit the end index, it slices through the very end. "
            "Slicing empowers programmers to truncate long headlines, extract domain names from email addresses, and isolate relevant tokens seamlessly."
        ),
        "hints_te": [
            "మొదటి 3 అక్షరాల కోసం 0 నుంచి 3 వరకు స్లైస్ చేయండి.",
            "స్లైసింగ్‌లో ఎండ్ ఇండెక్స్ చేర్చబడదు, కాబట్టి [0:3] వాడాలి.",
            "ప్లాన్: print(text[0:3]) అని మీ కోడ్‌లో రాయండి."
        ],
        "quiz_patch": {
            0: {
                "qtype": "predict_output",
                "prompt_md": "What prints?\n```python\nword = \"BANANA\"\nprint(word[0:4])\n```",
                "code": "word = \"BANANA\"\nprint(word[0:4])",
                "answer": "BANA",
                "explanation_md": "word[0:4] extracts characters at indices 0, 1, 2, and 3, which is BANA."
            }
        }
    }
}


def apply_updates():
    for filename, patch in UPDATES.items():
        found = False
        for path in glob.glob(f"content/**/{filename}", recursive=True):
            found = True
            d = json.load(open(path, encoding="utf-8"))
            ch = d["challenge"]

            # Fixed output setting
            ch["fixed_output"] = patch["fixed_output"]
            if patch["fixed_output"]:
                sol_code = ch["solution_code"]
                res = strict_validator.run_code(sol_code, "", 3000, ch["language"])
                exp = strict_validator.norm(res["stdout"])
                ch["tests"] = [{"stdin": "", "expected": exp, "hidden": False}]

            # Update body_md
            d["content"]["en"]["body_md"] = patch["en_body"]
            wc = words_outside_code(patch["en_body"])
            print(f"{filename}: updated word count = {wc}")

            # Update Telugu hints
            ch["hints_te"] = patch["hints_te"]

            # Patch quiz questions
            for q_idx, q_data in patch.get("quiz_patch", {}).items():
                d["quiz"][q_idx].update(q_data)

            # Save file
            json.dump(d, open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
            print(f"Saved {path}")

            # Validate
            errs = strict_validator.validate(path)
            if errs:
                print(f"  VALIDATOR ERRORS in {filename}:", errs)
            else:
                print(f"  ALL CHECKS PASSED for {filename}!")


if __name__ == "__main__":
    apply_updates()
