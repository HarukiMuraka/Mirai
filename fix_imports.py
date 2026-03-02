"""
Script de Correção Automática de Imports
"""

from pathlib import Path
import re

def fix_imports_in_file(filepath):
    """Corrige imports em um arquivo"""
    print(f"Corrigindo: {filepath}")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # Substituições (ordem importa!)
    replacements = [
        # Imports relativos para absolutos
        (r'from core\.', 'from mirai.core.'),
        (r'from actions\.', 'from mirai.actions.'),
        (r'from modes\.', 'from mirai.modes.'),
        (r'from interface\.', 'from mirai.interface.'),
        (r'from perception\.', 'from mirai.perception.'),
        (r'from research\.', 'from mirai.research.'),
        (r'from vtuber\.', 'from mirai.vtuber.'),
        (r'import core\.', 'import mirai.core.'),
        (r'import actions\.', 'import mirai.actions.'),
        (r'import modes\.', 'import mirai.modes.'),
        (r'import interface\.', 'import mirai.interface.'),
        (r'import perception\.', 'import mirai.perception.'),
        (r'import research\.', 'import mirai.research.'),
        (r'import vtuber\.', 'import mirai.vtuber.'),
    ]
    
    for pattern, replacement in replacements:
        content = re.sub(pattern, replacement, content)
    
    # Salva se mudou
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  ✓ Corrigido!")
        return True
    else:
        print(f"  - Já está correto")
        return False

# Corrige todos os arquivos .py em mirai/
print("🔧 CORRIGINDO IMPORTS...\n")

fixed_count = 0
for py_file in Path('mirai').rglob('*.py'):
    if '__pycache__' not in str(py_file):
        if fix_imports_in_file(py_file):
            fixed_count += 1

print(f"\n✅ {fixed_count} arquivos corrigidos!")
print("\nAgora execute: python run.py")