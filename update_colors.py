import os
import re

replacements = {
    'bg-[#0b0f19]': 'bg-slate-950',
    'bg-[#0f172a]': 'bg-slate-900',
    'bg-[#161b22]': 'bg-slate-800',
    'bg-[#0d1117]': 'bg-slate-900',
    'bg-[#0b0f19]/90': 'bg-slate-950/90',
    'bg-[#0f172a]/90': 'bg-slate-900/90',
}

def process_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()
    
    new_content = content
    for old, new in replacements.items():
        new_content = new_content.replace(old, new)
        
    if new_content != content:
        with open(filepath, 'w') as f:
            f.write(new_content)
        print(f"Updated {filepath}")

for root, _, files in os.walk('frontend/src'):
    for file in files:
        if file.endswith(('.jsx', '.js')):
            process_file(os.path.join(root, file))
