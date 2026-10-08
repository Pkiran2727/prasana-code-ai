import os

replacements = {
    'bg-slate-950': 'bg-ide-bg',
    'bg-slate-900': 'bg-ide-panel',
    'bg-slate-800': 'bg-ide-sidebar',
    'text-slate-100': 'text-ide-text',
    'text-slate-400': 'text-ide-muted',
    'text-slate-200': 'text-ide-text',
    'text-slate-300': 'text-ide-text',
    'border-slate-800': 'border-ide-border',
    'border-slate-700': 'border-ide-border',
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
