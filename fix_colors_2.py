import os
import re

replacements = {
    'text-white': 'text-ide-text',
    'bg-gray-950': 'bg-ide-bg',
    'bg-gray-900': 'bg-ide-panel',
    'bg-gray-800': 'bg-ide-sidebar',
    'border-gray-800': 'border-ide-border',
    'border-gray-700': 'border-ide-border',
    'text-gray-200': 'text-ide-text',
    'text-gray-300': 'text-ide-text',
    'text-gray-400': 'text-ide-muted',
    'text-gray-500': 'text-ide-muted',
    'hover:text-white': 'hover:text-ide-text',
    'hover:bg-gray-800': 'hover:bg-ide-sidebar',
    'hover:bg-gray-900': 'hover:bg-ide-panel',
}

def process_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()
    
    new_content = content
    for old, new in replacements.items():
        # Only replace exact class words, but simple string replace is safer if we just watch out.
        # Actually standard string replace is fine for these specific Tailwind classes.
        new_content = new_content.replace(old, new)
        
    if new_content != content:
        with open(filepath, 'w') as f:
            f.write(new_content)
        print(f"Updated {filepath}")

for root, _, files in os.walk('frontend/src'):
    for file in files:
        if file.endswith(('.jsx', '.js')):
            process_file(os.path.join(root, file))
