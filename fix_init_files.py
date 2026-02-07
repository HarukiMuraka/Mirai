from pathlib import Path

def fix_init_file(folder):
    """Corrige __init__.py de uma pasta"""
    init_file = Path(folder) / "__init__.py"
    
    # Conteúdo limpo
    clean_content = f"# {folder.capitalize()} module\n"
    
    try:
        # Cria ou sobrescreve
        with open(init_file, 'w', encoding='utf-8') as f:
            f.write(clean_content)
        
        print(f"✓ {folder}/__init__.py corrigido")
        return True
    except Exception as e:
        print(f"✗ Erro em {folder}: {e}")
        return False

if __name__ == "__main__":
    print("="*60)
    print("CORRIGINDO __init__.py DAS PASTAS")
    print("="*60)
    print()
    
    folders = [
        'core',
        'modes', 
        'perception',
        'actions',
        'research',
        'interface',
        'vtuber',
        'memory'
    ]
    
    success_count = 0
    
    for folder in folders:
        if Path(folder).exists():
            if fix_init_file(folder):
                success_count += 1
        else:
            print(f"⚠ Pasta {folder} não existe")
    
    print()
    print("="*60)
    print(f"RESULTADO: {success_count}/{len(folders)} corrigidos")
    print("="*60)
    print()
    print("Agora teste novamente:")
    print('  python -c "from research.search_engine_v2 import SearchEngineV2; print(\'OK!\')"')